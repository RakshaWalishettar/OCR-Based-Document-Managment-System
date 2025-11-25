# app/auth.py
# Placeholder auth dependency. Replace with real auth (JWT/OAuth/etc.)
from fastapi import Header, HTTPException, Depends

def fake_api_key(x_api_key: str = Header(None)):
    if x_api_key != "dev-key":
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return True

