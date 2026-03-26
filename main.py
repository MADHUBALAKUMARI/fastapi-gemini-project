from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class Question(BaseModel):
    question: str

API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.get("/")
def home():
    return {"message": "API is working"}

@app.post("/ask")
def ask_question(q: Question):
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "openai/gpt-3.5-turbo",  # free model
            "messages": [
                {"role": "user", "content": q.question}
            ]
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        return {
            "answer": result["choices"][0]["message"]["content"]
        }

    except Exception as e:
        return {"error": str(e)}