# Conversational AI in Zoom with [Recall.ai](https://www.recall.ai/)

In this project, we will create a conversational AI bot to listen and respond to Zoom participants. It demonstrates Recall's real-time transcription functionality using minimal code and a simple backend, which you can extend to build many interesting applications. Let's begin.

## Getting Started

Running this app locally first requires a few configurations.

### Ngrok Config
We use Ngrok to allow for local webhook development and for authenticating our app with our Zoom account. 

Follow the steps [here](https://docs.recall.ai/docs/local-webhook-development#ngrok-setup) for setup instructions. 

On line 19 of app.py, input your Ngrok static URL:

```python
NGROK_BASE_URL = "YOUR NGROK URL"
```

### Zoom Developer App

Navigate to the [Zoom App Marketplace](https://marketplace.zoom.us/) and click **Develop** **>** **Build App** **>** **General App** **>** **Create** 

Under **Basic Information** **>** **OAuth Information**, set the OAuth Redirect URL to 

`https://<YOUR_NGROK_STATIC_URL/redirect`

Build your app following their onboarding process, ensuring that **Embed** **>** **Meeting SDK** is turned on.

Run the following command in your terminal, replacing <YOUR_NGROK_STATIC_URL> with your Ngrok static URL (that we configured about):

```bash
ngrok http --domain=<YOUR_NGROK_STATIC_URL>.ngrok-free.app 8080
```
Add your Client ID and Client Secret to Recall [here](https://us-west-2.recall.ai/dashboard/platforms/zoom).

Click **Embed > Add App** and follow the auth process. You should see a message saying "You have authorized your Zoom account with your Recall app"

### Zoom Desktop and Website App Settings Config

Lastly, you need to allow for closed captions within your Zoom account. 

Navigate to your [zoom profile](https://zoom.us/profile) on zooms web app and click **Settings** on the left nav bar. Scroll all the way to the bottom until you see **In Meeting (Advanced)** and turn on **Automated captions**. 

Next, open up your Zoom Desktop App. Click your profile, then **Settings > Accessibility** and click Always show captions.

### Key & Webhook configs 

Add your AWS Keys to your Recall account. 

Finally, in your [Recall](https://api.recall.ai/dashboard/webhooks/) account, click **Webhooks > Add Endpoint** and and set the endpoint url to 

`https://<YOUR_NGROK_STATIC_URL/webhooks/transcription`

Now you're ready to go!

# Running the app

To run the app, start a Zoom meeting in the Zoom Desktop App. Copy the invite link and paste it into line 17 of app.py

```python
INVITE_LINK = "YOUR INVITE LINK"
```

Next, install the requirements and start up the Flask server:

```bash
pip install -r requirements.txt
```

```bash
python3 app.py
```

Finally, send a bot to your Zoom call:
```bash
curl localhost:8080/create-bot
```
You should quickly see Recally, the conversational AI, requesting to join the call. Allow, and also allow her request to record the video. 

Happy chatting!

