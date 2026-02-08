from fastapi import FastAPI
from pydantic import BaseModel
import requests
app = FastAPI(title="Prompt Module API")
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "llama3.2:latest"



class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    answer: str


@app.get("/")
def root():
    return {"status": "ok", "message": "Prompt module backend running"}


@app.post("/chat/prompt", response_model=ChatResponse)
def chat_prompt(req: ChatRequest):
    payload = {
        "model": MODEL_NAME,
        "prompt": req.query,
        "stream": False
    }

    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=300)
        if r.status_code != 200:
            return ChatResponse(answer=f"Ollama error {r.status_code}: {r.text}")

        out = r.json()
        return ChatResponse(answer=out.get("response", "").strip())

    except Exception as e:
        return ChatResponse(answer=f"Backend error calling Ollama: {str(e)}")
