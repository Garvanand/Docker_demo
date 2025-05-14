from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from datetime import datetime
import structlog
from pathlib import Path
import magic
import aiofiles
import os
import json

from .config import settings
from .services.pdf_processor import PDFProcessor
from .models.schemas import ProcessingResponse, ErrorResponse

logger = structlog.get_logger()
app = FastAPI(title=settings.PROJECT_NAME)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize PDF processor
pdf_processor = PDFProcessor()

# Custom JSON encoder for datetime objects
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/v1/process-pdf", response_model=ProcessingResponse)
async def process_pdf(file: UploadFile = File(...)):
    try:
        # Validate file size
        content = await file.read()
        if len(content) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File size exceeds maximum limit of {settings.MAX_UPLOAD_SIZE // (1024*1024)}MB"
            )
        
        # Validate file type
        mime_type = magic.from_buffer(content, mime=True)
        if mime_type != 'application/pdf':
            raise HTTPException(
                status_code=415,
                detail=f"Invalid file type. Expected PDF, got {mime_type}"
            )
        
        # Process PDF
        result = pdf_processor.process_pdf(content, file.filename)
        return result
    
    except Exception as e:
        logger.error("pdf_processing_error", error=str(e))
        error_response = ErrorResponse(
            detail=str(e),
            error_code="PDF_PROCESSING_ERROR"
        )
        return JSONResponse(
            status_code=500,
            content=json.loads(
                json.dumps(error_response.model_dump(), cls=DateTimeEncoder)
            )
        )

@app.get("/api/v1/download/{filename}")
async def download_results(filename: str):
    file_path = settings.STORAGE_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Results not found")
    return FileResponse(str(file_path)) 