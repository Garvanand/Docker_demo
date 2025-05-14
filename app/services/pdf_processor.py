import io
import json
from pathlib import Path
from typing import Dict, List, Optional, Union
import PyPDF2
import pytesseract
from pdf2image import convert_from_bytes
import camelot
import cv2
import numpy as np
from PIL import Image
import structlog
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential

from ..config import settings
from ..models.schemas import (
    TextExtractionResult,
    TableExtractionResult,
    ImageExtractionResult,
    MetadataResult,
    ProcessingResponse
)

logger = structlog.get_logger()

class PDFProcessor:
    def __init__(self):
        self.storage_dir = settings.STORAGE_DIR
        self.storage_dir.mkdir(exist_ok=True)
        pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def extract_text(self, pdf_content: bytes) -> TextExtractionResult:
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return TextExtractionResult(
                text=text,
                pages=len(pdf_reader.pages),
                extraction_method="PyPDF2"
            )
        except Exception as e:
            logger.error("text_extraction_failed", error=str(e))
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def extract_text_with_ocr(self, pdf_content: bytes) -> TextExtractionResult:
        try:
            images = convert_from_bytes(pdf_content)
            text = ""
            
            for image in images:
                opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
                thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                
                text += pytesseract.image_to_string(
                    thresh,
                    lang=settings.OCR_LANG,
                    config='--psm 3'
                ) + "\n"
            
            return TextExtractionResult(
                text=text,
                pages=len(images),
                extraction_method="OCR"
            )
        except Exception as e:
            logger.error("ocr_extraction_failed", error=str(e))
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def extract_tables(self, pdf_content: bytes) -> List[TableExtractionResult]:
        try:
            temp_path = self.storage_dir / f"temp_{datetime.now().timestamp()}.pdf"
            with open(temp_path, "wb") as f:
                f.write(pdf_content)
            
            tables = camelot.read_pdf(str(temp_path), pages='all')
            
            result = []
            for i, table in enumerate(tables):
                result.append(TableExtractionResult(
                    table_number=i + 1,
                    page=table.page,
                    data=table.df.to_dict(orient='records'),
                    accuracy=table.accuracy
                ))
            
            temp_path.unlink()
            return result
        except Exception as e:
            logger.error("table_extraction_failed", error=str(e))
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def extract_images(self, pdf_content: bytes) -> List[ImageExtractionResult]:
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
            images = []
            
            for page_num, page in enumerate(pdf_reader.pages):
                if '/XObject' in page['/Resources']:
                    x_objects = page['/Resources']['/XObject'].get_object()
                    
                    for obj in x_objects:
                        if x_objects[obj]['/Subtype'] == '/Image':
                            image = x_objects[obj]
                            image_data = image.get_data()
                            
                            image_path = self.storage_dir / f"image_{page_num}_{len(images)}.png"
                            with open(image_path, "wb") as f:
                                f.write(image_data)
                            
                            images.append(ImageExtractionResult(
                                page=page_num + 1,
                                path=str(image_path),
                                size=len(image_data)
                            ))
            
            return images
        except Exception as e:
            logger.error("image_extraction_failed", error=str(e))
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def extract_metadata(self, pdf_content: bytes) -> MetadataResult:
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
            info = pdf_reader.metadata
            
            return MetadataResult(
                title=info.get('/Title', ''),
                author=info.get('/Author', ''),
                subject=info.get('/Subject', ''),
                creator=info.get('/Creator', ''),
                producer=info.get('/Producer', ''),
                creation_date=info.get('/CreationDate', ''),
                modification_date=info.get('/ModDate', ''),
                pages=len(pdf_reader.pages),
                encrypted=pdf_reader.is_encrypted
            )
        except Exception as e:
            logger.error("metadata_extraction_failed", error=str(e))
            raise

    def process_pdf(self, pdf_content: bytes, filename: str) -> ProcessingResponse:
        try:
            text_result = self.extract_text(pdf_content)
            ocr_result = self.extract_text_with_ocr(pdf_content)
            tables = self.extract_tables(pdf_content)
            images = self.extract_images(pdf_content)
            metadata = self.extract_metadata(pdf_content)
            
            result = ProcessingResponse(
                message="PDF processed successfully",
                filename=filename,
                text_extraction=text_result,
                ocr_extraction=ocr_result,
                tables=tables,
                images=images,
                metadata=metadata,
                download_url=f"/download/{filename}_results.json"
            )
            
            output_path = self.storage_dir / f"{filename}_results.json"
            with open(output_path, "w") as f:
                json.dump(result.model_dump(), f, indent=2, default=str)
            
            return result
        except Exception as e:
            logger.error("pdf_processing_failed", error=str(e))
            raise 