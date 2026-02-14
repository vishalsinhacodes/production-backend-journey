from fastapi import FastAPI

from .database import engine
from .models import Base
from app.ai.routes import router as ai_router
from app.users.routes import router as users_router


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(ai_router)
app.include_router(users_router)

@app.get("/health")
def health_check():
    return {"status": "ok"} 