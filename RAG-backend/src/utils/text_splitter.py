from typing import List, Optional
import re
from ..core.config import settings


class TextSplitter:
    """
    Utility class for splitting text into chunks suitable for embedding and retrieval.
    """

    def __init__(
        self,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None
    ):
        self.chunk_size = chunk_size or settings.max_chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap

    def split_text(self, text: str) -> List[str]:
        """
        Split text into chunks of specified size with overlap.

        Args:
            text: The input text to split

        Returns:
            List of text chunks
        """
        if len(text) <= self.chunk_size:
            return [text]

        chunks = []
        start = 0

        while start < len(text):
            # Determine the end position
            end = start + self.chunk_size

            # If we're at the end of the text, take the remainder
            if end >= len(text):
                chunks.append(text[start:])
                break

            # Try to break at sentence boundary
            # Look for sentence endings (., !, ?) near the end of the chunk
            chunk_text = text[start:end]
            sentence_end_pos = -1

            # Look for sentence boundaries from the end of the chunk
            for punct in ['.', '!', '?', ';']:
                pos = chunk_text.rfind(punct)
                if pos != -1:
                    sentence_end_pos = pos
                    break

            # If found a sentence boundary and it's not too close to the beginning
            if sentence_end_pos != -1 and sentence_end_pos > len(chunk_text) * 0.5:
                end = start + sentence_end_pos + 1  # Include the punctuation
            else:
                # Look for word boundary if no sentence boundary found
                word_end_pos = chunk_text.rfind(' ')
                if word_end_pos != -1 and word_end_pos > len(chunk_text) * 0.7:
                    end = start + word_end_pos

            # Add the chunk
            chunk = text[start:end]
            chunks.append(chunk)

            # Move start position, considering overlap
            start = end - self.chunk_overlap

            # Prevent infinite loop in case chunking doesn't advance
            if start >= end:
                start = end

        # Filter out empty chunks
        chunks = [chunk.strip() for chunk in chunks if chunk.strip()]

        return chunks

    def split_by_section(
        self,
        text: str,
        section_pattern: Optional[str] = r'\n\s*#\s*[A-Za-z0-9\s]+\n|\n\s*##\s*[A-Za-z0-9\s]+\n'
    ) -> List[str]:
        """
        Split text by sections (e.g., chapters, headings) and then further chunk if needed.

        Args:
            text: The input text to split
            section_pattern: Regex pattern to identify section breaks

        Returns:
            List of text chunks
        """
        if section_pattern and re.search(section_pattern, text):
            sections = re.split(section_pattern, text)
            chunks = []
            for section in sections:
                if len(section.strip()) > 0:
                    if len(section) <= self.chunk_size:
                        chunks.append(section.strip())
                    else:
                        # If section is too large, further split it
                        sub_chunks = self.split_text(section)
                        chunks.extend(sub_chunks)
            return [chunk for chunk in chunks if chunk.strip()]
        else:
            # If no sections found, just use regular splitting
            return self.split_text(text)


# Global instance of the text splitter
text_splitter = TextSplitter()