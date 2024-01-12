# uvicorn main:app
# uvicorn main:app --reload

# main imports
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai

# custom function imports
from functions.openai_requests import convert_audio_to_text

# app initialization
app = FastAPI()

# CORS - origins
origins = [
    "http://localhost:5173",
    "http://localhost:5174"
    "http://localhost:4173"
    "http://localhost:4174"
    "http://localhost:3000"
]

# CORS - middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# CORSMiddleware(
#     app,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

# check health
@app.get("/health")
async def check_health():
    return {"message": "healthy"}


# get audio
@app.get("/post-audio-get/")
async def get_audio():
    # get saved audio
    audio_input = open("voice.mp3", "rb")

    # decode audio
    message_decoded = convert_audio_to_text(audio_input)
    print(message_decoded)
    return "Done"

