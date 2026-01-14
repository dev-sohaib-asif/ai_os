from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ChatRequest(BaseModel):
    """Request schema for chat endpoint"""
    message: str = Field(..., min_length=1, max_length=1000, description="User message to EMO")
    user_id: Optional[str] = Field(None, description="Optional user identifier")
    

class ChatResponse(BaseModel):
    """Response schema for chat endpoint"""
    response: str = Field(..., description="EMO's response")
    model_used: str = Field(..., description="AI model used")
    response_time_ms: int = Field(..., description="Response time in milliseconds")
    timestamp: datetime = Field(..., description="Response timestamp")


class HumorPhraseCreate(BaseModel):
    """Schema for creating a new humor phrase"""
    category: str = Field(..., min_length=1, max_length=50, description="Category (greeting, goodbye, thanks, etc.)")
    phrase: str = Field(..., min_length=1, description="The actual phrase")
    context: Optional[str] = Field(None, max_length=100, description="When to use this phrase")
    cuteness_level: int = Field(5, ge=1, le=10, description="Cuteness level (1-10)")


class HumorPhraseResponse(BaseModel):
    """Schema for humor phrase response"""
    id: int
    category: str
    phrase: str
    context: Optional[str]
    cuteness_level: int
    usage_count: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class PersonalityInstructionCreate(BaseModel):
    """Schema for creating a personality instruction"""
    instruction_type: str = Field(..., min_length=1, max_length=50, description="Type of instruction")
    instruction_text: str = Field(..., min_length=1, description="The instruction text")
    priority: int = Field(1, ge=1, le=10, description="Priority (1-10)")
    weight: float = Field(1.0, ge=0.1, le=2.0, description="Weight (0.1-2.0)")


class PersonalityInstructionResponse(BaseModel):
    """Schema for personality instruction response"""
    id: int
    instruction_type: str
    instruction_text: str
    priority: int
    weight: float
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class HealthCheck(BaseModel):
    """Schema for health check response"""
    status: str
    emo_name: str
    personality: str
    database_connected: bool
    api_ready: bool
