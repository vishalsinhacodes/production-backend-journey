from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import engine, get_db
from .models import Base, User
from .ai_service import chat_with_ai, summarize_document
from pydantic import BaseModel


app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/users")
def create_user(name: str, db: Session = Depends(get_db)):
    new_user = User(name=name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users")
def get_users(db: Session= Depends(get_db)):
    users = db.query(User).all()
    return users

class ChatRequest(BaseModel):
    message: str
    
@app.post("/ai/chat")
def ai_chat(request: ChatRequest):
    try:
        response = chat_with_ai(request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
class SummarizeRequest(BaseModel):
    text: str
    
class SummarizeResponse(BaseModel):
    summary: str
    key_points: list[str]
    action_items: list[str]
    
@app.post("/ai/summarize", response_model=SummarizeResponse)
def summerize(request: SummarizeRequest):
    try:
        result = summarize_document(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))        