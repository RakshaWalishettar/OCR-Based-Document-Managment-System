# app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.responses import HTMLResponse, FileResponse
import uuid
import os
from pathlib import Path

from .ocr import extract_text_generic
from .storage import save_file, get_file_path, STORAGE_DIR
from .models import UploadResponse
from .logging_setup import setup_logging
from .monitoring import Timer
from .auth import fake_api_key

logger = setup_logging()
app = FastAPI(title="OCR Document Management")

@app.get("/", response_class=HTMLResponse)
def home():
    html = Path(__file__).parent.parent.joinpath("frontend/index.html").read_text()
    return HTMLResponse(content=html)

@app.post("/upload", response_model=UploadResponse, dependencies=[Depends(fake_api_key)])
async def upload_file(file: UploadFile = File(...)):
    logger.info("Received upload: %s", file.filename)
    content = await file.read()
    file_id, saved_path = save_file(content, file.filename)
    try:
        with Timer() as t:
            text = extract_text_generic(saved_path)
        logger.info("OCR done in %.2fs", t.elapsed)
    except Exception as e:
        logger.exception("OCR failed: %s", e)
        text = None
    url_name = f"{file_id}{Path(file.filename).suffix}"
    # Return url as a local download path (the GET below expects id+ext)
    return UploadResponse(id=file_id, filename=file.filename, text=text, url=url_name)

@app.get("/download/{file_name}")
def download(file_name: str):
    """
    file_name is expected to be '<uuid>.<ext>' saved earlier.
    """
    try:
        path = get_file_path(file_name)
        return FileResponse(path, filename=file_name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

@app.get("/health")
def health():
    return {"status": "ok"}
