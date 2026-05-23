# src/server/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from src.server.core.brain import SamanthaBrain
from src.server.config import settings

app = FastAPI(title="Samantha AI Server")
brain = SamanthaBrain()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []

@app.get("/")
def read_root():
    return {"message": "Samantha is online.", "model": settings.MODEL_NAME}

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        # history 객체를 딕셔너리 리스트로 변환
        formatted_history = [
            {"role": msg.role, "content": msg.content} 
            for msg in request.history
        ]
        
        response = brain.think(request.message, history=formatted_history)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
