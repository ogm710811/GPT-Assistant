import openai
from decouple import config

# retrieve env variables
openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPENAI_API_KEY")


# open AI - whisper
# convert audio  to text
def convert_audio_to_text(audio_file):
    try:
        transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        return transcript
    except Exception as e:
        print(e)
        return
