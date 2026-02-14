from fastapi import APIRouter, HTTPException
from .service import chat_with_ai, summarize_document
from .schemas import ChatRequest, SummarizeRequest, SummarizeResponse

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/chat")
def ai_chat(request: ChatRequest):
    try:
        response = chat_with_ai(request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summarize", response_model=SummarizeResponse)
def summarize(request: SummarizeRequest):
    try:
        result = summarize_document(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
