# Conversational AI in Zoom with [Recall.ai](https://www.recall.ai/)

In this project, we will create a conversational AI bot to listen and respond to Zoom participants. It demonstrates Recall's real-time transcription functionality using minimal code and a simple backend, which you can extend to build many interesting applications. Let's begin.

## Getting Started

Running this app locally first requires a few configurations.

### Ngrok Config
We use Ngrok to allow for local webhook development and for authenticating our app with our Zoom account. 

Follow the steps [here](https://docs.recall.ai/docs/local-webhook-development#ngrok-setup) for setup instructions. 

In app.py, input your Ngrok static URL here, on line 19:

```python
NGROK_BASE_URL = "YOUR NGROK URL"
```

### Zoom Developer App

Navigate to the [Zoom App Marketplace](https://marketplace.zoom.us/) and click **Develop** **>** **Build App** **>** **General App** **>** **Create** 

Under **Basic Information** **>** **OAuth Information**, set the OAuth Redirect URL to https:// followed by your Ngrok static URL (that we configured about) followed by /redirect: https://<YOUR_NGROK_STATIC_URL/redirect

Build your app following their onboarding process, ensuring that **Embed** **>** **Meeting SDK** is turned on.

Run the following command in your terminal, replacing <YOUR_NGROK_STATIC_URL> with your Ngrok static URL (that we configured about):

```bash
ngrok http --domain=<YOUR_NGROK_STATIC_URL>.ngrok-free.app 8080
```

Click **Embed > Add App** and follow the auth process. You should see a message saying "You have authorized your Zoom account with your Recall app"

### Zoom Settings Config


```bash
print("hello world")
```
