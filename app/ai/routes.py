from fastapi import APIRouter, HTTPException
from .service import chat_with_ai, summarize_document
from .schemas import ChatRequest, SummarizeRequest, SummarizeResponse

router = APIRouter(prefix="/ai", tags=["AI"])

MAX_CHAT_INPUT_LENGTH = 2000
MAX_SUMMARY_INPUT_LENGTH = 5000

@router.post("/chat")
def ai_chat(request: ChatRequest):
    print(len(request.message))
    if len(request.message) > MAX_CHAT_INPUT_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Input text exceeds maximum allowed length ({MAX_CHAT_INPUT_LENGTH} characters)."
        )    
    
    try:
        response = chat_with_ai(request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summarize", response_model=SummarizeResponse)
def summarize(request: SummarizeRequest):
    if len(request.text) > MAX_SUMMARY_INPUT_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Input text exceeds maximum allowed length ({MAX_SUMMARY_INPUT_LENGTH} characters)."
        )
        
    try:
        result = summarize_document(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
