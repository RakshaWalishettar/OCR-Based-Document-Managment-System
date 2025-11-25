# Dockerfile
FROM python:3.11-slim

# Install system deps for tesseract + poppler
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# use pip cache
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV STORAGE_DIR=/tmp/ocr_storage
RUN mkdir -p /tmp/ocr_storage

EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers"]
