import asyncio
import os
import sys
import requests
import json

# Add the backend src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'RAG-Backend', 'src'))

from core.config import settings

async def index_textbook_content():
    """Index the textbook content into the RAG system."""

    # Get all the textbook markdown files
    textbook_dir = os.path.join(os.path.dirname(__file__), 'docs')
    textbook_files = [f for f in os.listdir(textbook_dir) if f.endswith('.md') and f != 'intro.md']

    # Sort files by chapter number (assuming they start with numbers)
    textbook_files.sort()

    print(f"Found {len(textbook_files)} textbook files to index...")

    for i, filename in enumerate(textbook_files[:3]):  # Index first 3 chapters for testing
        filepath = os.path.join(textbook_dir, filename)

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract title from the first line if it's a markdown header
        lines = content.split('\n')
        title = filename.replace('.md', '').replace('-', ' ').title()
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()  # Remove '# ' prefix
                break

        print(f"Indexing {filename} (Chapter {i+1}): {title[:50]}...")

        # Prepare the document data
        document_data = {
            "title": title,
            "content": content[:5000],  # Limit content size for testing
            "url": f"/docs/{filename}",
            "author": "Textbook Authors",
            "source_type": "book"
        }

        # Upload to the backend
        try:
            response = requests.post(
                "http://localhost:8000/api/v1/documents",
                json=document_data,
                headers={"Content-Type": "application/json"},
                timeout=30  # 30 second timeout
            )

            if response.status_code == 200:
                result = response.json()
                print(f"  [SUCCESS] Successfully indexed: {result.get('document_id', 'Unknown ID')}")
            else:
                print(f"  [FAILED] Failed to index {filename}: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"  [ERROR] Error indexing {filename}: {str(e)}")

    print("\nTextbook content indexing completed!")

if __name__ == "__main__":
    asyncio.run(index_textbook_content())