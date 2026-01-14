from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float
from sqlalchemy.sql import func
from database.connection import Base


class HumorPhrase(Base):
    """Model for storing EMO's humor phrases and personality traits"""

    __tablename__ = "humor_phrases"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), nullable=False, index=True)
    phrase = Column(Text, nullable=False)
    context = Column(String(100), nullable=True)
    cuteness_level = Column(Integer, default=5)  # 1-10 scale
    usage_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<HumorPhrase(id={self.id}, category='{self.category}', cuteness={self.cuteness_level})>"


class PersonalityInstruction(Base):
    """Model for storing EMO's personality instructions"""

    __tablename__ = "personality_instructions"

    id = Column(Integer, primary_key=True, index=True)
    instruction_type = Column(String(50), nullable=False, index=True)
    instruction_text = Column(Text, nullable=False)
    priority = Column(Integer, default=1)  # Higher priority = more important
    weight = Column(Float, default=1.0)  # How strongly to apply this instruction
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<PersonalityInstruction(id={self.id}, type='{self.instruction_type}', priority={self.priority})>"


class ConversationLog(Base):
    """Model for storing conversation history"""

    __tablename__ = "conversation_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_input = Column(Text, nullable=False)
    emo_response = Column(Text, nullable=False)
    model_used = Column(String(50), nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<ConversationLog(id={self.id}, timestamp='{self.created_at})>"
