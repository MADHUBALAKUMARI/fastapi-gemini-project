from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

app = FastAPI()

# API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

class Question(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "API is working "}

@app.post("/ask")
def ask_question(q: Question):
    try:
        if not OPENROUTER_API_KEY:
            return {"error": "API key missing "}

        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": q.question}
            ]
        }

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