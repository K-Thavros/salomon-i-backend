from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os

app = FastAPI()

NOTION_SECRET = os.getenv("NOTION_SECRET")

@app.post("/")
async def verify(request: Request):
    body = await request.json()
    challenge = body.get("challenge")
    token_recibido = body.get("verification_token")
    print("🔐 TOKEN RECIBIDO DESDE NOTION:", token_recibido)

    if token_recibido != NOTION_SECRET:
        return {"error": "Token de verificación no válido"}

    if challenge:
        return JSONResponse(content={"challenge": challenge})
    return {"error": "No se recibió challenge"}
import requests

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# 🧾 LECTURA de Bitácora
@app.get("/bitacora")
async def leer_bitacora():
    url = f"https://api.notion.com/v1/blocks/{PAGE_ID}/children"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return {"error": response.text}

# ✍️ ESCRITURA en Notion
@app.post("/escribir")
async def escribir(request: Request):
    data = await request.json()
    mensaje = data.get("mensaje")
    if not mensaje:
        return {"error": "No se recibió mensaje"}

    payload = {
        "parent": {"page_id": PAGE_ID},
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": mensaje}
                        }
                    ]
                }
            }
        ]
    }

    response = requests.patch(
        f"https://api.notion.com/v1/blocks/{PAGE_ID}/children",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return {"status": "✅ Escrito correctamente"}
    return {"status": "❌ Error", "detalle": response.text}
