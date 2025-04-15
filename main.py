from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/")
async def verify(request: Request):
    body = await request.json()
    challenge = body.get("challenge")

    if challenge:
        return JSONResponse(content={"challenge": challenge})
    return {"error": "No se recibió challenge"}
