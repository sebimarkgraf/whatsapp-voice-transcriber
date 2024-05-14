from fastapi import FastAPI, UploadFile, File

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "UP"}


@app.post("/transcribe")
async def transcribe(voice_message: UploadFile):
    if not voice_message.content_type.startswith("audio"):
        raise HTTPException(status_code=400, detail="File must be an audio file")
    return {"transcription": "Hello World"}
