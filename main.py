from fastapi import FastAPI, Query, Response
import edge_tts
import asyncio
import uuid
import os

app = FastAPI()

@app.get("/speak")
async def speak(text: str = Query(..., min_length=1, max_length=1000)):
    voice = "te-IN-ShrutiNeural"
    filename = f"/tmp/{uuid.uuid4()}.mp3"

    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(filename)

        with open(filename, "rb") as f:
            audio_bytes = f.read()

        return Response(content=audio_bytes, media_type="audio/mpeg")

    finally:
        if os.path.exists(filename):
            os.remove(filename)
