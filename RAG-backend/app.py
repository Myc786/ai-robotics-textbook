"""
Hugging Face Spaces entry point for the RAG Chatbot API.
This file is specifically for HF Spaces deployment which requires app.py at root.
"""
import uvicorn
import os

# Set default port for HF Spaces (7860)
os.environ.setdefault("PORT", "7860")

from src.api.main import app

# For HF Spaces, the app object needs to be importable
# HF Spaces will run: uvicorn app:app --host 0.0.0.0 --port 7860

if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))
    host = os.getenv("HOST", "0.0.0.0")

    uvicorn.run(
        "src.api.main:app",
        host=host,
        port=port,
        reload=False,  # Disable reload in production
        log_level="info"
    )
