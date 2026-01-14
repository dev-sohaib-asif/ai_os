# EMO AI Backend - Project Structure

```
emo-ai-backend/
│
├── app/                          # Main application package
│   ├── __init__.py              # Package initializer
│   ├── main.py                  # FastAPI application & entry point
│   ├── config.py                # Settings & environment configuration
│   │
│   ├── database/                # Database layer
│   │   ├── __init__.py
│   │   ├── connection.py        # Database connection & session management
│   │   └── seed.py              # Database seeding with initial data
│   │
│   ├── models/                  # Data models
│   │   ├── __init__.py
│   │   ├── database_models.py   # SQLAlchemy ORM models
│   │   └── schemas.py           # Pydantic request/response schemas
│   │
│   ├── routes/                  # API endpoints
│   │   ├── __init__.py
│   │   ├── chat.py              # Chat/conversation endpoints
│   │   ├── humor.py             # Humor phrase management
│   │   └── personality.py       # Personality instruction management
│   │
│   └── services/                # Business logic
│       ├── __init__.py
│       └── ai_service.py        # OpenCode.Zen API integration
│
├── .env                         # Environment variables (not in git)
├── .env.example                 # Example environment file
├── .gitignore                   # Git ignore rules
├── pyproject.toml              # Project dependencies (UV)
├── README.md                    # Main documentation
├── API_EXAMPLES.md             # API usage examples
├── STRUCTURE.md                # This file - project structure
├── setup.sh                    # Quick setup script
└── run.sh                      # Quick run script

```

## File Descriptions

### Core Application Files

#### `app/main.py`
- FastAPI application initialization
- CORS middleware configuration
- Router registration
- Lifespan events (startup/shutdown)
- Root and health check endpoints

#### `app/config.py`
- Pydantic Settings for environment variables
- Centralized configuration management
- Type-safe settings with validation

### Database Layer

#### `app/database/connection.py`
- SQLAlchemy engine creation
- Session factory setup
- Database dependency injection
- Table initialization

#### `app/database/seed.py`
- Initial humor phrases (greetings, goodbyes, thanks, etc.)
- Personality instructions (tone, expression, emotion, etc.)
- Database seeding functions

### Models

#### `app/models/database_models.py`
**Tables:**
- `humor_phrases` - Cute phrases with categories
- `personality_instructions` - Behavior shaping rules
- `conversation_logs` - Chat history

#### `app/models/schemas.py`
**Pydantic Models:**
- `ChatRequest/Response` - Chat API
- `HumorPhraseCreate/Response` - Humor management
- `PersonalityInstructionCreate/Response` - Personality API
- `HealthCheck` - System health

### Routes (API Endpoints)

#### `app/routes/chat.py`
- `POST /chat/` - Chat with EMO

#### `app/routes/humor.py`
- `POST /humor/phrases` - Add phrase
- `GET /humor/phrases` - List phrases
- `GET /humor/phrases/{id}` - Get phrase
- `PUT /humor/phrases/{id}` - Update phrase
- `DELETE /humor/phrases/{id}` - Delete phrase
- `GET /humor/categories` - List categories
- `GET /humor/stats` - Statistics

#### `app/routes/personality.py`
- `POST /personality/instructions` - Add instruction
- `GET /personality/instructions` - List instructions
- `GET /personality/instructions/{id}` - Get instruction
- `PUT /personality/instructions/{id}` - Update instruction
- `DELETE /personality/instructions/{id}` - Delete instruction
- `GET /personality/types` - List types

### Services

#### `app/services/ai_service.py`
- OpenCode.Zen API integration
- System prompt building from database
- Response generation with BigPickle model
- Fallback handling
- Humor phrase injection

## Configuration Files

### `pyproject.toml`
- UV package manager configuration
- Python dependencies
- Build system configuration

### `.env`
Database, API, and EMO personality settings:
```env
DATABASE_URL=postgresql://...
OPENCODE_ZEN_API_KEY=...
EMO_NAME=EMO
EMO_PERSONALITY=cute_innocent
```

## Scripts

### `setup.sh`
- Checks PostgreSQL
- Creates virtual environment
- Installs dependencies
- Copies .env.example

### `run.sh`
- Activates virtual environment
- Starts uvicorn server

## Data Flow

```
User Request
    ↓
FastAPI Router (chat.py)
    ↓
AI Service (ai_service.py)
    ↓
┌─────────────────────┐
│ 1. Get personality  │
│    from database    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ 2. Build system     │
│    prompt           │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ 3. Add humor        │
│    phrases          │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ 4. Call OpenCode    │
│    Zen API          │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ 5. Log conversation │
│    to database      │
└──────────┬──────────┘
           ↓
Response to User
```

## Database Schema

```sql
-- Humor Phrases Table
CREATE TABLE humor_phrases (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    phrase TEXT NOT NULL,
    context VARCHAR(100),
    cuteness_level INTEGER DEFAULT 5,
    usage_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Personality Instructions Table
CREATE TABLE personality_instructions (
    id SERIAL PRIMARY KEY,
    instruction_type VARCHAR(50) NOT NULL,
    instruction_text TEXT NOT NULL,
    priority INTEGER DEFAULT 1,
    weight FLOAT DEFAULT 1.0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Conversation Logs Table
CREATE TABLE conversation_logs (
    id SERIAL PRIMARY KEY,
    user_input TEXT NOT NULL,
    emo_response TEXT NOT NULL,
    model_used VARCHAR(50),
    response_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Extension Points

Want to add more features? Here's where:

### Add New Routes
1. Create file in `app/routes/`
2. Define router with `APIRouter()`
3. Add endpoints
4. Register in `app/main.py`

### Add New Database Models
1. Add model to `app/models/database_models.py`
2. Create corresponding schema in `app/models/schemas.py`
3. Run migration or restart server

### Add New Services
1. Create file in `app/services/`
2. Implement service class
3. Import and use in routes

### Customize AI Behavior
1. Add to `app/database/seed.py` for defaults
2. Use APIs to add at runtime
3. Adjust weights and priorities

---

*Ready to build? Let's make EMO even cuter! 🤖💕*
