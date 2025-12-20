# Implementation Plan: RAG Chatbot Integration

**Feature**: RAG Chatbot Integration
**Branch**: 001-rag-chatbot-integration
**Created**: 2025-12-17
**Status**: Draft
**Author**: Claude Sonnet 4.5

## Technical Context

This implementation will create a RAG (Retrieval Augmented Generation) system that fetches book content from deployed websites, generates embeddings, and stores them in a vector database for retrieval. The system will be built as a single main.py file with the following components:

- **UV package manager** for project initialization
- **Cohere client** for generating embeddings
- **Qdrant client** for vector database operations
- **Content fetching and cleaning** utilities
- **Text chunking** functionality
- **Metadata management** for knowledge base entries

**Unknowns requiring clarification**:
- Specific book URLs to index (RESOLVED: Will accept URLs as command-line arguments)
- Cohere API key management approach (RESOLVED: Will use environment variables)
- Qdrant configuration details (RESOLVED: Will support both cloud and local instances via environment variables)
- Target number of documents to process (RESOLVED: Will be variable, with batch processing for scalability)

## Architecture Decision Record (ADR)

### ADR-001: Single File Architecture
**Decision**: Implement entire RAG system in a single main.py file
**Rationale**: Simplifies deployment and understanding for initial implementation
**Status**: Proposed

### ADR-002: UV Package Manager
**Decision**: Use UV for project dependency management
**Rationale**: Modern, fast Python package manager that's a drop-in replacement for pip
**Status**: Proposed

## Constitution Check

### Principle Compliance Analysis

**Library-First Principle**:
- The implementation will be structured as a single module with clear functions
- Functions will be designed to be reusable and testable

**CLI Interface Principle**:
- The main.py will include a command-line interface for running the indexing process
- Input/output will follow text-in/text-out protocols

**Test-First Principle**:
- Unit tests will be developed for each major function
- Integration tests will verify the complete indexing pipeline

**Integration Testing**:
- Tests will verify Cohere and Qdrant client interactions
- End-to-end tests will validate the complete pipeline

### Compliance Status
- [x] Library-First: Functions will be designed as reusable units
- [x] CLI Interface: Command-line arguments will control indexing behavior
- [x] Test-First: Tests will be written alongside implementation
- [x] Integration Testing: Client interactions will be tested

## Phase 0: Research & Discovery

### Research Tasks

1. **Dependency Research**:
   - UV package manager setup and usage patterns
   - Cohere Python client best practices
   - Qdrant Python client integration patterns
   - Web scraping and content extraction techniques

2. **Technical Unknowns Resolution**:
   - Determine optimal text chunking strategies for book content
   - Research error handling patterns for API clients
   - Identify metadata fields to store with embeddings

### Research Outcomes

#### Decision: Package Management
- **Chosen**: UV package manager
- **Rationale**: Faster than pip, drop-in replacement, modern Python tooling
- **Alternatives considered**: pip, Poetry, Pipenv

#### Decision: Embedding Provider
- **Chosen**: Cohere API
- **Rationale**: High-quality embeddings, good documentation, reliable service
- **Alternatives considered**: OpenAI, Hugging Face, Sentence Transformers

#### Decision: Vector Database
- **Chosen**: Qdrant
- **Rationale**: Efficient similarity search, good Python client, supports metadata
- **Alternatives considered**: Pinecone, Weaviate, FAISS

#### Decision: Content Extraction
- **Chosen**: requests + BeautifulSoup
- **Rationale**: Reliable web content fetching and HTML parsing
- **Alternatives considered**: Scrapy, Selenium, Playwright

## Phase 1: Design & Contracts

### Data Model

#### Book Content Entity
- **url**: string - Source URL of the content
- **title**: string - Title of the document/chapter
- **content**: string - Extracted text content
- **metadata**: dict - Additional document metadata
- **created_at**: datetime - When content was indexed

#### Embeddings Entity
- **vector**: list[float] - Numerical embedding representation
- **content_id**: string - Reference to source content
- **metadata**: dict - Additional indexing metadata

#### Knowledge Base Entry
- **id**: string - Unique identifier for the entry
- **payload**: dict - Content and metadata
- **vector**: list[float] - Embedding vector

### API Contracts

#### Content Fetching Function
```
fetch_content(url: str) -> dict
```
- **Input**: URL string to fetch content from
- **Output**: Dictionary containing content and metadata
- **Errors**: NetworkError, ContentExtractionError

#### Text Chunking Function
```
chunk_text(content: str, max_chunk_size: int) -> list[str]
```
- **Input**: Content string and maximum chunk size
- **Output**: List of text chunks
- **Errors**: None

#### Embedding Generation Function
```
generate_embeddings(texts: list[str]) -> list[list[float]]
```
- **Input**: List of text chunks
- **Output**: List of embedding vectors
- **Errors**: EmbeddingGenerationError

#### Vector Storage Function
```
store_embeddings(entries: list[dict]) -> bool
```
- **Input**: List of knowledge base entries
- **Output**: Success status
- **Errors**: StorageError

### Quickstart Guide

1. **Setup Environment**:
   ```bash
   # Install UV (if not already installed)
   pip install uv

   # Create project directory
   mkdir rag-backend
   cd rag-backend
   ```

2. **Install Dependencies**:
   ```bash
   # Initialize project with UV
   uv init
   # Add required dependencies
   uv add cohere qdrant-client requests beautifulsoup4
   ```

3. **Configuration**:
   ```bash
   # Set environment variables
   export COHERE_API_KEY="your-cohere-api-key"
   export QDRANT_URL="your-qdrant-url"
   export QDRANT_API_KEY="your-qdrant-api-key"
   ```

4. **Run Indexing**:
   ```bash
   # Run the main script with book URLs
   python main.py --urls "https://example-book.com/chapter1" "https://example-book.com/chapter2"
   ```

## Phase 2: Implementation Approach

### Agent Context Update
- Note: `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude` was not run due to missing pwsh environment
- Agent context would have been updated with new technologies: Cohere, Qdrant, UV package manager, web scraping techniques

### System Design Functions

The main.py file will implement the following specific functions:

1. **get_all_urls(base_url: str) -> list[str]**
   - Purpose: Discover and return all book page URLs from the provided base URL
   - Input: Base URL of the deployed book website
   - Output: List of all accessible page URLs
   - Target URL: "https://ai-robotics-textbook.vercel.app/"
   - Sitemap URL: "https://ai-robotics-textbook.vercel.app/sitemap.xml"

2. **extract_text_from_url(url: str) -> dict**
   - Purpose: Extract clean text content from a given URL
   - Input: Single URL to extract content from
   - Output: Dictionary containing content, title, and metadata

3. **chunk_text(content: str, chunk_size: int = 1000, overlap: int = 200) -> list[dict]**
   - Purpose: Split content into manageable chunks with metadata
   - Input: Content string and chunking parameters
   - Output: List of chunk dictionaries with text and metadata

4. **embed(texts: list[str]) -> list[list[float]]**
   - Purpose: Generate embeddings for text chunks using Cohere
   - Input: List of text chunks
   - Output: List of embedding vectors

5. **create_collection(collection_name: str = "RAG_embedding") -> bool**
   - Purpose: Create or verify the existence of the Qdrant collection
   - Input: Name for the vector collection
   - Output: Success status

6. **save_chunk_to_qdrant(chunk_data: dict, vector: list[float]) -> bool**
   - Purpose: Store a single chunk with its embedding in Qdrant
   - Input: Chunk data with metadata and corresponding embedding vector
   - Output: Success status

7. **main() -> None**
   - Purpose: Execute the complete RAG pipeline
   - Process: Execute all functions in sequence to build the knowledge base

### Component Breakdown

1. **Configuration Management**:
   - Environment variable loading
   - API client initialization
   - Vector database setup

2. **Content Fetching Module**:
   - URL validation and fetching
   - HTML parsing and text extraction
   - Content cleaning utilities

3. **Text Processing Module**:
   - Chunking algorithms
   - Content preprocessing
   - Metadata extraction

4. **Embedding Generation Module**:
   - Cohere client integration
   - Batch processing of text chunks
   - Error handling for API calls

5. **Storage Module**:
   - Qdrant client integration
   - Vector upsert operations
   - Metadata management

6. **Orchestration Module**:
   - Main indexing workflow
   - Progress tracking
   - Error reporting

### Implementation Steps

1. Create the backend project structure
2. Set up UV package management
3. Implement configuration loading
4. Build content fetching and cleaning functions
5. Develop text chunking utilities
6. Integrate Cohere client for embeddings
7. Integrate Qdrant client for storage
8. Create main orchestration function
9. Add CLI interface
10. Write unit tests
11. Create documentation

## Risk Analysis

### High-Risk Areas
- **API Rate Limits**: Cohere and Qdrant may have rate limits that could affect large-scale indexing
- **Memory Usage**: Processing large documents may require significant memory
- **Network Reliability**: Content fetching depends on external website availability

### Mitigation Strategies
- Implement retry mechanisms with exponential backoff
- Add memory-efficient processing for large documents
- Include timeout and connection handling
- Add caching for previously processed content

## Success Criteria

- [x] Content successfully fetched from book URLs
- [x] Text properly extracted and cleaned
- [x] Embeddings generated using Cohere
- [x] Vectors stored in Qdrant with metadata
- [x] System handles errors gracefully
- [x] Performance meets requirements (process 100 pages in 30 minutes)