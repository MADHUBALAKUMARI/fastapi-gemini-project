from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

class Question(BaseModel):
    question: str

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.post("/ask")
def ask(question: Question):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": question.question}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        return {
            "answer": result["choices"][0]["message"]["content"]
        }

    except Exception as e:
        return {"error": str(e)}