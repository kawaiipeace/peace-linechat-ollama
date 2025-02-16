import os
import requests
from fastapi import FastAPI, Request
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError

app = FastAPI()

# Load environment variables
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://ollama:11434/api/generate")

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(CHANNEL_SECRET)

@app.post("/webhook")
async def webhook(request: Request):
    signature = request.headers.get("X-Line-Signature")
    body = await request.body()

    try:
        events = parser.parse(body.decode("utf-8"), signature)
    except InvalidSignatureError:
        return {"message": "Invalid signature"}

    for event in events:
        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):
            user_input = event.message.text

            # Check for model keywords (you can customize this)
            if "mistral" in user_input.lower():
                model = "mistral"
            elif "gpt" in user_input.lower():
                model = "gpt-4"
            elif "llama" in user_input.lower():
                model = "llama3.2"
            else:
                model = "llama3.2"  # Default model

            response_text = query_ollama(user_input, model)
            
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=response_text)
            )

    return {"message": "OK"}

def query_ollama(prompt, model="mistral"):
    """Send a request to the Ollama API with a specified model."""
    payload = {"model": model, "prompt": prompt}
    response = requests.post(OLLAMA_API_URL, json=payload)

    if response.status_code == 200:
        try:
            response_json = response.json()
            # Log the entire response for debugging purposes
            print(f"API Response: {response_json}")
            return response_json.get("response", "No response received.")
        except ValueError:
            # If the response isn't a valid JSON, log the raw content
            print(f"Error: Response is not in JSON format. Raw response: {response.text}")
            return "Sorry, the response is not in the expected format."
    else:
        print(f"Error: Received status code {response.status_code} from Ollama API.")
        return f"Sorry, I couldn't process your request. Status Code: {response.status_code}"
