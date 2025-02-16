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
            response_text = query_ollama(user_input)
            
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=response_text)
            )

    return {"message": "OK"}

def query_ollama(prompt):
    """Send a request to the Ollama API."""
    payload = {"model": "mistral", "prompt": prompt}
    response = requests.post(OLLAMA_API_URL, json=payload)

    if response.status_code == 200:
        return response.json().get("response", "No response received.")
    else:
        return "Sorry, I couldn't process your request."

