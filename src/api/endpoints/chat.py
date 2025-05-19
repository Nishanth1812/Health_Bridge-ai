
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    # TODO: connect to retrieval + generation pipeline
    return ChatResponse(answer="(demo) I am still learning.")
