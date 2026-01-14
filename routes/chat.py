from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from modals.schemas import ChatRequest, ChatResponse
from database.connection import get_db
from ai_services.ai_service import ai_service
from modals.database_models import ConversationLog

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
async def chat_with_emo(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Chat with EMO! Send a message and get a cute response.

    - **message**: Your message to EMO
    - **user_id**: Optional user identifier for tracking conversations
    """

    try:
        # Generate response using AI service
        result = await ai_service.generate_response(request.message, db)

        # Log conversation
        conversation_log = ConversationLog(
            user_input=request.message,
            emo_response=result["response"],
            model_used=result["model_used"],
            response_time_ms=result.get("response_time_ms"),
        )
        db.add(conversation_log)
        db.commit()

        # Return response
        return ChatResponse(
            response=result["response"],
            model_used=result["model_used"],
            response_time_ms=result["response_time_ms"],
            timestamp=datetime.now(),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Oopsie! Something went wrong: {str(e)}"
        )
