
from fastapi import APIRouter, Body
from pydantic import BaseModel

router = APIRouter()

class FeedbackRequest(BaseModel):
    query: str
    answer: str
    rating: int  # 1-5
    comments: str | None = None

@router.post("/")
async def feedback_endpoint(data: FeedbackRequest):
    # TODO: save feedback to DB or logs
    return {"status": "received"}
