from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.core.logger import setup_logger

# Set up logging
logger = setup_logger()

# Create FastAPI app instance
app = FastAPI(
    title="RAG Chatbot API",
    description="A Retrieval-Augmented Generation chatbot that answers questions based on book content",
    version="0.1.0",
    openapi_tags=[
        {
            "name": "chat",
            "description": "Chat and conversation endpoints"
        },
        {
            "name": "documents",
            "description": "Document management endpoints"
        }
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "RAG Chatbot API", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "environment": settings.environment}

# Include API routes
def include_routers():
    try:
        from src.api.v1.chat import router as chat_router
        from src.api.v1.documents import router as documents_router

        app.include_router(chat_router, prefix="/api/v1", tags=["chat"])
        app.include_router(documents_router, prefix="/api/v1", tags=["documents"])
    except ImportError:
        # Routers will be included when they are created
        pass

# Include routers
include_routers()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.environment == "development" else False
    )