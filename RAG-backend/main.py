#!/usr/bin/env python3
"""
RAG Chatbot Integration - Main Implementation

This script implements a RAG (Retrieval Augmented Generation) system that:
- Fetches content from deployed book websites
- Generates embeddings using Cohere
- Stores content in Qdrant vector database for retrieval
"""

import os
import sys
import logging
import argparse
import requests
import time
from typing import List, Dict, Optional, Tuple
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET

import cohere
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# FastAPI and related imports
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel

# OpenAI imports
from openai import OpenAI


# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Config:
    """Configuration class to manage environment variables and settings"""

    def __init__(self):
        self.cohere_api_key = os.getenv('COHERE_API_KEY')
        self.qdrant_url = os.getenv('QDRANT_URL', 'http://localhost:6333')
        self.qdrant_api_key = os.getenv('QDRANT_API_KEY')
        self.target_url = os.getenv('TARGET_URL')

        # Additional configuration parameters
        self.chunk_size = int(os.getenv('CHUNK_SIZE', '1000'))
        self.overlap = int(os.getenv('OVERLAP', '200'))
        self.collection_name = os.getenv('COLLECTION_NAME', 'RAG_embedding')
        self.max_retries = int(os.getenv('MAX_RETRIES', '3'))
        self.initial_backoff = float(os.getenv('INITIAL_BACKOFF', '1.0'))
        self.backoff_multiplier = float(os.getenv('BACKOFF_MULTIPLIER', '2.0'))

        # Validate required configuration
        if not self.cohere_api_key:
            logger.warning("COHERE_API_KEY not set in environment variables")
        if not self.qdrant_api_key:
            logger.info("QDRANT_API_KEY not set, using default settings")
        if not self.target_url:
            logger.info("TARGET_URL not set in environment variables")

    def validate(self) -> Tuple[bool, List[str]]:
        """Validate configuration and return (is_valid, errors)"""
        errors = []
        if not self.cohere_api_key:
            errors.append("COHERE_API_KEY is required")
        if not self.target_url:
            errors.append("TARGET_URL is required")

        return len(errors) == 0, errors


# Initialize configuration
config = Config()


def initialize_cohere_client():
    """Initialize Cohere client with proper error handling"""
    if not config.cohere_api_key:
        logger.error("Cohere API key not provided")
        return None

    try:
        cohere_client = cohere.Client(api_key=config.cohere_api_key)
        logger.info("Cohere client initialized successfully")
        return cohere_client
    except Exception as e:
        logger.error(f"Failed to initialize Cohere client: {str(e)}")
        return None


def initialize_qdrant_client():
    """Initialize Qdrant client with proper error handling"""
    try:
        if config.qdrant_api_key:
            qdrant_client = QdrantClient(
                url=config.qdrant_url,
                api_key=config.qdrant_api_key
            )
        else:
            qdrant_client = QdrantClient(url=config.qdrant_url)

        logger.info("Qdrant client initialized successfully")
        return qdrant_client
    except Exception as e:
        logger.error(f"Failed to initialize Qdrant client: {str(e)}")
        return None


# Initialize clients
cohere_client = initialize_cohere_client()
qdrant_client = initialize_qdrant_client()


class RAGException(Exception):
    """Base exception class for RAG operations"""
    pass


class NetworkError(RAGException):
    """Exception raised for network-related errors"""
    pass


class ContentExtractionError(RAGException):
    """Exception raised for content extraction errors"""
    pass


class EmbeddingGenerationError(RAGException):
    """Exception raised for embedding generation errors"""
    pass


class StorageError(RAGException):
    """Exception raised for storage-related errors"""
    pass


class URLDiscoveryError(RAGException):
    """Exception raised for URL discovery errors"""
    pass


def retry_with_backoff(max_retries: int = 3, initial_backoff: float = 1.0, backoff_multiplier: float = 2.0):
    """
    Decorator to implement retry mechanism with exponential backoff
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            backoff_time = initial_backoff

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (requests.RequestException, RAGException) as e:
                    last_exception = e
                    if attempt < max_retries - 1:  # Don't sleep on the last attempt
                        logger.warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in {backoff_time}s...")
                        time.sleep(backoff_time)
                        backoff_time *= backoff_multiplier
                    else:
                        logger.error(f"All {max_retries} attempts failed. Last error: {str(e)}")

            raise last_exception
        return wrapper
    return decorator


def main():
    """Main function to execute the complete RAG pipeline"""
    parser = argparse.ArgumentParser(description='RAG Chatbot Integration')
    parser.add_argument('command', choices=['index', 'status'], help='Command to execute')
    parser.add_argument('--target-url', type=str, help='Base URL of the book website to index')
    parser.add_argument('--chunk-size', type=int, default=config.chunk_size, help=f'Size of text chunks (default: {config.chunk_size})')
    parser.add_argument('--overlap', type=int, default=config.overlap, help=f'Overlap between chunks (default: {config.overlap})')
    parser.add_argument('--collection', type=str, default=config.collection_name, help=f'Qdrant collection name (default: {config.collection_name})')

    args = parser.parse_args()

    # Validate configuration
    is_valid, errors = config.validate()
    if not is_valid:
        for error in errors:
            logger.error(error)
        sys.exit(1)

    if args.command == 'index':
        target_url = args.target_url or config.target_url
        if not target_url:
            logger.error("Target URL is required. Use --target-url or set TARGET_URL in .env")
            sys.exit(1)

        logger.info(f"Starting indexing process for: {target_url}")
        # Execute the complete pipeline
        execute_pipeline(target_url, args.chunk_size, args.overlap, args.collection)

    elif args.command == 'status':
        logger.info("Checking system status...")
        check_status()


@retry_with_backoff(max_retries=config.max_retries, initial_backoff=config.initial_backoff, backoff_multiplier=config.backoff_multiplier)
def get_all_urls(base_url: str) -> Dict:
    """
    Discover and return all book page URLs from the provided base URL
    Will attempt to discover URLs from the sitemap at: https://ai-robotics-textbook.vercel.app/sitemap.xml
    Will fall back to web crawling if sitemap is not available or incomplete
    """
    sitemap_url = f"{base_url.rstrip('/')}/sitemap.xml"
    urls = set()  # Use set to avoid duplicates

    # Try to get URLs from sitemap first
    try:
        logger.info(f"Attempting to fetch URLs from sitemap: {sitemap_url}")
        response = requests.get(sitemap_url, timeout=10)
        if response.status_code == 200:
            # Parse sitemap XML
            root = ET.fromstring(response.content)
            # Handle both regular sitemap and sitemap index
            if root.tag.endswith('sitemapindex'):
                # This is a sitemap index, need to fetch individual sitemaps
                for sitemap_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap/{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                    sitemap_loc = sitemap_elem.text
                    logger.info(f"Found sub-sitemap: {sitemap_loc}")
                    sub_response = requests.get(sitemap_loc, timeout=10)
                    if sub_response.status_code == 200:
                        sub_root = ET.fromstring(sub_response.content)
                        for url_elem in sub_root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                            url = url_elem.text
                            if url and url.startswith(base_url):
                                urls.add(url)
            else:
                # This is a regular sitemap
                for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                    url = url_elem.text
                    if url and url.startswith(base_url):
                        urls.add(url)

            logger.info(f"Found {len(urls)} URLs from sitemap")
        else:
            logger.info(f"Sitemap not available at {sitemap_url}, will try crawling")
    except Exception as e:
        logger.warning(f"Could not fetch or parse sitemap: {str(e)}, will try crawling")

    # If sitemap didn't provide sufficient URLs, try basic crawling
    if len(urls) < 5:  # If we got very few URLs from sitemap, try crawling
        try:
            logger.info(f"Attempting to crawl base URL: {base_url}")
            response = requests.get(base_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find all links that are relative to the base URL
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(base_url, href)

                    # Only add URLs that are under the same domain/base URL
                    if full_url.startswith(base_url) and not any(x in full_url for x in ['#', 'mailto:', 'javascript:']):
                        urls.add(full_url)
        except Exception as e:
            logger.warning(f"Could not crawl base URL: {str(e)}")

    # Convert to list and return
    url_list = list(urls)
    result = {
        "urls": url_list,
        "total_count": len(url_list),
        "base_url": base_url,
        "sitemap_url": sitemap_url
    }

    logger.info(f"Discovered {len(url_list)} total URLs from base URL {base_url}")
    return result


def execute_pipeline(target_url: str, chunk_size: int, overlap: int, collection_name: str):
    """Execute the complete RAG pipeline"""
    logger.info("Starting RAG pipeline execution...")

    # 1. Create the collection in Qdrant
    logger.info(f"Creating/verifying Qdrant collection: {collection_name}")
    collection_result = create_collection(collection_name)
    if not collection_result["success"]:
        logger.error(f"Failed to create collection: {collection_result.get('error')}")
        return

    # 2. Get all URLs from the target site
    logger.info(f"Discovering URLs from: {target_url}")
    urls_result = get_all_urls(target_url)
    urls = urls_result["urls"]

    logger.info(f"Discovered {len(urls)} URLs to process")

    if not urls:
        logger.warning("No URLs found to process")
        return

    # 3. Process each URL: extract → chunk → embed → save to Qdrant
    processed_count = 0
    error_count = 0
    total_chunks = 0

    for i, url in enumerate(urls):
        # Progress tracking
        progress_percent = ((i + 1) / len(urls)) * 100
        logger.info(f"Processing URL {i+1}/{len(urls)} ({progress_percent:.1f}%): {url}")

        try:
            # Extract text content
            extraction_result = extract_text_from_url(url)
            if not extraction_result["success"]:
                logger.error(f"Failed to extract content from {url}: {extraction_result.get('error')}")
                error_count += 1
                continue

            content = extraction_result["content"]
            title = extraction_result["title"]
            metadata = extraction_result["metadata"]

            if not content.strip():
                logger.warning(f"No content extracted from {url}, skipping")
                continue

            # Chunk the content
            chunk_result = chunk_text(content, chunk_size=chunk_size, overlap=overlap)
            chunks = chunk_result["chunks"]

            logger.info(f"Chunked content into {len(chunks)} chunks")

            # For now, we'll save chunks without embeddings (we'll implement embedding in Phase 4)
            # For testing purposes, we'll use placeholder vectors
            for chunk_data in chunks:
                # Add additional metadata to the chunk
                chunk_data["url"] = url
                chunk_data["title"] = title
                chunk_data["source_type"] = metadata.get("source_type", "webpage")

                # Create a placeholder vector for now (will be replaced with real embeddings in Phase 4)
                # Using a simple vector of zeros for now - will be replaced with actual embeddings later
                placeholder_vector = [0.0] * 1024  # 1024 dimensions for Cohere embeddings

                # Save chunk to Qdrant
                save_result = save_chunk_to_qdrant(chunk_data, placeholder_vector)
                if save_result["success"]:
                    logger.debug(f"Saved chunk {chunk_data['chunk_index']} to Qdrant")
                    total_chunks += 1
                else:
                    logger.error(f"Failed to save chunk to Qdrant: {save_result.get('error')}")

            processed_count += 1
            logger.info(f"Successfully processed {url} ({processed_count}/{len(urls)})")

        except Exception as e:
            logger.error(f"Error processing {url}: {str(e)}")
            error_count += 1

    # Final progress and status report
    success_rate = (processed_count / len(urls) * 100) if urls else 0
    logger.info(f"Pipeline completed.")
    logger.info(f"  URLs processed: {processed_count}/{len(urls)} ({success_rate:.1f}%)")
    logger.info(f"  Chunks saved: {total_chunks}")
    logger.info(f"  Errors: {error_count}")
    logger.info(f"  Collection: {collection_name}")

    # Summary report
    print("\n" + "="*50)
    print("RAG PIPELINE EXECUTION SUMMARY")
    print("="*50)
    print(f"Target URL: {target_url}")
    print(f"Collection: {collection_name}")
    print(f"URLs processed: {processed_count}/{len(urls)}")
    print(f"Success rate: {success_rate:.1f}%")
    print(f"Total chunks saved: {total_chunks}")
    print(f"Errors: {error_count}")
    print("="*50)


@retry_with_backoff(max_retries=config.max_retries, initial_backoff=config.initial_backoff, backoff_multiplier=config.backoff_multiplier)
def embed(texts: List[str]) -> Dict:
    """
    Generate embeddings for text chunks using Cohere
    """
    if not cohere_client:
        return {
            "success": False,
            "vectors": [],
            "model": "",
            "text_count": 0,
            "error": "Cohere client not initialized"
        }

    try:
        # Generate embeddings using Cohere
        response = cohere_client.embed(
            texts=texts,
            model='embed-english-v3.0',
            input_type="search_document"
        )

        # Extract the embeddings from the response
        embeddings = response.embeddings
        # Handle different possible response formats from Cohere API
        if hasattr(response, 'meta') and response.meta:
            if hasattr(response.meta, 'model'):
                model_used = response.meta.model
            elif isinstance(response.meta, dict) and 'model' in response.meta:
                model_used = response.meta['model']
            else:
                model_used = 'embed-english-v3.0'
        else:
            model_used = 'embed-english-v3.0'

        # Convert to the expected format (list of lists)
        vectors = [embedding for embedding in embeddings]

        result = {
            "success": True,
            "vectors": vectors,
            "model": model_used,
            "text_count": len(texts)
        }

        logger.info(f"Generated embeddings for {len(texts)} texts using model: {model_used}")
        return result

    except Exception as e:
        logger.error(f"Error generating embeddings: {str(e)}")
        return {
            "success": False,
            "vectors": [],
            "model": "",
            "text_count": 0,
            "error": str(e)
        }


def execute_pipeline(target_url: str, chunk_size: int, overlap: int, collection_name: str):
    """Execute the complete RAG pipeline with embeddings"""
    logger.info("Starting RAG pipeline execution with embeddings...")

    # 1. Create the collection in Qdrant
    logger.info(f"Creating/verifying Qdrant collection: {collection_name}")
    collection_result = create_collection(collection_name)
    if not collection_result["success"]:
        logger.error(f"Failed to create collection: {collection_result.get('error')}")
        return

    # 2. Get all URLs from the target site
    logger.info(f"Discovering URLs from: {target_url}")
    urls_result = get_all_urls(target_url)
    if "urls" not in urls_result:
        logger.error(f"get_all_urls failed: {urls_result}")
        return

    urls = urls_result["urls"]

    logger.info(f"Discovered {len(urls)} URLs to process")

    if not urls:
        logger.warning("No URLs found to process")
        return

    # 3. Process each URL: extract → chunk → embed → save to Qdrant
    processed_count = 0
    error_count = 0
    total_chunks = 0

    for i, url in enumerate(urls):
        # Progress tracking
        progress_percent = ((i + 1) / len(urls)) * 100
        logger.info(f"Processing URL {i+1}/{len(urls)} ({progress_percent:.1f}%): {url}")

        try:
            # Extract text content
            extraction_result = extract_text_from_url(url)
            if not extraction_result or not extraction_result.get("success"):
                logger.error(f"Failed to extract content from {url}: {extraction_result.get('error', 'Unknown error')}")
                error_count += 1
                continue

            content = extraction_result.get("content", "")
            title = extraction_result.get("title", "")
            metadata = extraction_result.get("metadata", {})

            if not content or not content.strip():
                logger.warning(f"No content extracted from {url}, skipping")
                continue

            # Chunk the content
            chunk_result = chunk_text(content, chunk_size=chunk_size, overlap=overlap)
            if "chunks" not in chunk_result:
                logger.error(f"Chunking failed for {url}")
                error_count += 1
                continue

            chunks = chunk_result["chunks"]

            logger.info(f"Chunked content into {len(chunks)} chunks")

            # Extract text from chunks for embedding
            chunk_texts = [chunk.get("text", "") for chunk in chunks]

            # Generate embeddings for all chunks at once
            embed_result = embed(chunk_texts)
            if not embed_result.get("success"):
                logger.error(f"Failed to generate embeddings for {url}: {embed_result.get('error', 'Unknown error')}")
                # Continue processing but use placeholder vectors
                vectors = [[0.0] * 1024 for _ in chunk_texts]  # Placeholder vectors
            else:
                vectors = embed_result.get("vectors", [])

            # Validate embedding dimensions and ensure we have the right number of vectors
            if len(vectors) != len(chunks):
                logger.error(f"Mismatch between chunks ({len(chunks)}) and vectors ({len(vectors)}) for {url}")
                error_count += 1
                continue

            # Validate embedding dimensions
            for j, vector in enumerate(vectors):
                if not validate_embedding_dimensions(vector):
                    logger.warning(f"Invalid embedding dimensions for chunk {j} in {url}, using placeholder")
                    vectors[j] = [0.0] * 1024

            # Save each chunk with its embedding to Qdrant
            for chunk_data, vector in zip(chunks, vectors):
                # Add additional metadata to the chunk
                chunk_data["url"] = url
                chunk_data["title"] = title
                chunk_data["source_type"] = metadata.get("source_type", "webpage")

                # Save chunk to Qdrant
                save_result = save_chunk_to_qdrant(chunk_data, vector)
                if save_result and save_result.get("success"):
                    logger.debug(f"Saved chunk {chunk_data.get('chunk_index', 'unknown')} to Qdrant")
                    total_chunks += 1
                else:
                    logger.error(f"Failed to save chunk to Qdrant: {save_result.get('error', 'Unknown error')}")

            processed_count += 1
            logger.info(f"Successfully processed {url} ({processed_count}/{len(urls)})")

        except NetworkError as e:
            logger.error(f"Network error processing {url}: {str(e)}")
            error_count += 1
        except ContentExtractionError as e:
            logger.error(f"Content extraction error for {url}: {str(e)}")
            error_count += 1
        except EmbeddingGenerationError as e:
            logger.error(f"Embedding generation error for {url}: {str(e)}")
            error_count += 1
        except StorageError as e:
            logger.error(f"Storage error for {url}: {str(e)}")
            error_count += 1
        except Exception as e:
            logger.error(f"Unexpected error processing {url}: {str(e)}")
            error_count += 1

    # Final progress and status report
    success_rate = (processed_count / len(urls) * 100) if urls else 0
    logger.info(f"Pipeline completed.")
    logger.info(f"  URLs processed: {processed_count}/{len(urls)} ({success_rate:.1f}%)")
    logger.info(f"  Chunks saved: {total_chunks}")
    logger.info(f"  Errors: {error_count}")
    logger.info(f"  Collection: {collection_name}")

    # Summary report
    print("\n" + "="*50)
    print("RAG PIPELINE EXECUTION SUMMARY")
    print("="*50)
    print(f"Target URL: {target_url}")
    print(f"Collection: {collection_name}")
    print(f"URLs processed: {processed_count}/{len(urls)}")
    print(f"Success rate: {success_rate:.1f}%")
    print(f"Total chunks saved: {total_chunks}")
    print(f"Errors: {error_count}")
    print("="*50)


def check_status():
    """Check the status of the system components"""
    logger.info("System status check...")

    # Check configuration
    config_valid, config_errors = config.validate()

    # Check Cohere client
    cohere_connected = cohere_client is not None
    if cohere_connected:
        try:
            # Test Cohere client by making a simple call
            pass  # For now, just check if client is initialized
        except Exception:
            cohere_connected = False

    # Check Qdrant client
    qdrant_connected = qdrant_client is not None
    qdrant_collection_exists = False
    qdrant_point_count = 0

    if qdrant_connected:
        try:
            # Check if collection exists and get stats
            collections = qdrant_client.get_collections()
            qdrant_collection_exists = any(col.name == config.collection_name for col in collections.collections)

            if qdrant_collection_exists:
                # Get point count for the collection
                try:
                    count = qdrant_client.count(config.collection_name)
                    qdrant_point_count = count.count
                except:
                    qdrant_point_count = 0  # Collection exists but couldn't get count
        except Exception as e:
            logger.error(f"Error checking Qdrant status: {str(e)}")
            qdrant_connected = False

    status = {
        "config_valid": config_valid,
        "config_errors": config_errors,
        "cohere_client": cohere_connected,
        "qdrant_client": qdrant_connected,
        "qdrant_collection_exists": qdrant_collection_exists,
        "qdrant_point_count": qdrant_point_count
    }

    logger.info(f"Configuration: {'Valid' if status['config_valid'] else 'Invalid'}")
    if not status['config_valid']:
        for error in status['config_errors']:
            logger.error(f"  - {error}")

    logger.info(f"Cohere client: {'Connected' if status['cohere_client'] else 'Not connected'}")
    logger.info(f"Qdrant client: {'Connected' if status['qdrant_client'] else 'Not connected'}")
    logger.info(f"Qdrant collection '{config.collection_name}': {'Exists' if status['qdrant_collection_exists'] else 'Does not exist'}")
    logger.info(f"Qdrant points stored: {status['qdrant_point_count']}")

    return status


@retry_with_backoff(max_retries=config.max_retries, initial_backoff=config.initial_backoff, backoff_multiplier=config.backoff_multiplier)
def extract_text_from_url(url: str) -> Dict:
    """
    Extract clean text content from a given URL
    """
    try:
        logger.info(f"Extracting text from URL: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Extract title
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else "No Title"

        # Extract main content - try common content containers
        content_selectors = [
            'main',  # Main content area
            'article',  # Article content
            '[role="main"]',  # ARIA role main
            '.content',  # Common content class
            '.post-content',  # Post content
            '.article-content',  # Article content
            'body'  # Fallback to body
        ]

        content_text = ""
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                content_text = content_elem.get_text(separator=' ', strip=True)
                break

        # If no specific content container found, extract from body
        if not content_text:
            body = soup.find('body')
            if body:
                content_text = body.get_text(separator=' ', strip=True)

        # Clean up the text
        content_text = ' '.join(content_text.split())  # Normalize whitespace

        # Prepare metadata
        metadata = {
            "url": url,
            "source_type": "webpage",
            "content_length": len(content_text),
            "fetch_time": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        }

        result = {
            "success": True,
            "content": content_text,
            "title": title,
            "metadata": metadata
        }

        logger.info(f"Successfully extracted content from {url} ({len(content_text)} chars)")
        return result

    except requests.RequestException as e:
        error_msg = f"Network error while fetching {url}: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "metadata": {"url": url}
        }
    except Exception as e:
        error_msg = f"Content extraction error for {url}: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "metadata": {"url": url}
        }


def clean_text_content(text: str) -> str:
    """
    Clean and sanitize text content
    """
    if not text:
        return ""

    # Remove extra whitespace
    cleaned = ' '.join(text.split())

    # Remove special characters that might cause issues
    # Keep basic punctuation and common symbols
    import re
    cleaned = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\'\"/]', ' ', cleaned)

    # Normalize whitespace again after regex
    cleaned = ' '.join(cleaned.split())

    return cleaned


def chunk_text(content: str, chunk_size: int = 1000, overlap: int = 200) -> Dict:
    """
    Split content into manageable chunks with metadata
    """
    if not content:
        return {
            "chunks": [],
            "chunk_count": 0,
            "original_length": 0
        }

    chunks = []
    start = 0
    chunk_index = 0

    while start < len(content):
        # Determine the end position for this chunk
        end = start + chunk_size

        # If we're near the end, make sure to include the remainder
        if end > len(content):
            end = len(content)

        # Create the chunk
        chunk_text = content[start:end]

        chunk_data = {
            "text": chunk_text,
            "chunk_index": chunk_index,
            "original_length": len(content),
            "start_pos": start,
            "end_pos": end
        }

        chunks.append(chunk_data)

        # Move start position forward by (chunk_size - overlap)
        start += (chunk_size - overlap)
        chunk_index += 1

        # If we've reached the end, break
        if end >= len(content):
            break

    result = {
        "chunks": chunks,
        "chunk_count": len(chunks),
        "original_length": len(content)
    }

    logger.info(f"Content chunked into {len(chunks)} chunks")
    return result


def create_collection(collection_name: str = "RAG_embedding") -> Dict:
    """
    Create or verify the existence of the Qdrant collection with optimized schema for embedding storage
    """
    if not qdrant_client:
        return {
            "success": False,
            "collection_name": collection_name,
            "created": False,
            "error": "Qdrant client not initialized"
        }

    try:
        # Check if collection exists
        collections = qdrant_client.get_collections()
        collection_exists = any(col.name == collection_name for col in collections.collections)

        if not collection_exists:
            # Create collection with optimized settings for embedding storage
            # 1024 dimensions for Cohere embeddings with cosine distance
            qdrant_client.recreate_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
                # Add payload schema for optimized storage
                optimizers_config={
                    "memmap_threshold": 20000,  # Use memory mapping for faster access
                    "indexing_threshold": 20000,  # Index vectors after this many points
                },
                # Enable HNSW index for faster similarity search
                hnsw_config={
                    "m": 16,  # Max number of edges per node
                    "ef_construct": 100,  # Construction time / quality
                    "full_scan_threshold": 10000,  # Use full scan for small collections
                }
            )
            logger.info(f"Created optimized Qdrant collection: {collection_name}")
            return {
                "success": True,
                "collection_name": collection_name,
                "created": True
            }
        else:
            logger.info(f"Qdrant collection already exists: {collection_name}")
            return {
                "success": True,
                "collection_name": collection_name,
                "created": False
            }

    except Exception as e:
        logger.error(f"Error creating Qdrant collection {collection_name}: {str(e)}")
        return {
            "success": False,
            "collection_name": collection_name,
            "created": False,
            "error": str(e)
        }


def save_chunk_to_qdrant(chunk_data: Dict, vector: List[float]) -> Dict:
    """
    Store a single chunk with its embedding in Qdrant
    """
    if not qdrant_client:
        return {
            "success": False,
            "chunk_id": None,
            "error": "Qdrant client not initialized"
        }

    try:
        # Generate a consistent ID for this chunk based on content and URL for idempotency
        import hashlib
        content_for_id = f"{chunk_data.get('url', '')}_{chunk_data.get('text', '')[:100]}_{chunk_data.get('chunk_index', 0)}"
        chunk_id = hashlib.md5(content_for_id.encode()).hexdigest()

        # Prepare the payload with metadata following data model specification
        payload = {
            "url": chunk_data.get("url", ""),
            "title": chunk_data.get("title", ""),
            "content": chunk_data.get("text", "")[:1000],  # Store first 1000 chars to avoid large payloads
            "content_id": chunk_data.get("content_id", chunk_data.get("url", "")),  # Use URL as content_id if not provided
            "chunk_index": chunk_data.get("chunk_index", 0),
            "source_type": chunk_data.get("source_type", "webpage"),
            "start_pos": chunk_data.get("start_pos", 0),
            "end_pos": chunk_data.get("end_pos", 0),
            "original_length": chunk_data.get("original_length", 0)
        }

        # Prepare the point to be inserted
        points = [PointStruct(
            id=chunk_id,
            vector=vector,
            payload=payload
        )]

        # Upsert the point to the collection
        qdrant_client.upsert(
            collection_name=config.collection_name,
            points=points
        )

        logger.info(f"Successfully saved chunk to Qdrant with ID: {chunk_id}")
        return {
            "success": True,
            "chunk_id": chunk_id
        }

    except Exception as e:
        logger.error(f"Error saving chunk to Qdrant: {str(e)}")
        return {
            "success": False,
            "chunk_id": None,
            "error": str(e)
        }


@retry_with_backoff(max_retries=config.max_retries, initial_backoff=config.initial_backoff, backoff_multiplier=config.backoff_multiplier)
def search_similar_chunks(query_embedding: List[float], collection_name: str = "RAG_embedding", limit: int = 5) -> List[Dict]:
    """
    Implement similarity search functionality for retrieval
    """
    if not qdrant_client:
        logger.error("Qdrant client not initialized for search")
        return []

    try:
        # Perform similarity search using the query embedding
        search_results = qdrant_client.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=limit,
            with_payload=True,
            with_vectors=False
        )

        # Format results
        results = []
        for result in search_results:
            formatted_result = {
                "id": result.id,
                "score": result.score,
                "payload": result.payload
            }
            results.append(formatted_result)

        logger.info(f"Found {len(results)} similar chunks")
        return results

    except Exception as e:
        logger.error(f"Error searching for similar chunks: {str(e)}")
        return []


def validate_embedding_dimensions(vector: List[float], expected_size: int = 1024) -> bool:
    """
    Add vector dimension validation for Cohere embeddings (1024 dimensions)
    """
    return len(vector) == expected_size


def validate_url(url: str) -> bool:
    """
    Validate URL format and accessibility
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def validate_content_length(content: str, min_length: int = 10) -> bool:
    """
    Validate content length meets minimum requirements
    """
    return len(content) >= min_length if content else False


# FastAPI Application
app = FastAPI(title="RAG Chatbot API", version="1.0.0")

# Add CORS middleware to allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: List[str]


def retrieve_chunks(query: str, top_k: int = 5) -> List[Dict]:
    """
    Retrieval tool: query → Cohere embed → Qdrant search → return top 5 chunks as string
    """
    try:
        # Generate embedding for the query using Cohere
        if not cohere_client:
            logger.error("Cohere client not initialized")
            return []

        response = cohere_client.embed(
            texts=[query],
            model='embed-english-v3.0',
            input_type="search_query"  # As specified in the requirements
        )
        query_embedding = response.embeddings[0]

        # Search in Qdrant for similar vectors
        search_results = search_similar_chunks(
            query_embedding=query_embedding,
            collection_name=config.collection_name,
            limit=top_k
        )

        # Format results to include text, score, and metadata
        chunks = []
        for result in search_results:
            chunk_data = {
                'text': result['payload'].get('content', ''),
                'score': result['score'],
                'url': result['payload'].get('url', ''),
                'title': result['payload'].get('title', ''),
                'chunk_index': result['payload'].get('chunk_index', 0)
            }
            chunks.append(chunk_data)

        return chunks

    except Exception as e:
        logger.error(f"Error during retrieval: {e}")
        return []


def create_openai_agent():
    """
    Create OpenAI Agent with retrieval tool and system prompt
    """
    # Initialize OpenAI client
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    # If using a custom endpoint (like Qwen), set the base URL
    openai_base_url = os.getenv("OPENAI_BASE_URL")
    if openai_base_url:
        client = OpenAI(api_key=openai_api_key, base_url=openai_base_url)
    else:
        client = OpenAI(api_key=openai_api_key)

    return client


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    POST /chat endpoint: accept {"question": "..."}, run agent, return {"answer": "...", "sources": [urls]}
    """
    try:
        question = request.question.strip()
        if not question:
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        # Retrieve relevant chunks using the retrieval tool
        retrieved_chunks = retrieve_chunks(question, top_k=5)

        if not retrieved_chunks:
            return ChatResponse(
                answer="I couldn't find any relevant information to answer your question.",
                sources=[]
            )

        # Prepare context from retrieved chunks
        context_parts = []
        sources = set()  # Use set to avoid duplicate URLs

        for chunk in retrieved_chunks:
            if chunk['text'].strip():  # Only add non-empty chunks
                context_parts.append(f"Source: {chunk['title']}\nURL: {chunk['url']}\nContent: {chunk['text'][:500]}...")  # Limit content length
                if chunk['url']:
                    sources.add(chunk['url'])

        context = "\n\n".join(context_parts)

        # Create the system prompt as specified
        system_prompt = "Answer only using the provided book content. Cite sources."

        # Prepare the full prompt with context
        full_prompt = f"""
        Context:
        {context}

        Question: {question}

        Please provide an answer based only on the provided context and cite the sources.
        """

        # Create OpenAI client and get response
        client = create_openai_agent()

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can change this to your preferred model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.3,  # Lower temperature for more consistent answers
            max_tokens=1000
        )

        answer = response.choices[0].message.content

        return ChatResponse(
            answer=answer,
            sources=list(sources)
        )

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "RAG Chatbot API"}


if __name__ == "__main__":
    main()