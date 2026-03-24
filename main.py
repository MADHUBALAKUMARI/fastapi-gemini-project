from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from google import genai

# Load env
load_dotenv()

# Create client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

class Question(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "FastAPI + Gemini latest running 🚀"}

@app.post("/ask")
def ask_question(data: Question):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",   # ✅ FINAL FIX
            contents=data.question
        )
        return {"answer": response.text}
    except Exception as e:
        return {"error": str(e)}