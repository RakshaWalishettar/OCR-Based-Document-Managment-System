# app/storage.py
import os
import uuid
from pathlib import Path
from typing import Tuple

STORAGE_DIR = os.environ.get("STORAGE_DIR", "/tmp/ocr_storage")
Path(STORAGE_DIR).mkdir(parents=True, exist_ok=True)

def save_file(file_bytes: bytes, filename: str) -> Tuple[str, str]:
    """
    Save file locally and return (id, path)
    """
    file_id = str(uuid.uuid4())
    ext = Path(filename).suffix or ".bin"
    out_name = f"{file_id}{ext}"
    out_path = Path(STORAGE_DIR) / out_name
    with open(out_path, "wb") as f:
        f.write(file_bytes)
    return file_id, str(out_path)

def get_file_path(file_id_with_ext: str) -> str:
    p = Path(STORAGE_DIR) / file_id_with_ext
    if p.exists():
        return str(p)
    raise FileNotFoundError("File not found")
