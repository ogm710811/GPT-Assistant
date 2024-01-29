import openai
from decouple import config

# import custom functions
from functions.database import get_recent_messages

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


# open ChatGPT
# get response to our message
def get_chat_response(message_input):
    messages = get_recent_messages()
    user_message = {"role": "user", "content": message_input + " Only say two or 3 words in Spanish if speaking in "
                                                               "Spanish. The remaining words should be in English"}
    messages.append(user_message)

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        assistant_message_content = response.choices[0].message.content
        return assistant_message_content

    except Exception as e:
        print(e)
        return
