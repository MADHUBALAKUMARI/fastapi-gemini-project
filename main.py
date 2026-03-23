import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai

# API Key from environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise Exception("API Key not found. Set GOOGLE_API_KEY as environment variable.")

# Initialize Gemini AI client
client = genai.Client(api_key=API_KEY)

app = FastAPI(title="FastAPI + Gemini GenAI")

@app.get("/")
def home():
    return {"message": "API is working"}

class Question(BaseModel):
    question: str

def get_supported_model():
    """
    Return the first model that supports generateContent.
    Fallback: if supported_methods missing, use models with 'models/' prefix.
    """
    models = client.models.list()
    for m in models:
        try:
            if "generateContent" in getattr(m, "supported_methods", []):
                return m.name
            elif getattr(m, "name", "").startswith("models/"):
                return m.name
        except:
            continue
    return None

@app.post("/ask")
def ask_question(q: Question):
    model_name = get_supported_model()
    if not model_name:
        raise HTTPException(status_code=500, detail="No supported model found")

    try:
        # Generate content from Gemini GenAI
        response = client.models.generate_content(
            model=model_name,
            contents=[q.question]
        )

        # Extract answer safely
        answer = getattr(response, "output_text", None)
        
        # Fallback for alternate response attribute (latest SDK)
        if not answer:
            try:
                # Some SDK versions store it in 'content' of first output
                answer = response.outputs[0].content
            except:
                # Last fallback: return string representation
                answer = str(response)

        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))