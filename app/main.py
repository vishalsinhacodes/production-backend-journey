from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import engine, get_db
from .models import Base, User


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