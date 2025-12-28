from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.health import router as health_router
from src.api.chat import router as chat_router
from src.config.database import qdrant_db, postgres_db
from src.config.settings import settings
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        await postgres_db.connect()
        await postgres_db.initialize_schema()
        print("PostgreSQL connected successfully")
    except Exception as e:
        print(f"Warning: PostgreSQL connection failed: {e}")
        print("Backend will run without database logging")

    try:
        qdrant_db.initialize_collection()
        print("Qdrant connected successfully")
    except Exception as e:
        print(f"Warning: Qdrant connection failed: {e}")
        print("Backend will run with limited retrieval capabilities")

    yield

    # Shutdown
    try:
        await postgres_db.disconnect()
    except Exception:
        pass


app = FastAPI(
    title="Book-Authored RAG Chatbot API",
    description="A RAG system that provides book-authoritative answers with zero hallucinations",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # Local Docusaurus dev server
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "https://ai-robotics-textbook.vercel.app",  # Production Vercel URL
        "https://*.vercel.app",       # All Vercel preview deployments
        "https://*.hf.space",         # Hugging Face Spaces
        "https://*.github.io",        # GitHub Pages
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(health_router, prefix="/api/v1", tags=["health"])
app.include_router(chat_router, prefix="/api/v1", tags=["chat"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Book-Authored RAG Chatbot API"}