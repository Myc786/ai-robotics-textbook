import uuid
from typing import List, Dict, Any
from src.models.book import Book, Chapter, Section
from src.models.chunk import Chunk
from src.utils.text_processing import (
    extract_text_from_pdf,
    extract_text_from_html,
    extract_text_from_markdown,
    chunk_text,
    count_tokens,
    preserve_hierarchy,
    extract_text_from_url,
    extract_urls_from_sitemap
)
from src.config.database import postgres_db, qdrant_db
from qdrant_client.http import models
import cohere
from src.config.settings import settings


class IngestionService:
    def __init__(self):
        self.cohere_client = cohere.Client(api_key=settings.cohere_api_key)
        self.postgres_db = postgres_db
        self.qdrant_db = qdrant_db

    async def ingest_book(self, source: str, source_type: str, book_title: str, author: str = None):
        """
        Ingest a book from various sources (files, URLs, sitemaps) and store in the database.

        Args:
            source: Path to the file, URL, or sitemap URL
            source_type: Type of source ('pdf', 'html', 'md', 'mdx', 'url', 'sitemap')
            book_title: Title of the book
            author: Author of the book (optional)
        """
        # Extract text from the source based on its type
        if source_type.lower() == 'pdf':
            content = extract_text_from_pdf(source)
        elif source_type.lower() == 'html':
            with open(source, 'r', encoding='utf-8') as file:
                content = extract_text_from_html(file.read())
        elif source_type.lower() in ['md', 'mdx']:
            with open(source, 'r', encoding='utf-8') as file:
                content = extract_text_from_markdown(file.read())
        elif source_type.lower() == 'url':
            content = extract_text_from_url(source)
        elif source_type.lower() == 'sitemap':
            # For sitemap, we'll extract all URLs and combine their content
            urls = extract_urls_from_sitemap(source)
            content = ""
            for url in urls:
                content += extract_text_from_url(url) + "\n\n"
        else:
            raise ValueError(f"Unsupported source type: {source_type}")

        # Preserve hierarchy (simplified implementation)
        hierarchy_elements = preserve_hierarchy(content)

        # Create book entry
        book_id = uuid.uuid4()

        # For this simplified implementation, we'll create one chapter and section with all content
        chapter_id = uuid.uuid4()
        section_id = uuid.uuid4()

        # Insert book, chapter, and section into the database
        query = """
            INSERT INTO books (book_id, title, author)
            VALUES ($1, $2, $3)
        """
        await self.postgres_db.connection.execute(
            query,
            book_id,
            book_title,
            author
        )

        query = """
            INSERT INTO chapters (chapter_id, book_id, title, content)
            VALUES ($1, $2, $3, $4)
        """
        await self.postgres_db.connection.execute(
            query,
            chapter_id,
            book_id,
            f"Chapter 1 of {book_title}",
            content
        )

        query = """
            INSERT INTO sections (section_id, chapter_id, title, content)
            VALUES ($1, $2, $3, $4)
        """
        await self.postgres_db.connection.execute(
            query,
            section_id,
            chapter_id,
            f"Section 1 of {book_title}",
            content
        )

        # Chunk the content
        chunks = chunk_text(content)

        # Process each chunk
        for i, chunk_text in enumerate(chunks):
            chunk_id = uuid.uuid4()
            token_count = count_tokens(chunk_text)

            # Generate embedding using Cohere
            response = self.cohere_client.embed(
                texts=[chunk_text],
                model="embed-english-v3.0",  # Using a standard Cohere embedding model
                input_type="search_document"
            )
            embedding = response.embeddings[0]

            # Store in Qdrant
            point_id = str(uuid.uuid4())
            self.qdrant_db.client.upsert(
                collection_name=self.qdrant_db.collection_name,
                points=[
                    models.PointStruct(
                        id=point_id,
                        vector=embedding,
                        payload={
                            "chunk_id": str(chunk_id),
                            "book_id": str(book_id),
                            "chapter_id": str(chapter_id),
                            "section_id": str(section_id),
                            "content": chunk_text
                        }
                    )
                ]
            )

            # Store chunk metadata in Postgres
            query = """
                INSERT INTO chunks (chunk_id, book_id, chapter_id, section_id, content, token_count, vector_id)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
            """
            await self.postgres_db.connection.execute(
                query,
                chunk_id,
                book_id,
                chapter_id,
                section_id,
                chunk_text,
                token_count,
                point_id
            )

        return {"book_id": book_id, "chunks_created": len(chunks)}

    async def get_book_content(self, book_id: uuid.UUID):
        """
        Retrieve all content associated with a book.
        
        Args:
            book_id: UUID of the book
            
        Returns:
            Dictionary with book content organized by hierarchy
        """
        # Get book info
        query = "SELECT * FROM books WHERE book_id = $1"
        book_record = await self.postgres_db.connection.fetchrow(query, book_id)
        
        # Get chapters
        query = "SELECT * FROM chapters WHERE book_id = $1"
        chapter_records = await self.postgres_db.connection.fetch(query, book_id)
        
        # Get sections for each chapter
        book_content = {
            "book": dict(book_record) if book_record else None,
            "chapters": []
        }
        
        for chapter in chapter_records:
            chapter_id = chapter['chapter_id']
            query = "SELECT * FROM sections WHERE chapter_id = $1"
            section_records = await self.postgres_db.connection.fetch(query, chapter_id)
            
            chapter_data = dict(chapter)
            chapter_data["sections"] = [dict(section) for section in section_records]
            book_content["chapters"].append(chapter_data)
        
        return book_content