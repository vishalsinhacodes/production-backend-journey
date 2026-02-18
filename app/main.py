import logging
import time
import uuid

from fastapi import FastAPI, Request

from .database import engine
from .models import Base
from app.ai.routes import router as ai_router
from app.users.routes import router as users_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    start_time = time.time()
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(
        f"request_id={request_id} "
        f"{request.method} {request.url.path} "
        f"Status: {response.status_code} "
        f"Duration: {process_time: .2f}s"
    )
    
    return response

Base.metadata.create_all(bind=engine)

app.include_router(ai_router)
app.include_router(users_router)

@app.get("/health")
def health_check():
    return {"status": "ok"} 