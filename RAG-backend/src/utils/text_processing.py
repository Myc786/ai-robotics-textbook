import re
import fitz  # PyMuPDF
import tiktoken
from typing import List, Tuple
from bs4 import BeautifulSoup
import markdown
import requests
from urllib.parse import urljoin, urlparse


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text content from a PDF file.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Extracted text content
    """
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def extract_text_from_html(html_content: str) -> str:
    """
    Extract text content from HTML.

    Args:
        html_content: HTML string

    Returns:
        Extracted text content
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()


def extract_text_from_markdown(md_content: str) -> str:
    """
    Extract text content from Markdown.

    Args:
        md_content: Markdown string

    Returns:
        Extracted text content
    """
    html = markdown.markdown(md_content)
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()


def chunk_text(text: str, max_tokens: int = 500, overlap_ratio: float = 0.15) -> List[str]:
    """
    Split text into chunks with a maximum token count.

    Args:
        text: Input text to chunk
        max_tokens: Maximum number of tokens per chunk
        overlap_ratio: Ratio of overlap between chunks

    Returns:
        List of text chunks
    """
    # Initialize the encoding for token counting
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")  # Using a common encoding

    # Split text into sentences to maintain semantic coherence
    sentences = re.split(r'[.!?]+\s+', text)

    chunks = []
    current_chunk = ""
    current_token_count = 0

    for sentence in sentences:
        # Count tokens in the sentence
        sentence_tokens = len(encoding.encode(sentence))

        # If adding this sentence would exceed the limit
        if current_token_count + sentence_tokens > max_tokens:
            if current_chunk.strip():  # If there's content in the current chunk
                chunks.append(current_chunk.strip())

            # Start a new chunk with the current sentence
            current_chunk = sentence
            current_token_count = sentence_tokens
        else:
            # Add the sentence to the current chunk
            current_chunk += " " + sentence if current_chunk else sentence
            current_token_count += sentence_tokens

    # Add the last chunk if it has content
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    # Apply overlap if needed
    if overlap_ratio > 0 and len(chunks) > 1:
        overlap_chunks = []
        overlap_size = int(max_tokens * overlap_ratio)

        for i, chunk in enumerate(chunks):
            if i == 0:
                overlap_chunks.append(chunk)
            else:
                # Get the last part of the previous chunk to add as overlap
                prev_chunk_tokens = encoding.encode(chunks[i-1])
                overlap_tokens = prev_chunk_tokens[-overlap_size:]
                overlap_text = encoding.decode(overlap_tokens)

                # Combine overlap with current chunk
                new_chunk = overlap_text + " " + chunk
                overlap_chunks.append(new_chunk)

        chunks = overlap_chunks

    return chunks


def count_tokens(text: str) -> int:
    """
    Count the number of tokens in a text string.

    Args:
        text: Input text

    Returns:
        Number of tokens
    """
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoding.encode(text))


def preserve_hierarchy(text: str) -> List[Tuple[str, str, str, str]]:
    """
    Preserve the book hierarchy (Book → Chapter → Section) in the text.

    Args:
        text: Input text with hierarchy markers

    Returns:
        List of tuples (book_title, chapter_title, section_title, content)
    """
    # This is a simplified implementation
    # In a real implementation, you would parse the actual hierarchy
    # based on the document structure

    # Example regex patterns for detecting hierarchy
    book_pattern = r'# Book: (.+)'
    chapter_pattern = r'## Chapter: (.+)'
    section_pattern = r'### Section: (.+)'

    # For now, return a single hierarchy element
    # This would be expanded based on actual document parsing needs
    return [("Default Book", "Default Chapter", "Default Section", text)]


def extract_text_from_url(url: str) -> str:
    """
    Extract text content from a webpage URL.

    Args:
        url: URL of the webpage

    Returns:
        Extracted text content
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get text content
        text = soup.get_text()

        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        return text
    except Exception as e:
        print(f"Error extracting text from URL {url}: {e}")
        return ""


def extract_urls_from_sitemap(sitemap_url: str) -> List[str]:
    """
    Extract URLs from a sitemap.

    Args:
        sitemap_url: URL of the sitemap

    Returns:
        List of URLs extracted from the sitemap
    """
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'xml')  # Use xml parser for sitemaps
        urls = []

        # Look for <url><loc> elements in the sitemap
        for loc in soup.find_all('loc'):
            urls.append(loc.text.strip())

        return urls
    except Exception as e:
        print(f"Error extracting URLs from sitemap {sitemap_url}: {e}")
        return []