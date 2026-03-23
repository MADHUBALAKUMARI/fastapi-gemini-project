from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
import os


API_KEY = os.getenv("AIzaSyAL9pXxPYLEPJ11OugxLUYLt_yCvaccbvc")

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not set")

client = genai.Client(api_key=API_KEY)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is working"}

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask_question(q: Question):
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=q.question
        )
        return {"answer": getattr(response, "text", str(response))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))