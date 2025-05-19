
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .endpoints.chat import router as chat_router
from .endpoints.feedback import router as feedback_router

app = FastAPI(title="Preventive Healthcare Chatbot API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/chat", tags=["Chat"])
app.include_router(feedback_router, prefix="/feedback", tags=["Feedback"])

@app.get("/")
async def root():
    return {"message": "Preventive Healthcare Chatbot is running"}
