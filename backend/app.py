from flask import Flask, render_template, request, redirect, session
import os
import requests
from ai import create_audio, generate_response

# TODO: Add webhook verification - https://docs.recall.ai/docs/real-time-transcription
# ngrok http --domain=emerging-clam-star.ngrok-free.app 8080

# TODO: Add cacheing for conversation

# TODO: Add interrupt feature

app = Flask(__name__)

WELCOME_MESSAGE = "Hey Matt! Thanks for letting me in to the zoom room! My name is Alloy. I am here to chat with you about, well, anything really! What would you like to chat about?"

MEETING_URL = "https://us04web.zoom.us/j/74246558055?pwd=JNv4BojyGnbCyalmbMVParURjQoCbk.1"

with_audio_payload = {
        "real_time_transcription": { "destination_url": "https://emerging-clam-star.ngrok-free.app/webhooks/transcription" },
        
        "transcription_options": { 
            "provider": "aws_transcribe",
            "aws_transcribe": {
              "language_code": "en-US" }
            },


        "chat": {
            "on_bot_join": { "send_to": "host",
                            "message": "Hello! I am Alloy, here to chat!" },
            "on_participant_join": { "exclude_host": True,
                                    "message": "hello",
                                     "matches": [] }
        },
        "meeting_url": MEETING_URL,
        "bot_name": "Recall Bot",
          "automatic_audio_output": {
            "in_call_recording": {
            "data": {
                "kind": "mp3",
                "b64_data": create_audio(WELCOME_MESSAGE)
            }}}
    }

#Recall routes
@app.route("/create-bot")
def create_bot():
    url = "https://us-west-2.recall.ai/api/v1/bot/"

    payload = with_audio_payload

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": '80dd33e842ce017fa774041c7f7f392f5bfd23d9'
    }

    response = requests.post(url, json=payload, headers=headers)
    
    return response.text


def send_audio_to_bot(text, bot_id): 
    url = f"https://us-west-2.recall.ai/api/v1/bot/{bot_id}/output_audio/"
    payload = { "kind": "mp3", "b64_data": create_audio(text) }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "a5538149ac200699e4d4c5a1e15ef70dbe4e44ea"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response

@app.route("/webhooks/transcription", methods=["GET", "POST"])
def webhook_handler():
    #listen for output (bot.status_change)
    #joining call, in waiting room, recording permission allowed, call_ended, done, joining_call

    request_body = request.get_json()
    event = request_body['event']
    if event == 'bot.status_change':
        print(f"{request_body['data']['status'][4:].replace('_', ' ').title()}...")


    #listen for real time transcription (bot.transcription)
    if event == 'bot.transcription':
        sentence = ' '.join(word['text'] for word in request_body["data"]["transcript"]["words"])
        bot_response = generate_response(sentence)
        print(bot_response)   
        send_audio_to_bot(bot_response, request_body["data"]["bot_id"])

    # output an mean image or happy image

    ...

    # listen for logs (bot.log)

    ...
    
    return "hello"
@app.route("/redirect")
def redirect(): 
    return "good"

app.run(host='127.0.0.1', port=8080) 


