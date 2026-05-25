# OCR API

API Python para extrair texto de imagens usando Tesseract OCR.

## Arquivos

- `texto_ocr.py`: aplicação Flask que expõe a rota `/ocr`
- `requirements.txt`: dependências Python
- `Dockerfile`: containeriza a aplicação com Tesseract instalado

## Usar localmente

1. Instale dependências:

```bash
pip install -r requirements.txt
```

2. Execute:

```bash
python texto_ocr.py
```

3. Envie imagem via `curl`:

```bash
curl -X POST -F "image=@/caminho/para/imagem.png" http://127.0.0.1:8000/ocr
```

## Usar via URL de imagem

```bash
curl -X POST -H "Content-Type: application/json" -d '{"image_url":"https://example.com/image.png"}' http://127.0.0.1:8000/ocr
```

## Docker

```bash
docker build -t ocr-api .
docker run -p 8000:8000 ocr-api
```
