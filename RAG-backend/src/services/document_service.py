from typing import List, Optional
from uuid import uuid4
from datetime import datetime
import logging
from ..models.document import DocumentChunk, Document
from ..models.database import DocumentDB, DocumentChunkDB
from ..services.embedding_service import embedding_service
from ..services.vector_store_service import vector_store_service
from ..utils.text_splitter import text_splitter
from ..core.logger import setup_logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class DocumentService:
    def __init__(self):
        self.logger = setup_logger(__name__)

    async def process_and_store_document(
        self,
        title: str,
        content: str,
        url: Optional[str] = None,
        author: Optional[str] = None,
        source_type: str = "book",
        metadata: Optional[dict] = None,
        db_session: AsyncSession = None
    ) -> str:
        """
        Process and store a document by splitting it, generating embeddings, and storing in both databases.

        Args:
            title: Title of the document
            content: Content of the document
            url: Optional URL of the document
            author: Optional author of the document
            source_type: Type of source (default: "book")
            metadata: Optional additional metadata
            db_session: Database session for Postgres operations

        Returns:
            Document ID of the processed document
        """
        try:
            # Generate a unique document ID
            document_id = str(uuid4())

            self.logger.info(f"Processing document: {title} (ID: {document_id})")

            # Split the content into chunks
            content_chunks = text_splitter.split_text(content)
            self.logger.info(f"Split document into {len(content_chunks)} chunks")

            # Create Document object for metadata
            document = Document(
                id=document_id,
                title=title,
                author=author,
                url=url,
                source_type=source_type,
                total_chunks=len(content_chunks),
                metadata=metadata
            )

            # Store document metadata in Postgres if session provided
            if db_session:
                # Check if db_session is not None before using it
                from sqlalchemy.ext.asyncio import AsyncSession
                if isinstance(db_session, AsyncSession):
                    db_document = DocumentDB(
                        id=document_id,
                        title=title,
                        author=author,
                        url=url,
                        source_type=source_type,
                        status="indexing",
                        total_chunks=len(content_chunks),
                        metadata=metadata
                    )
                    db_session.add(db_document)
                    await db_session.flush()  # Ensure the document is saved before proceeding

            # Create DocumentChunk objects
            document_chunks = []
            for i, chunk_content in enumerate(content_chunks):
                chunk_id = f"{document_id}_chunk_{i}"
                chunk = DocumentChunk(
                    chunk_id=chunk_id,
                    document_id=document_id,
                    content=chunk_content,
                    url=url,
                    metadata={"original_chunk_index": i}
                )
                document_chunks.append(chunk)

            # Generate embeddings for all chunks
            chunk_texts = [chunk.content for chunk in document_chunks]
            embeddings = await embedding_service.embed_texts(chunk_texts)

            # Store chunks in vector database (Qdrant)
            await vector_store_service.upsert_document_chunks(document_chunks, embeddings)

            # Store chunk metadata in Postgres if session provided
            if db_session:
                # Check if db_session is not None before using it
                from sqlalchemy.ext.asyncio import AsyncSession
                if isinstance(db_session, AsyncSession):
                    for chunk in document_chunks:
                        db_chunk = DocumentChunkDB(
                            chunk_id=chunk.chunk_id,
                            document_id=chunk.document_id,
                            content=chunk.content,
                            url=chunk.url,
                            metadata=chunk.metadata
                        )
                        db_session.add(db_chunk)

                    # Update document status to indexed
                    result = await db_session.execute(
                        select(DocumentDB).where(DocumentDB.id == document_id)
                    )
                    db_doc = result.scalars().first()
                    if db_doc:
                        db_doc.status = "indexed"
                        db_doc.indexed_chunks = len(document_chunks)

                    await db_session.commit()

            self.logger.info(f"Successfully processed and stored document: {title}")

            return document_id

        except Exception as e:
            self.logger.error(f"Error processing document: {str(e)}")
            if db_session:
                # Check if db_session is not None before using it
                from sqlalchemy.ext.asyncio import AsyncSession
                if isinstance(db_session, AsyncSession):
                    await db_session.rollback()
            raise

    async def delete_document(
        self,
        document_id: str,
        db_session: AsyncSession = None
    ):
        """
        Delete a document and all its chunks from both databases.

        Args:
            document_id: ID of the document to delete
            db_session: Database session for Postgres operations
        """
        try:
            self.logger.info(f"Deleting document: {document_id}")

            # Delete from vector database (Qdrant)
            await vector_store_service.delete_document_chunks(document_id)

            # Delete from Postgres if session provided
            if db_session:
                # Check if db_session is not None before using it
                from sqlalchemy.ext.asyncio import AsyncSession
                if isinstance(db_session, AsyncSession):
                    # Delete document chunks
                    await db_session.execute(
                        DocumentChunkDB.__table__.delete().where(
                            DocumentChunkDB.document_id == document_id
                        )
                    )

                    # Delete document
                    await db_session.execute(
                        DocumentDB.__table__.delete().where(
                            DocumentDB.id == document_id
                        )
                    )

                    await db_session.commit()

            self.logger.info(f"Successfully deleted document: {document_id}")

        except Exception as e:
            self.logger.error(f"Error deleting document: {str(e)}")
            if db_session:
                # Check if db_session is not None before using it
                from sqlalchemy.ext.asyncio import AsyncSession
                if isinstance(db_session, AsyncSession):
                    await db_session.rollback()
            raise


# Global instance of the document service
document_service = DocumentService()