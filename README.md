# 🤖 EMO AI Backend

A cute and innocent AI companion backend that mimics the adorable personality of EMO AI! Built with FastAPI, PostgreSQL, and powered by free AI models from OpenCode.Zen.

## ✨ Features

- 💬 **Text Generation**: Chat with EMO using BigPickle model from OpenCode.Zen
- 😊 **Customizable Humor**: Store and manage cute phrases in PostgreSQL
- 🎭 **Personality System**: Shape EMO's behavior with custom instructions
- 📊 **Conversation Logging**: Track all interactions for learning
- 🔧 **REST API**: Complete API for integration with any frontend

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 12+
- UV package manager
- OpenCode.Zen API key (get it free from https://opencode.zen)

### 1. Install UV (if not installed)

```bash
# On Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Setup PostgreSQL

```bash
# Install PostgreSQL (Arch Linux example)
sudo pacman -S postgresql

# Initialize database
sudo -u postgres initdb -D /var/lib/postgres/data

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql
```

In PostgreSQL console:
```sql
CREATE DATABASE emo_ai_db;
CREATE USER emo_user WITH PASSWORD 'emo_password';
GRANT ALL PRIVILEGES ON DATABASE emo_ai_db TO emo_user;
\q
```

### 3. Clone and Setup Project

```bash
# Navigate to project directory
cd emo-ai-backend

# Create virtual environment with UV
uv venv

# Activate virtual environment
source .venv/bin/activate  # On Linux/macOS
# .venv\Scripts\activate   # On Windows

# Install dependencies
uv pip install -e .
```

### 4. Configure Environment

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your OpenCode.Zen API key
nano .env
```

Update these values in `.env`:
```bash
DATABASE_URL=postgresql://emo_user:emo_password@localhost:5432/emo_ai_db
OPENCODE_ZEN_API_KEY=your_actual_api_key_here
```

### 5. Run the Application

```bash
# Make sure you're in the project directory
cd /path/to/emo-ai-backend

# Run with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or run directly:
```bash
python -m app.main
```

### 6. Access the API

- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 📚 API Endpoints

### Chat
- `POST /chat/` - Chat with EMO (send message, get cute response)

### Humor Management
- `POST /humor/phrases` - Add new humor phrase
- `GET /humor/phrases` - Get all humor phrases
- `GET /humor/phrases/{id}` - Get specific phrase
- `PUT /humor/phrases/{id}` - Update phrase
- `DELETE /humor/phrases/{id}` - Delete/deactivate phrase
- `GET /humor/categories` - Get all phrase categories
- `GET /humor/stats` - Get humor database statistics

### Personality Management
- `POST /personality/instructions` - Add personality instruction
- `GET /personality/instructions` - Get all instructions
- `GET /personality/instructions/{id}` - Get specific instruction
- `PUT /personality/instructions/{id}` - Update instruction
- `DELETE /personality/instructions/{id}` - Delete/deactivate instruction
- `GET /personality/types` - Get instruction types

### System
- `GET /` - Welcome message
- `GET /health` - Health check

## 💬 Example Usage

### Chat with EMO

```bash
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello EMO!",
    "user_id": "user123"
  }'
```

Response:
```json
{
  "response": "Hiii! *bounces happily* Yay, a friend! 💕 How are you doing today?",
  "model_used": "bigpickle",
  "response_time_ms": 1234,
  "timestamp": "2026-01-14T10:30:00"
}
```

### Add Custom Humor

```bash
curl -X POST "http://localhost:8000/humor/phrases" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "excited",
    "phrase": "OMG! *spins in circles* This is AMAZING! 🎉",
    "context": "When something awesome happens",
    "cuteness_level": 10
  }'
```

### Add Personality Instruction

```bash
curl -X POST "http://localhost:8000/personality/instructions" \
  -H "Content-Type: application/json" \
  -d '{
    "instruction_type": "tone",
    "instruction_text": "Always end responses with a question to keep the conversation going",
    "priority": 8,
    "weight": 1.5
  }'
```

## 🎨 Customization

### Adding More Humor Categories

EMO comes with these categories:
- `greeting` - Hello/Hi responses
- `goodbye` - Bye/See you later
- `thanks` - Thank you responses
- `excited` - Super excited reactions
- `confused` - Cute confusion
- `error` - Error/apology messages

Add your own:
```python
# Use the API or add directly to database
{
  "category": "sleepy",
  "phrase": "*yawns* Hehe, I'm getting a bit sleepy! 😴",
  "context": "When tired or late at night",
  "cuteness_level": 8
}
```

### Tuning Personality

Adjust EMO's personality by modifying instructions:
- **Priority** (1-10): How important the instruction is
- **Weight** (0.1-2.0): How strongly to apply it
- Higher priority instructions are included first in the system prompt
- Higher weight instructions are emphasized more

## 🗄️ Database Schema

### Tables

**humor_phrases**
- Stores all cute phrases EMO can use
- Tracks usage count for popularity
- Can be activated/deactivated

**personality_instructions**
- Core personality rules and behaviors
- Priority-based system for importance
- Weight system for strength of application

**conversation_logs**
- Every chat interaction logged
- Tracks response times
- Useful for analytics and learning

## 🔧 Development

### Project Structure

```
emo-ai-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Settings management
│   ├── database/
│   │   ├── connection.py    # Database setup
│   │   └── seed.py          # Database seeding
│   ├── models/
│   │   ├── database_models.py  # SQLAlchemy models
│   │   └── schemas.py       # Pydantic schemas
│   ├── routes/
│   │   ├── chat.py          # Chat endpoints
│   │   ├── humor.py         # Humor management
│   │   └── personality.py   # Personality management
│   └── services/
│       └── ai_service.py    # AI integration
├── .env                     # Environment variables
├── .env.example            # Example env file
├── pyproject.toml          # Project dependencies
└── README.md               # This file
```

### Running Tests

```bash
# Install test dependencies
uv pip install pytest pytest-asyncio

# Run tests (when available)
pytest
```

## 🌟 Future Enhancements

- [ ] Voice synthesis integration (TTS)
- [ ] Speech recognition (STT)
- [ ] Emotion detection from text
- [ ] Multi-user support with user profiles
- [ ] WebSocket support for real-time chat
- [ ] Frontend web interface
- [ ] Mobile app integration
- [ ] Custom model fine-tuning
- [ ] Sentiment analysis
- [ ] Multi-language support

## 🤝 Contributing

This is an open project! Feel free to:
- Add more humor phrases
- Improve personality instructions
- Add new features
- Fix bugs
- Improve documentation

## 📝 License

MIT License - Feel free to use this for your own cute AI projects!

## 🙏 Acknowledgments

- Inspired by the adorable EMO AI robot by Living.AI
- Powered by OpenCode.Zen's free AI models
- Built with FastAPI, PostgreSQL, and love 💕

## 💡 Tips

1. **Start Simple**: Begin with basic chat, then add more humor gradually
2. **Monitor Stats**: Check `/humor/stats` to see which phrases are popular
3. **Adjust Personality**: Fine-tune instructions based on conversations
4. **Temperature**: Lower temperature (0.5-0.7) = more consistent, higher (0.8-1.0) = more creative
5. **Cuteness Level**: Use this to prioritize certain phrases over others

## 🆘 Troubleshooting

### Database Connection Error
- Make sure PostgreSQL is running: `sudo systemctl status postgresql`
- Verify credentials in `.env` match your PostgreSQL setup
- Check database exists: `psql -U emo_user -d emo_ai_db`

### API Key Error
- Verify your OpenCode.Zen API key is correct
- Check the base URL is correct
- Make sure the model name is "bigpickle"

### Import Errors
- Activate virtual environment: `source .venv/bin/activate`
- Reinstall dependencies: `uv pip install -e .`

---

Made with 💕 by the EMO AI Community

*Hehe! *bounces* Have fun with EMO! 🤖✨*
