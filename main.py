from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# FastAPI app with title, description, version (friend style)
app = FastAPI(
    title="Chat API",
    description="AI Chatbot API using OpenRouter - Friend Style Swagger UI",
    version="1.0.0",
    contact={
        "name": "Gauri's API",
        "url": "https://yourwebsite.com",
        "email": "gauri@example.com"
    }
)

# API Key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Request Model
class ChatRequest(BaseModel):
    question: str

# Root Endpoint
@app.get("/", tags=["Root"])
def root():
    return {"message": "API is working 🚀"}

# Chat Endpoint
@app.post("/chat", tags=["Chat"])
def chat(request: ChatRequest):
    if not OPENROUTER_API_KEY:
        return {"error": "API key missing ❌"}

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": request.question}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if "choices" in result:
            return {
                "answer": result["choices"][0]["message"]["content"]
            }
        else:
            return {"error": result}

    except Exception as e:
        return {"error": str(e)}