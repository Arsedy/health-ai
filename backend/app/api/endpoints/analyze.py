from fastapi import APIRouter
from app.services.ai_service import Message, doctor_recommendation 

router = APIRouter()

@router.post("/analyze")
async def analyze_symptoms(message: Message):
    result = await doctor_recommendation(message.prompt)
    return result