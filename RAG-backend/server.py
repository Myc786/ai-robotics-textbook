#!/usr/bin/env python3
"""
FastAPI server for RAG Chatbot - Separate from main indexing logic
"""

import os
import sys
import logging
import time
from typing import List, Dict
from urllib.parse import urljoin, urlparse

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

# Google Generative AI imports
import google.generativeai as genai
from google.generativeai import GenerativeModel

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

    def validate(self):
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
                except Exception as e:
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
    query: str


class ChatResponse(BaseModel):
    response: str
    retrieved_chunks: List[Dict]
    execution_time_ms: float


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


def create_llm_client():
    """
    Create LLM client supporting OpenRouter, OpenAI, and Google Gemini
    """
    # Try OpenRouter first
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    openrouter_base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

    if openrouter_api_key:
        client = OpenAI(
            api_key=openrouter_api_key,
            base_url=openrouter_base_url
        )
        return client, "openrouter"
    # Try Google Gemini next
    elif os.getenv("GEMINI_API_KEY"):
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=gemini_api_key)
        model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        # For native Google SDK, use just the model name (without 'models/' prefix)
        if model_name.startswith("models/"):
            model_name = model_name[7:]  # Remove "models/" prefix for native SDK
        model = genai.GenerativeModel(model_name)
        return model, "gemini"
    else:
        # Fallback to OpenAI
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENROUTER_API_KEY, GEMINI_API_KEY, or OPENAI_API_KEY must be set in environment variables")

        # If using a custom endpoint (like Qwen), set the base URL
        openai_base_url = os.getenv("OPENAI_BASE_URL")
        if openai_base_url:
            client = OpenAI(api_key=openai_api_key, base_url=openai_base_url)
        else:
            client = OpenAI(api_key=openai_api_key)

        return client, "openai"


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    POST /api/v1/chat endpoint: accept {"query": "..."}, run agent, return {"response": "...", "retrieved_chunks": [...], "execution_time_ms": ...}
    """
    start_time = time.time()
    try:
        question = request.query.strip()
        if not question:
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        # Retrieve relevant chunks using the retrieval tool
        retrieved_chunks = retrieve_chunks(question, top_k=5)

        if not retrieved_chunks:
            response_time = (time.time() - start_time) * 1000
            return ChatResponse(
                response="I couldn't find any relevant information to answer your question.",
                retrieved_chunks=[],
                execution_time_ms=response_time
            )

        # Prepare context from retrieved chunks
        context_parts = []

        for chunk in retrieved_chunks:
            if chunk['text'].strip():  # Only add non-empty chunks
                context_parts.append(f"Source: {chunk['title']}\nURL: {chunk['url']}\nContent: {chunk['text'][:500]}...")  # Limit content length

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

        # Create LLM client (OpenRouter, Google Gemini, or OpenAI)
        llm_client, client_type = create_llm_client()

        if client_type == "gemini":
            # Using Google Gemini
            full_prompt_with_system = f"{system_prompt}\n\n{full_prompt}"
            response = llm_client.generate_content(
                full_prompt_with_system,
                generation_config={
                    "temperature": 0.3,
                    "max_output_tokens": 1000,
                }
            )
            answer = response.text
        else:
            # Using OpenAI-compatible client (OpenRouter or OpenAI)
            if client_type == "openrouter":
                model_name = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")
                # Create completion with OpenRouter-specific headers
                response = llm_client.chat.completions.create(
                    model=model_name,  # Using model from environment
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": full_prompt}
                    ],
                    temperature=0.3,  # Lower temperature for more consistent answers
                    max_tokens=1000,
                    extra_headers={
                        "HTTP-Referer": os.getenv("YOUR_SITE_URL", "http://localhost:3000"), # Optional. Site URL for rankings on openrouter.ai.
                        "X-Title": os.getenv("YOUR_SITE_NAME", "AI Textbook Assistant"), # Optional. Site title for rankings on openrouter.ai.
                    }
                )
            else:
                model_name = os.getenv("GEMINI_MODEL") or os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
                response = llm_client.chat.completions.create(
                    model=model_name,  # Using model from environment
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": full_prompt}
                    ],
                    temperature=0.3,  # Lower temperature for more consistent answers
                    max_tokens=1000
                )
            answer = response.choices[0].message.content
        response_time = (time.time() - start_time) * 1000

        return ChatResponse(
            response=answer,
            retrieved_chunks=retrieved_chunks,
            execution_time_ms=response_time
        )

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        response_time = (time.time() - start_time) * 1000
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "RAG Chatbot API"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)