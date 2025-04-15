from fastapi import FastAPI, Request, Header
from fastapi.responses import JSONResponse
import os

app = FastAPI()

NOTION_SECRET = os.getenv("NOTION_SECRET")

@app.post("/")
async def verify(request: Request, notion_secret: str = Header(None)):
    if notion_secret != NOTION_SECRET:
        return {"error": "Token de verificación no válido"}

    body = await request.json()
    challenge = body.get("challenge")

    if challenge:
        return JSONResponse(content={"challenge": challenge})
    return {"error": "No se recibió challenge"}
