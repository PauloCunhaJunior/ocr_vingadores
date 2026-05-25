# OCR API

API Python com Flask para extrair texto de imagens usando Tesseract OCR.

O projeto pode ser usado de duas formas:

- Pelo navegador, acessando uma pagina HTML para enviar a imagem.
- Pela API `/ocr`, enviando a imagem com `curl` ou outro cliente HTTP.

## Arquivos

- `texto_ocr.py`: aplicacao Flask com a tela HTML e a rota da API.
- `requirements.txt`: dependencias Python.
- `Dockerfile`: cria um container com Python, Tesseract OCR e idioma portugues.
- `OCR_IMAGENS/`: pasta local com imagens para teste.

## Rodar com Docker

Essa e a forma recomendada, porque nao precisa instalar o Tesseract diretamente no Windows.

No terminal, dentro da pasta do projeto:

```powershell
cd "C:\Users\paulo\Desktop\Visual Studio Code\OCR"
```

Crie a imagem Docker:

```powershell
docker build -t ocr-api .
```

Rode o container:

```powershell
docker run --rm -p 8000:8000 ocr-api
```

Quando aparecer algo como `Running on http://127.0.0.1:8000`, deixe esse terminal aberto.

## Acessar a tela HTML

Abra no navegador:

```text
http://127.0.0.1:8000/
```

Nessa tela, escolha uma imagem do computador e clique em `Extrair texto`.

Exemplo de imagem para escolher:

```text
OCR_IMAGENS\texto.jpeg
```

## Testar se a API esta ligada

Abra no navegador:

```text
http://127.0.0.1:8000/health
```

Resposta esperada:

```json
{"status":"ok"}
```

## Testar OCR pelo terminal

Com o container rodando, abra outro terminal na pasta do projeto e execute:

```powershell
curl.exe -X POST -F "image=@OCR_IMAGENS\texto.jpeg" http://127.0.0.1:8000/ocr
```

Outro exemplo:

```powershell
curl.exe -X POST -F "image=@OCR_IMAGENS\bola.png" http://127.0.0.1:8000/ocr
```

Resposta esperada:

```json
{"text":"texto encontrado na imagem"}
```

Se a imagem nao tiver texto, a resposta pode ser:

```json
{"text":""}
```

## Ver somente o texto no PowerShell

```powershell
(curl.exe -X POST -F "image=@OCR_IMAGENS\texto.jpeg" http://127.0.0.1:8000/ocr | ConvertFrom-Json).text
```

## Enviar URL de uma imagem

Tambem e possivel enviar uma URL no formato JSON:

```powershell
curl.exe -X POST `
  -H "Content-Type: application/json" `
  -d "{\"image_url\":\"https://example.com/imagem.png\"}" `
  http://127.0.0.1:8000/ocr
```

## Rodar localmente sem Docker

Para rodar sem Docker, e necessario instalar o programa Tesseract OCR no Windows, alem das dependencias Python.

Instale as dependencias:

```powershell
pip install -r requirements.txt
```

Execute:

```powershell
python texto_ocr.py
```

Se aparecer o erro `tesseract is not installed or it's not in your PATH`, use Docker ou instale o Tesseract OCR no Windows.

## Parar o servidor

No terminal onde o servidor esta rodando, pressione:

```text
Ctrl+C
```
