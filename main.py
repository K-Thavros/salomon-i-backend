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
