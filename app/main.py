import os
from fastapi import FastAPI, HTTPException, File, UploadFile, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
from gtts import gTTS
from datetime import datetime
from extract_webpage import router as extract_router


class TTSRequest(BaseModel):
    transcript: str
    lang: str = 'en'
    slow: bool = False

app = FastAPI(title="TTS Server", version="1.0", description="A simple Text-to-Speech API server.")
app.mount("/audio_files", StaticFiles(directory="audio_files"), name="audio_files")
app.include_router(extract_router)

@app.post("/convert")
async def convert_text_to_speech(request: TTSRequest):
    """
    Receives a transcript and optional voice and effects parameters,
    converts the text to speech using Google Text-to-Speech API, 
    and returns the path to the audio file.
    """
    try:
        # Create gTTS object
        tts = gTTS(text=request.transcript, lang=request.lang, slow=request.slow)

        # Create directory if it doesn't exist
        if not os.path.exists('audio_files'):
            os.makedirs('audio_files')

        # Generate a unique name for the audio file using the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        audio_file_name = f"audio_{timestamp}.mp3"

        # Save the audio file in the specified directory
        audio_file_path = os.path.join('audio_files', audio_file_name)
        tts.save(audio_file_path)


        # Construct the URL for the audio file
        audio_file_url = f"http://localhost:8000/{audio_file_path}"

        return {"message": "Conversion successful.", "audio_file_url": audio_file_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_root():
    """
    Root endpoint for basic API health check.
    """
    return {"message": "TTS Server is running."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)