import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai  # New official package

# API key from Render environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise Exception("API Key not found. Set GOOGLE_API_KEY in Render environment variables.")

# Initialize GenAI client
client = genai.Client(api_key=API_KEY)

app = FastAPI(title="FastAPI + Gemini GenAI")

class Question(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "API is working"}

@app.post("/ask")
def ask_question(q: Question):
    try:
        # Use official model
        response = client.generate_text(
            model="models/text-bison-001",
            prompt=q.question
        )
        return {"answer": response.output_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))