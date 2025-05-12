from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class HealthResponse(BaseModel):
    status: str
    message: str

class Item(BaseModel):
    id: int
    name: str

class ItemsResponse(BaseModel):
    items: List[Item]

@router.get('/health', response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status='healthy',
        message='Garv API is running'
    )

@router.get('/items', response_model=ItemsResponse)
async def get_items():
    """Sample endpoint to demonstrate API functionality"""
    return ItemsResponse(
        items=[
            Item(id=1, name='Garv Anand'),
            Item(id=2, name='Garv Projects'),
            Item(id=3, name='Garv Docker Demo')
        ]
    ) 