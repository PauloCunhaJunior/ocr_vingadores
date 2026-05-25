FROM python:3.12-alpine

RUN apk add --no-cache \
    tesseract-ocr \
    tesseract-ocr-data-por

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY texto_ocr.py .

EXPOSE 8000
CMD ["python", "texto_ocr.py"]
