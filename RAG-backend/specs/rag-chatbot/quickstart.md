# Quickstart: RAG Chatbot Development

## Prerequisites

- Python 3.11+
- pip package manager
- Git
- Access to Cohere API key
- Access to Qdrant Cloud (Free Tier) API key and URL
- Access to Neon Serverless Postgres connection details

## Environment Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd RAG-Backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables by creating a `.env` file:
```env
# API Keys
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_URL=your_qdrant_cloud_url_here

# Database
DATABASE_URL=postgresql://username:password@ep-xxxxxx.us-east-1.aws.neon.tech/dbname

# Application
ENVIRONMENT=development
LOG_LEVEL=INFO
```

## Initial Project Structure

The project follows a modular architecture:

```
backend/
├── src/
│   ├── models/          # Data models and schemas
│   ├── services/        # Business logic and service layers
│   ├── api/            # API endpoints and routes
│   ├── core/           # Configuration and core utilities
│   └── utils/          # Helper functions and utilities
├── tests/              # Test files
├── requirements.txt    # Python dependencies
└── alembic/            # Database migrations
```

## Running the Application

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables by creating a `.env` file:
```env
# API Keys
COHERE_API_KEY=your_cohere_api_key_here
OPENAI_API_KEY=your_openai_api_key_here  # Optional, for enhanced responses
QDRANT_URL=your_qdrant_cloud_url_here
QDRANT_API_KEY=your_qdrant_api_key_here

# Database
DATABASE_URL=postgresql://username:password@ep-xxxxxx.us-east-1.aws.neon.tech/dbname

# Application
ENVIRONMENT=development
LOG_LEVEL=INFO
```

3. Run database migrations:
```bash
alembic upgrade head
```

4. Start the development server:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at `http://localhost:8000`

5. Access the API documentation at `http://localhost:8000/docs`

## Key Development Commands

### Testing
```bash
# Run all tests (requires TESTING=1 environment variable)
TESTING=1 python -m pytest

# Run tests with coverage
TESTING=1 python -m pytest --cov=src

# Run specific test file
TESTING=1 python -m pytest tests/unit/test_retrieval_service.py

# Run only unit tests
TESTING=1 python -m pytest tests/unit/
```

### Database Migrations
```bash
# Generate a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Downgrade migrations
alembic downgrade -1
```

### Code Quality
```bash
# Run linting
flake8 src

# Run type checking
mypy src

# Format code
black src
```

## API Endpoints

### Chat Endpoint
- **POST** `/api/v1/chat`
- Accepts query with optional selected text
- Returns grounded response with source attribution

Example request:
```json
{
  "query": "What are the key principles of RAG systems?",
  "selected_text": "Optional text to constrain search",
  "top_k": 5,
  "similarity_threshold": 0.5,
  "search_scope": "full_book"
}
```

### Document Management
- **POST** `/api/v1/documents` - Upload and index documents
- **GET** `/api/v1/documents/{document_id}` - Get document info
- **DELETE** `/api/v1/documents/{document_id}` - Delete document and chunks

## Configuration

### Environment Variables
- `ENVIRONMENT`: Application environment (development, staging, production)
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `COHERE_API_KEY`: Cohere API key for embeddings
- `QDRANT_URL`: Qdrant Cloud instance URL
- `QDRANT_API_KEY`: Qdrant Cloud API key
- `DATABASE_URL`: Postgres database connection string
- `EMBEDDING_MODEL`: Cohere model to use for embeddings (default: multilingual-light-v2.0)
- `DEFAULT_TOP_K`: Default number of chunks to retrieve (default: 5)
- `DEFAULT_SIMILARITY_THRESHOLD`: Default similarity threshold (default: 0.5)

### Application Settings
Configuration is managed through `src/core/config.py` using Pydantic settings:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    environment: str = "development"
    log_level: str = "INFO"
    cohere_api_key: str
    qdrant_url: str
    qdrant_api_key: str
    database_url: str
    embedding_model: str = "multilingual-light-v2.0"
    default_top_k: int = 5
    default_similarity_threshold: float = 0.5
```

## Development Workflow

1. **Feature Development**:
   - Create a new branch: `git checkout -b feature/your-feature-name`
   - Implement your changes following the architecture
   - Write tests for new functionality
   - Run tests: `pytest`
   - Commit changes with descriptive messages
   - Push and create a pull request

2. **Testing Strategy**:
   - Unit tests for individual functions/classes
   - Integration tests for service interactions
   - End-to-end tests for complete workflows
   - Mock external services (Cohere, Qdrant) for faster local testing

3. **Code Review**:
   - Ensure adherence to project constitution (retrieval-first, zero hallucination)
   - Verify proper error handling and logging
   - Check for security considerations
   - Confirm performance implications are acceptable

## Common Development Tasks

### Adding a New API Endpoint
1. Define the request/response models in `src/models/`
2. Implement the service logic in `src/services/`
3. Create the endpoint in the appropriate file in `src/api/v1/`
4. Add tests in `tests/`
5. Update documentation if needed

### Adding a New Database Model
1. Define the SQLAlchemy model in `src/models/`
2. Create the corresponding Pydantic schema
3. Generate and apply database migration
4. Update services to use the new model
5. Add tests for the new functionality

### Implementing a New Service
1. Create the service file in `src/services/`
2. Define the service interface and implementation
3. Add dependency injection if needed
4. Write unit tests for the service
5. Integrate with API endpoints as needed