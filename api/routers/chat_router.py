from fastapi import APIRouter, Depends
from services.chat_service import ChatService
from api.schemas.base_response import BaseResponse
from api.schemas.chat_response import (
    ChatResponse,
    TranslationResponse,
    SummarizationResponse,
    MentalCareResponse,
    DateCalculationResponse,
    TimeConversionResponse,
)

chat_servcie = ChatService()

router = APIRouter(
    prefix="/chat", tags=["chat"],
)

@router.post("/chat", response_model=BaseResponse[ChatResponse])
async def general(request: str):
    result = chat_servcie.process_message(request)
    return BaseResponse(success=True, data=result)