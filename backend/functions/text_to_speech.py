import requests
import os
from decouple import config

ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")


# eleven labs
# convert text to speech
# saved speech respond in text_to_audio dir
def convert_text_to_speech(assistant_message):
    url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"

    payload = {
        "model_id": "eleven_monolingual_v1",
        "text": assistant_message,
        "voice_settings": {
            "similarity_boost": 0.5,
            "stability": 0.5
        }
    }
    headers = {
        "xi-api-key": ELEVEN_LABS_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.request("POST", url, json=payload, headers=headers)
        try:
            os.remove('./text_to_audio/output.mp3')
        except FileNotFoundError:
            print('File does not exist')
    except Exception as e:
        print(e)
        return

    if response.status_code == 200:
        with open('./text_to_audio/output.mp3', 'wb') as f:
            for chunk in response.iter_content():
                if chunk:
                    f.write(chunk)

        def iterfile():
            with open('text_to_audio/output.mp3', "rb") as f:
                yield from f

        return iterfile
    else:
        return
