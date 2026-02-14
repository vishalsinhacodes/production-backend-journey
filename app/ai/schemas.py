from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class SummarizeRequest(BaseModel):
    text: str

class SummarizeResponse(BaseModel):
    summary: str
    key_points: list[str]
    action_items: list[str]
