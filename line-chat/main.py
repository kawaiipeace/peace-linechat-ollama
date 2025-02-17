# LINE Webhook for Chatbot with OLLAMA Integration
# Created and Modified by PEACE & CHATGPT @ 17022025

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

# Supported models
VALID_MODELS = {"mistral", "gpt-4", "llama3.2","hf.co/openthaigpt/openthaigpt1.5-7b-instruct","deepseek-r1"}

# Store user-selected models
user_models = {}

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
            user_id = event.source.user_id
            user_input = event.message.text.strip()

            # Handle model selection command
            # For Example, #model llama
            if user_input.startswith("#model"):
                model_name = user_input.split(" ", 1)[-1].strip()

                if model_name in VALID_MODELS:
                    user_models[user_id] = model_name
                    response_text = f"🤖 โมเดลถูกเปลี่ยนเป็น {model_name} แล้ว 🤖"
                else:
                    response_text = (
                        f"ไม่มี Model ที่ชื่อ `{model_name}`\n"
                        f"Model ที่มีให้เลือกใช้มีดังนี้ {', '.join(VALID_MODELS)}."
                    )
            else:
                # Use user's selected model or auto-detect from keywords
                model = user_models.get(user_id, detect_model(user_input))
                response_text = query_ollama(user_input, model)

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=response_text)
            )

    return {"message": "OK"}

def detect_model(user_input: str) -> str:
    """Detects the model based on user input keywords."""
    user_input_lower = user_input.lower()
    if "mistral" in user_input_lower:
        return "mistral"
    elif "gpt" in user_input_lower:
        return "gpt-4"
    elif "llama3.2" in user_input_lower:
        return "llama3.2"
    elif "hf.co/openthaigpt/openthaigpt1.5-7b-instruct" in user_input_lower:
        return "hf.co/openthaigpt/openthaigpt1.5-7b-instruct"
    elif "deepseek-r1" in user_input_lower:
        return "deepseek-r1"
    return "llama3.2"  # Default model

def query_ollama(prompt, model="llama3.2"):
    """Send a request to the Ollama API with the specified model."""
    payload = {"model": model, "prompt": prompt, "stream": False}  # Disable streaming
    response = requests.post(OLLAMA_API_URL, json=payload)

    if response.status_code == 200:
        try:
            response_json = response.json()
            print(f"API Response: {response_json}")  # Debugging
            return response_json.get("response", "No response received.")
        except ValueError:
            print(f"Error: Invalid JSON response. Raw: {response.text}")
            return "⚠️ พบปัญหาฟอร์แมตที่ตอบกลับมาไม่ถูกต้อง (Model ตอบกลับมาแปลก ๆ)"
    else:
        print(f"Error: API returned {response.status_code}")
        return f"⚠️ พบปัญหาที่ไม่สามารถดำเนินการได้ (Model อาจจะไม่มีอยู่จริงหรืออื่น ๆ). สถานะ: {response.status_code}"
