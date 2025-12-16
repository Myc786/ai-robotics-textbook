from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import logging
from uuid import uuid4

from ...models.document import Document
from ...services.document_service import document_service
from ...core.database import get_db_session
from ...core.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)


from fastapi import Form

@router.post("/documents", summary="Upload and index a document")
async def upload_document(
    title: str = Form(...),
    content: str = Form(...),
    url: Optional[str] = Form(None),
    author: Optional[str] = Form(None),
    source_type: str = Form("book"),
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Upload and index a document for retrieval.

    This endpoint:
    1. Takes document content and metadata
    2. Processes the document (splits, embeds, stores)
    3. Makes it available for retrieval in the RAG system
    """
    try:
        logger.info(f"Received document upload request: {title}")

        # Process and store the document
        document_id = await document_service.process_and_store_document(
            title=title,
            content=content,
            url=url,
            author=author,
            source_type=source_type,
            db_session=db_session
        )

        logger.info(f"Document uploaded and indexed successfully: {document_id}")

        return {
            "document_id": document_id,
            "status": "indexed",
            "message": "Document uploaded and indexed successfully"
        }

    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the document: {str(e)}"
        )


@router.post("/documents/file", summary="Upload a document file")
async def upload_document_file(
    file: UploadFile = File(...),
    title: Optional[str] = None,
    url: Optional[str] = None,
    author: Optional[str] = None,
    source_type: str = "book",
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Upload a document file for processing and indexing.

    This endpoint:
    1. Accepts a file upload
    2. Extracts text content from the file (currently supports text files)
    3. Processes the document (splits, embeds, stores)
    4. Makes it available for retrieval in the RAG system
    """
    try:
        logger.info(f"Received document file upload: {file.filename}")

        # Read file content
        content = await file.read()
        content = content.decode('utf-8')  # For text files

        # Use filename as title if not provided
        if not title:
            title = file.filename

        # Process and store the document
        document_id = await document_service.process_and_store_document(
            title=title,
            content=content,
            url=url,
            author=author,
            source_type=source_type,
            db_session=db_session
        )

        logger.info(f"Document file uploaded and indexed successfully: {document_id}")

        return {
            "document_id": document_id,
            "status": "indexed",
            "message": "Document file uploaded and indexed successfully"
        }

    except UnicodeDecodeError:
        logger.error("Uploaded file is not a text file")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only text files are supported in this implementation"
        )
    except Exception as e:
        logger.error(f"Error uploading document file: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the document file: {str(e)}"
        )


@router.get("/documents/{document_id}", response_model=Document, summary="Get document information")
async def get_document(
    document_id: str,
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Retrieve information about a specific document.
    """
    try:
        logger.info(f"Retrieving document info: {document_id}")

        # TODO: Implement database lookup for document metadata
        # For now, we'll return a placeholder response
        # In a real implementation, you'd query the DocumentDB table

        # Placeholder response - in a real implementation, you'd fetch from the database
        return Document(
            id=document_id,
            title="Placeholder Title",
            source_type="book",
            status="indexed",
            total_chunks=0,
            indexed_chunks=0
        )

    except Exception as e:
        logger.error(f"Error retrieving document: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the document"
        )


@router.delete("/documents/{document_id}", summary="Delete a document")
async def delete_document(
    document_id: str,
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Delete a document and all its associated chunks from the system.
    """
    try:
        logger.info(f"Deleting document: {document_id}")

        # Delete the document from both vector store and database
        await document_service.delete_document(
            document_id=document_id,
            db_session=db_session
        )

        logger.info(f"Document deleted successfully: {document_id}")

        return {
            "document_id": document_id,
            "status": "deleted",
            "message": "Document and its chunks deleted successfully"
        }

    except Exception as e:
        logger.error(f"Error deleting document: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the document"
        )


@router.get("/documents", summary="List all documents")
async def list_documents(
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    List all indexed documents in the system.
    """
    try:
        logger.info("Retrieving list of all documents")

        # TODO: Implement database query to fetch all documents
        # For now, we'll return an empty list
        # In a real implementation, you'd query the DocumentDB table

        return {
            "documents": [],
            "count": 0
        }

    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the document list"
        )