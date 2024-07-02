from pathlib import Path
from openai import OpenAI
import base64
import os


def create_audio(text):
  client = OpenAI(api_key="sk-proj-q6BSzVRt5SiFl9u1O57oT3BlbkFJ3sjkvfOiMnj32W4fxQgN")

  response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=text
  )

  binary = response.read()
  base64_encoded_data = base64.b64encode(binary)

  return base64_encoded_data.decode('utf-8')
# response.stream_to_file("output.mp3")

def generate_response(text):
    client = OpenAI(api_key="sk-proj-q6BSzVRt5SiFl9u1O57oT3BlbkFJ3sjkvfOiMnj32W4fxQgN")

    response = client.chat.completions.create(
       model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are acting as a helpful friend, who responds to the user and then usually asks a question. Be supportive and ask personal questions when it seems appropriate."},
    {"role": "user", "content": text},
  ]
    )
    return response.choices[0].message.content

