from flask import Flask
import os
import requests
app = Flask(__name__)
from recallai import RecallAi

headers = f"Authorization: Token {os.getenv('TOKEN')}"  # Set Recall.ai token - https://api.recall.ai/auth/login/?next=/dashboard/apikeys/





@app.route("/", methods=['POST'])
def hello_world():
    ...



app.run(host='127.0.0.1', port=3000) 