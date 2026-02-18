from fastapi import APIRouter, HTTPException, Request
from time import time
from collections import defaultdict

from .service import chat_with_ai, summarize_document
from .schemas import ChatRequest, SummarizeRequest, SummarizeResponse

router = APIRouter(prefix="/ai", tags=["AI"])

MAX_CHAT_INPUT_LENGTH = 2000
MAX_SUMMARY_INPUT_LENGTH = 5000

REQUEST_LOG = defaultdict(list)
RATE_LIMIT = 3
WINDOW_SIZE = 60

# Helper Class
def check_rate_limit(client_ip: str):
    current_time = time()
    request_times = REQUEST_LOG[client_ip]
    
    # remove old requests outside window
    REQUEST_LOG[client_ip] = [
        t for t in request_times if current_time - t < WINDOW_SIZE
    ]
    
    if len(REQUEST_LOG[client_ip]) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Try again later."
        )
        
    REQUEST_LOG[client_ip].append(current_time)

@router.post("/chat")
def ai_chat(payload: ChatRequest, req: Request):
    check_rate_limit(req.client.host)
    if len(payload.message) > MAX_CHAT_INPUT_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Input text exceeds maximum allowed length ({MAX_CHAT_INPUT_LENGTH} characters)."
        )    
    
    try:
        response = chat_with_ai(payload.message, req.state.request_id)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summarize", response_model=SummarizeResponse)
def summarize(payload: SummarizeRequest, req: Request):
    check_rate_limit(req.client.host)    
    if len(payload.text) > MAX_SUMMARY_INPUT_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Input text exceeds maximum allowed length ({MAX_SUMMARY_INPUT_LENGTH} characters)."
        )
        
    try:
        result = summarize_document(payload.text, req.state.request_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

