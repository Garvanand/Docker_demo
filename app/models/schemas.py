from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union
from datetime import datetime

class TextExtractionResult(BaseModel):
    text: str
    pages: int
    extraction_method: str

class TableExtractionResult(BaseModel):
    table_number: int
    page: int
    data: List[Dict]
    accuracy: float

class ImageExtractionResult(BaseModel):
    page: int
    path: str
    size: int

class MetadataResult(BaseModel):
    title: str = ""
    author: str = ""
    subject: str = ""
    creator: str = ""
    producer: str = ""
    creation_date: str = ""
    modification_date: str = ""
    pages: int
    encrypted: bool

class ProcessingResponse(BaseModel):
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    filename: Optional[str] = None
    text_extraction: Optional[TextExtractionResult] = None
    ocr_extraction: Optional[TextExtractionResult] = None
    tables: Optional[List[TableExtractionResult]] = None
    images: Optional[List[ImageExtractionResult]] = None
    metadata: Optional[MetadataResult] = None
    download_url: Optional[str] = None

class ErrorResponse(BaseModel):
    detail: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    error_code: Optional[str] = None 