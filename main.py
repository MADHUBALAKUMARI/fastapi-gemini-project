from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai


API_KEY = "AIzaSyAWagSvdi80AFqORGonS2jR_j6E5Loo26Q"
client = genai.Client(api_key=API_KEY)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is working"}

class Question(BaseModel):
    question: str


def get_supported_model():
    models = client.models.list()
    for m in models:
        
        try:
            
            if m.name.startswith("models/"):
                return m.name
        except:
            continue
    return None

@app.post("/ask")
def ask_question(q: Question):
    try:
        model_name = get_supported_model()
        if not model_name:
            raise HTTPException(status_code=500, detail="No supported model found for generateContent")

        response = client.models.generate_content(
            model=model_name,
            contents=q.question
        )
        return {"answer": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))