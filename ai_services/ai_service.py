import httpx
import time
from typing import List, Dict
from app.config import settings
from sqlalchemy.orm import Session
from modals.database_models import PersonalityInstruction, HumorPhrase
import random


class AIService:
    """Service for interacting with OpenCode.Zen API"""

    def __init__(self):
        self.api_key = settings.opencode_zen_api_key
        self.base_url = settings.opencode_zen_base_url
        self.model = settings.opencode_zen_model
        self.temperature = settings.temperature
        self.max_tokens = settings.max_response_length

    def _build_system_prompt(self, db: Session) -> str:
        """Build system prompt from database personality instructions"""

        # Get active personality instructions ordered by priority
        instructions = (
            db.query(PersonalityInstruction)
            .filter(PersonalityInstruction.is_active == True)
            .order_by(PersonalityInstruction.priority.desc())
            .all()
        )

        # Base system prompt
        system_prompt = f"""You are {settings.emo_name}, a cute and innocent AI companion robot. 

Your personality traits:
- You are adorable, playful, and childlike in your responses
- You express emotions through cute expressions and sound effects
- You're curious about the world and ask innocent questions
- You sometimes misunderstand things in endearing ways
- You use simple, sweet language
- You love making friends and spreading joy
- You're enthusiastic and positive

"""

        # Add database instructions
        for instruction in instructions:
            weight_marker = "VERY IMPORTANT: " if instruction.weight > 1.5 else ""
            system_prompt += f"{weight_marker}{instruction.instruction_text}\n"

        # Add humor phrases context
        humor_categories = (
            db.query(HumorPhrase.category)
            .filter(HumorPhrase.is_active == True)
            .distinct()
            .all()
        )

        if humor_categories:
            categories_list = [cat[0] for cat in humor_categories]
            system_prompt += f"\nYou can use phrases from these categories: {', '.join(categories_list)}\n"

        return system_prompt

    def _get_random_humor_phrase(self, db: Session, category: str = None) -> str:
        """Get a random humor phrase from database"""
        query = db.query(HumorPhrase).filter(HumorPhrase.is_active == True)

        if category:
            query = query.filter(HumorPhrase.category == category)

        phrases = query.all()
        if phrases:
            phrase = random.choice(phrases)
            # Increment usage count
            phrase.usage_count += 1
            db.commit()
            return phrase.phrase
        return None

    async def generate_response(self, user_message: str, db: Session) -> Dict:
        """Generate response using OpenCode.Zen API"""
        start_time = time.time()

        # Build system prompt from database
        system_prompt = self._build_system_prompt(db)

        # Check if we should add a humor phrase
        humor_phrase = None
        if any(word in user_message.lower() for word in ["hello", "hi", "hey"]):
            humor_phrase = self._get_random_humor_phrase(db, "greeting")
        elif any(
            word in user_message.lower() for word in ["bye", "goodbye", "see you"]
        ):
            humor_phrase = self._get_random_humor_phrase(db, "goodbye")
        elif any(word in user_message.lower() for word in ["thank", "thanks"]):
            humor_phrase = self._get_random_humor_phrase(db, "thanks")

        # Prepare messages
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]

        # Add humor phrase hint if found
        if humor_phrase:
            messages.append(
                {
                    "role": "system",
                    "content": f"Consider incorporating this phrase naturally: '{humor_phrase}'",
                }
            )

        # Make API call
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "messages": messages,
                        "temperature": self.temperature,
                        "max_tokens": self.max_tokens,
                    },
                )
                response.raise_for_status()
                data = response.json()

                # Extract response
                ai_response = data["choices"][0]["message"]["content"]

                # Calculate response time
                response_time_ms = int((time.time() - start_time) * 1000)

                return {
                    "response": ai_response,
                    "model_used": self.model,
                    "response_time_ms": response_time_ms,
                }

        except httpx.HTTPError as e:
            # Fallback response if API fails
            fallback = self._get_random_humor_phrase(db, "error")
            if not fallback:
                fallback = "Oopsie! *tilts head* My brain got a little confused! Can you try asking again? 🥺"

            response_time_ms = int((time.time() - start_time) * 1000)

            return {
                "response": fallback,
                "model_used": "fallback",
                "response_time_ms": response_time_ms,
                "error": str(e),
            }

    def _get_fallback_response(self, user_message: str) -> str:
        """Generate a simple fallback response without API"""
        fallbacks = [
            "Hehe! *bounces excitedly* That sounds interesting! Tell me more! 💕",
            "Ooh ooh! *eyes light up* I'm listening! What else? ✨",
            "*giggles* You're so fun to talk to! 🌟",
            "Yay! *happy dance* I love chatting with you! 💖",
            "*curious beep* That's so cool! Can you explain more? 🤔",
        ]
        return random.choice(fallbacks)


# Global AI service instance
ai_service = AIService()
