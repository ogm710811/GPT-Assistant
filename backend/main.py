# uvicorn main:app
# uvicorn main:app --reload

# main imports
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai

# custom function imports
from functions.database import store_messages, reset_messages
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.text_to_speech import convert_text_to_speech, convert_text_to_speech

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


# check health
@app.get("/health")
async def check_health():
    return {"message": "healthy"}


# reset messages from database file
@app.get("/reset")
async def reset_messages_file():
    reset_messages()
    return {"message": "reset messages file successfully"}


# convert assistant response into audio
@app.get("/text_to_speech/")
async def get_text_to_speech():
    # get saved audio
    audio_input = open("voice.mp3", "rb")

    # decode audio
    message_decoded = convert_audio_to_text(audio_input)

    # guard: ensure message decoded
    if not message_decoded:
        return HTTPException(status_code=400, detail='Failed to decode audio file')

    # get ChatGPT response
    assistant_response = get_chat_response(message_decoded)

    # guard: ensure to get ChatGPT response
    if not assistant_response:
        return HTTPException(status_code=400, detail='Failed to get ChatGPT response')

    # store messages into database file
    store_messages(message_decoded, assistant_response)

    audio_chunk = convert_text_to_speech(assistant_response)

    return StreamingResponse(audio_chunk(), media_type="audio/mp3")
