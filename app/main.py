from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from app.config import settings
from database.connection import init_db, get_db, engine
from database.seed import seed_database
from routes import chat, humor, personality
from modals.schemas import HealthCheck
from modals.database_models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("🤖 EMO AI Backend starting up...")
    print(f"🎭 Personality: {settings.emo_personality}")
    print(f"🤖 EMO Name: {settings.emo_name}")

    # Initialize database
    print("📊 Initializing database...")
    init_db()

    # Seed database if empty
    print("🌱 Checking database seed status...")
    db = next(get_db())
    try:
        seed_database(db)
    finally:
        db.close()

    print("✅ EMO AI Backend is ready!")
    print(f"🌐 API running on http://{settings.api_host}:{settings.api_port}")
    print(f"📚 Docs available at http://{settings.api_host}:{settings.api_port}/docs")

    yield

    # Shutdown
    print("👋 EMO AI Backend shutting down... Bye bye!")


# Create FastAPI app
app = FastAPI(
    title="EMO AI Backend",
    description="""
    🤖 **EMO AI Backend API** - A cute and innocent AI companion!
    
    This API mimics the adorable personality of EMO AI, complete with:
    - 💬 Text generation using free AI models (BigPickle from OpenCode.Zen)
    - 😊 Customizable humor phrases stored in PostgreSQL
    - 🎭 Personality instructions that shape EMO's behavior
    - 📊 Conversation logging and analytics
    
    ## Features
    
    - **Chat with EMO**: Send messages and get cute, innocent responses
    - **Manage Humor**: Add, update, and organize EMO's funny phrases
    - **Shape Personality**: Control how EMO behaves with custom instructions
    - **Track Conversations**: All interactions are logged for learning
    
    ## Getting Started
    
    1. Make sure you have your OpenCode.Zen API key in the `.env` file
    2. Use the `/chat/` endpoint to start talking with EMO
    3. Use `/humor/phrases` to add more cute phrases
    4. Use `/personality/instructions` to fine-tune EMO's personality
    
    *Made with 💕 to bring joy and cuteness to your day!*
    """,
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)
app.include_router(humor.router)
app.include_router(personality.router)


@app.get("/", tags=["Root"])
async def root():
    """
    Welcome endpoint!

    EMO says hi! 👋✨
    """
    return {
        "message": "Hiii! *bounces excitedly* Welcome to EMO AI Backend! 💕",
        "emo_name": settings.emo_name,
        "personality": settings.emo_personality,
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", response_model=HealthCheck, tags=["Health"])
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint.

    Check if EMO is awake and ready to chat! 🏥
    """

    # Test database connection
    try:
        from sqlalchemy import text

        db.execute(text("SELECT 1"))
        db_connected = True
    except Exception:
        db_connected = False

    return HealthCheck(
        status="healthy" if db_connected else "unhealthy",
        emo_name=settings.emo_name,
        personality=settings.emo_personality,
        database_connected=db_connected,
        api_ready=True,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
    )
