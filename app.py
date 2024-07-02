from flask import Flask, request
import requests
from ai import create_audio, generate_response, initialize_memory

# TODO: Add webhook verification - https://docs.recall.ai/docs/real-time-transcription
# TODO: Delete keys
# TODO: Add requirements.txt

# ngrok http --domain=emerging-clam-star.ngrok-free.app 8080

app = Flask(__name__) # Initialize Flask backend

RECALL_KEY="YOUR RECALL KEY"  # Input your Recall key here https://api.recall.ai/dashboard/apikeys/

WELCOME_MESSAGE = "Hey! Thanks for letting me into the zoom call. My name is Recally, I'm here to chat about, well, anything! What's on your mind?"

INVITE_LINK = "https://us04web.zoom.us/j/78045732635?pwd=aPS7s27RmqBWBP1FSRpcNVSDza56Pb.1"

NGROK_BASE_URL = "YOUR NGROK URL"  # https://ngrok.com/

WEBHOOK_URL = f"https://{NGROK_BASE_URL}/webhooks/transcription"



def get_bot_payload():
    """
    Generates and returns the payload configuration to create a Recall bot used in real-time transcription.

    The payload includes:
    - Real-time transcription settings
    - Transcription options and provider settings
    - Chat message settings for when the bot joins
    - Meeting URL for the bot to join
    - Bot's name
    - Automatic audio output settings for in-call recording

    Returns:
        dict: A dictionary containing the bot configuration settings.
    """
    return {
        "real_time_transcription": {
            "destination_url": WEBHOOK_URL,  # The location that the Recall webhook sends 
        },                                   # Be sure to register it with your Recall account: https://api.recall.ai/dashboard/webhooks/
        "transcription_options": {
            "provider": "aws_transcribe",    # Your transcription provider - You can choose from the following                                  #
            "aws_transcribe": {              # Make sure to add your keys here: https://api.recall.ai/dashboard/platforms/aws_transcribe
                "language_code": "en-US"
            }
        },
        "chat": {
            "on_bot_join": {
                "send_to": "host",
                "message": "Hello! I am Recally, here to chat!"     # The message that the bot sends when it enters the chat.
            }
        },
        "meeting_url": INVITE_LINK,     # The zoom meeting link
        "bot_name": "Recally",
        "automatic_audio_output": {
            "in_call_recording": {
                "data": {
                    "kind": "mp3",
                    "b64_data": create_audio(WELCOME_MESSAGE)       # The audio, in base64, that the bot outputs upon entering the call.
                }
            }
        }
    }


@app.route("/create-bot")
def create_bot():
    """
    Flask route that creates a new bot by sending a request to the Recall API with the appropriate payload and headers.

    The function performs the following steps:
    1. Initializes the OpenAI bot's memory by calling `initiliaze_memory()`.
    2. Sets the Recall API endpoint URL for creating a bot.
    3. Generates the bot payload using `get_bot_payload()`.
    4. Sets the headers required for the API request, including the Recall API key.
    5. Sends a POST request to the Recall API with the payload and headers to create the bot.
    6. Returns the response text from the API.

    Docs: https://docs.recall.ai/reference/bot_create

    Returns:
        str: The response text from the Recall API indicating the result of the bot creation request.
    """

    # A helper function from ai.py which initailizes the OpenAI bots memory (which is just a local JSON file, memory.json). 
    initialize_memory()

    url = "https://us-west-2.recall.ai/api/v1/bot/"    

    payload = get_bot_payload()

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": RECALL_KEY   
    }

    response = requests.post(url, json=payload, headers=headers)
    
    return response.text


def send_audio_to_bot(text: str, bot_id: str) -> requests.Response:
    """
    Sends audio data to an existing bot using the Recall API.

    The function performs the following steps:
    1. Creates the payload with the audio data in base64 format using `create_audio(text)`.
    2. Sets the headers required for the API request, including the Recall API key.
    3. Sends a POST request to the Recall API with the payload and headers to send the audio data.

    Docs: https://docs.recall.ai/reference/bot_output_audio_create

    Args:
        text (str): The text to be converted into audio and sent to the bot.
        bot_id (str): The ID of the bot to which the audio data is to be sent.

    Returns:
        requests.Response: The response object from the Recall API indicating the result of the audio data sending request.
    """
    url = f"https://us-west-2.recall.ai/api/v1/bot/{bot_id}/output_audio/"  # Recall API endpoint for sending audio data.
    
    payload = { 
        "kind": "mp3", 
        "b64_data": create_audio(text)  # Convert the text to audio in base64 format.
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": RECALL_KEY  
    }

    response = requests.post(url, json=payload, headers=headers)  
    
    return response


@app.route("/webhooks/transcription", methods=["POST"])
def webhook_handler():
    """
    Flask route to handle incoming events from the bot via webhooks. 

    This function processes various events such as:
    1. Listening for output status changes from the bot.
    2. Handling real-time transcription events and generating a response.
    3. Listening for error logs and handling them accordingly.

    The function performs the following steps:
    1. Parses the incoming JSON request body to extract the event type.
    2. Checks for transcription events where the speaker is 'Matthew Koen' and generates a response.
    3. Sends the generated response audio back to the bot.
    4. Provides a placeholder for handling error logs.

    Returns:
        str: A response indicating the webhook was processed.
    """


    request_body = request.get_json()
    event = request_body['event']

    if event == 'bot.status_change':
        # Parse status type into a more readable form for the terminal.
        print(f"\033[1m{request_body['data']['status']['code'].replace('_', ' ').title()}...\033[0m")     

    # and request_body["data"]["transcript"]["speaker"] == 'Matthew Koen'
    if event == 'bot.transcription':  # check if the event is a real-time transcription event

        # Joins individual words into sentence for ChatGPT
        sentence = ' '.join(word['text'] for word in request_body["data"]["transcript"]["words"])  
        
        # Generate response to the caller from ChatGPT 
        bot_response = generate_response(sentence)  

        # Sends ChatGPT response as audio to the bot 
        send_audio_to_bot(bot_response, request_body["data"]["bot_id"])  


    # Here, you can listen for error logs and handle them accordingly
    if event == 'bot.log':
        ...
    
    return "success"

@app.route("/redirect")
def redirect(): 
    """
    Simple redirect callback endpoint for local development Zoom authentication 
    (only required once when allowing application to connect to your Zoom account)
    
    """
    return "You have authorized your Zoom account with your Recall app"


app.run(host='127.0.0.1', port=8080)  #Run Flask Server on localhost:8080


