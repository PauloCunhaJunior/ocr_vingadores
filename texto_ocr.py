from flask import Flask, request, jsonify, render_template_string
import os
from PIL import Image
from pathlib import Path
import pytesseract
import requests
from io import BytesIO

app = Flask(__name__)

SUPPORTED_LANG = "por"
TESSERACT_PATHS = (
    Path(os.environ["TESSERACT_CMD"]) if os.environ.get("TESSERACT_CMD") else None,
    Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe"),
    Path(r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"),
)

for tesseract_path in TESSERACT_PATHS:
    if tesseract_path and tesseract_path.exists():
        pytesseract.pytesseract.tesseract_cmd = str(tesseract_path)
        break

PAGE_TEMPLATE = """
<!doctype html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>OCR Tesseract</title>
    <style>
        body {
            max-width: 820px;
            margin: 40px auto;
            padding: 0 20px;
            font-family: Arial, sans-serif;
            background: #f6f7f9;
            color: #1f2937;
        }

        main {
            background: white;
            border: 1px solid #d7dce2;
            border-radius: 8px;
            padding: 24px;
        }

        h1 {
            margin-top: 0;
        }

        form {
            display: flex;
            gap: 12px;
            align-items: center;
            flex-wrap: wrap;
            margin-bottom: 24px;
        }

        button {
            border: 0;
            border-radius: 6px;
            padding: 10px 16px;
            background: #2563eb;
            color: white;
            cursor: pointer;
        }

        pre {
            white-space: pre-wrap;
            overflow-wrap: anywhere;
            min-height: 140px;
            padding: 16px;
            border: 1px solid #d7dce2;
            border-radius: 6px;
            background: #f9fafb;
            font-size: 16px;
            line-height: 1.5;
        }

        .error {
            color: #b91c1c;
            font-weight: 700;
        }
    </style>
</head>
<body>
    <main>
        <h1>OCR Tesseract</h1>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="image" accept="image/*" required>
            <button type="submit">Extrair texto</button>
        </form>

        {% if error %}
            <p class="error">{{ error }}</p>
        {% endif %}

        {% if text is not none %}
            <h2>Texto extraido</h2>
            <pre>{{ text or "Nenhum texto encontrado na imagem." }}</pre>
        {% endif %}
    </main>
</body>
</html>
"""


def extract_text(image: Image.Image) -> str:
    return pytesseract.image_to_string(image, lang=SUPPORTED_LANG)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template_string(PAGE_TEMPLATE, text=None, error=None)

    if "image" not in request.files:
        return render_template_string(
            PAGE_TEMPLATE,
            text=None,
            error="Escolha uma imagem para processar.",
        ), 400

    try:
        file = request.files["image"]
        image = Image.open(file.stream).convert("RGB")
        text = extract_text(image).strip()
        return render_template_string(PAGE_TEMPLATE, text=text, error=None)
    except Exception as exc:
        return render_template_string(
            PAGE_TEMPLATE,
            text=None,
            error=f"Falha ao processar OCR: {exc}",
        ), 500


@app.route("/ocr", methods=["POST"])
def ocr():
    image = None

    if "image" in request.files:
        file = request.files["image"]
        image = Image.open(file.stream).convert("RGB")
    elif request.is_json:
        payload = request.get_json(silent=True)
        if not payload or "image_url" not in payload:
            return jsonify({"error": "JSON deve conter a chave image_url"}), 400

        image_url = payload["image_url"]
        try:
            response = requests.get(image_url, timeout=20)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content)).convert("RGB")
        except requests.RequestException as exc:
            return jsonify({"error": f"Falha ao baixar imagem: {exc}"}), 400
    else:
        return jsonify({"error": "Envie o arquivo em multipart/form-data com a chave image ou JSON com image_url."}), 400

    try:
        text = extract_text(image).strip()
        return jsonify({"text": text})
    except Exception as exc:
        return jsonify({"error": f"Falha ao processar OCR: {exc}"}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
