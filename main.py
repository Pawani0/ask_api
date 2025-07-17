from fastapi import FastAPI, Form
from query_handler import get_answer
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import edge_tts
import io
import asyncio
import urllib.parse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["*"] for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Answer"],
)

class QueryRequest(BaseModel):
    question: str

async def generate_tts_stream(text):
    communicate = edge_tts.Communicate(text, "en-IN-NeerjaNeural")
    mp3_data = io.BytesIO()
    
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            mp3_data.write(chunk["data"])
    
    mp3_data.seek(0)
    return mp3_data

@app.get("/ask/")
async def speak(text: str):
    response = get_answer(text)
    mp3_stream = await generate_tts_stream(response)
    return StreamingResponse(mp3_stream, media_type="audio/mpeg",headers={"X-Answer": urllib.parse.quote(response)})
