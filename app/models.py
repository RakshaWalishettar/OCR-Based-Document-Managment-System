# app/models.py
from pydantic import BaseModel
from typing import Optional

class UploadResponse(BaseModel):
    id: str
    filename: str
    text: Optional[str] = None
    url: Optional[str] = None

class OCRRequest(BaseModel):
    file_url: Optional[str] = None
