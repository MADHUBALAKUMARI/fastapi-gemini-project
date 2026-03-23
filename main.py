import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai  # <- updated package

# API Key from environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise Exception(
        "API Key not found. Set GOOGLE_API_KEY as environment variable in Render dashboard."
    )

# Initialize Gemini AI client
client = genai.Client(api_key=API_KEY)

app = FastAPI(title="FastAPI + Gemini GenAI")

@app.get("/")
def home():
    return {"message": "API is working"}

class Question(BaseModel):
    question: str

def get_supported_model():
    """Return a supported model for content generation."""
    try:
        models = client.list_models()
        for m in models:
            if "generateText" in getattr(m, "supported_methods", []):
                return m.name
        # fallback: pick first model with 'models/' prefix
        for m in models:
            if getattr(m, "name", "").startswith("models/"):
                return m.name
    except Exception as e:
        print("Error fetching models:", e)
    return None

@app.post("/ask")
def ask_question(q: Question):
    model_name = get_supported_model()
    if not model_name:
        raise HTTPException(status_code=500, detail="No supported model found")

    try:
        # Generate content from Gemini GenAI
        response = client.generate_text(
            model=model_name,
            prompt=q.question
        )

        # Extract answer safely
        answer = getattr(response, "output_text", None)
        if not answer:
            try:
                answer = response.outputs[0].content
            except Exception:
                answer = str(response)

        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))