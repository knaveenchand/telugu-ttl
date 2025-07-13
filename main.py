from fastapi import FastAPI, HTTPException, Response, Request
from pydantic import BaseModel
from typing import Optional
import edge_tts
import uuid
import os

app = FastAPI()

API_SECRET_KEY = os.getenv("API_SECRET_KEY", "invalid")

class PublicSpeakRequest(BaseModel):
    text: str
    voice: Optional[str] = "te-IN-ShrutiNeural"

@app.post("/proxy-speak")
async def proxy_speak(data: PublicSpeakRequest):
    if not data.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    voice = data.voice or "te-IN-ShrutiNeural"
    filename = f"/tmp/{uuid.uuid4()}.mp3"

    try:
        communicate = edge_tts.Communicate(data.text, voice)
        await communicate.save(filename)

        with open(filename, "rb") as f:
            audio_bytes = f.read()

        return Response(content=audio_bytes, media_type="audio/mpeg")

    finally:
        if os.path.exists(filename):
            os.remove(filename)
