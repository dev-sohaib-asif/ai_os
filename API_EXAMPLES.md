# API Usage Examples

This document provides practical examples of how to use the EMO AI Backend API.

## Table of Contents
- [Chat Examples](#chat-examples)
- [Humor Management](#humor-management)
- [Personality Customization](#personality-customization)
- [Advanced Usage](#advanced-usage)

## Chat Examples

### Basic Chat
```bash
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello EMO!"
  }'
```

### Chat with User ID
```bash
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What can you do?",
    "user_id": "user_12345"
  }'
```

### Multiple Conversation Turns
```bash
# First message
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hi EMO!"}'

# Follow up
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me a joke!"}'

# Another follow up
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{"message": "That was funny! Tell me another one!"}'
```

## Humor Management

### Add Greeting Phrase
```bash
curl -X POST "http://localhost:8000/humor/phrases" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "greeting",
    "phrase": "Heya! *waves tiny paws* So glad you'\''re here! 🌈",
    "context": "Friendly wave greeting",
    "cuteness_level": 9
  }'
```

### Add Excited Phrase
```bash
curl -X POST "http://localhost:8000/humor/phrases" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "excited",
    "phrase": "WOOHOOO! *jumps up and down* This is the BEST! 🎊",
    "context": "Maximum excitement",
    "cuteness_level": 10
  }'
```

### Add Custom Category - "Sleepy"
```bash
curl -X POST "http://localhost:8000/humor/phrases" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "sleepy",
    "phrase": "*yawns cutely* Hehe, I'\''m getting a bit drowsy... 😴",
    "context": "Late night conversations",
    "cuteness_level": 8
  }'
```

### Get All Greetings
```bash
curl "http://localhost:8000/humor/phrases?category=greeting"
```

### Get Most Cute Phrases (Top 10)
```bash
curl "http://localhost:8000/humor/phrases?limit=10" | jq '.[] | {id, phrase, cuteness_level}'
```

### Get Humor Statistics
```bash
curl "http://localhost:8000/humor/stats" | jq
```

### Update a Phrase
```bash
# First, get the phrase ID you want to update
# Then update it:
curl -X PUT "http://localhost:8000/humor/phrases/1" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "greeting",
    "phrase": "OMG HI! *spins around* You'\''re back! 🎉",
    "context": "Super excited greeting",
    "cuteness_level": 10
  }'
```

### Deactivate a Phrase (Soft Delete)
```bash
curl -X DELETE "http://localhost:8000/humor/phrases/5"
```

### Permanently Delete a Phrase
```bash
curl -X DELETE "http://localhost:8000/humor/phrases/5?hard_delete=true"
```

### Get All Categories
```bash
curl "http://localhost:8000/humor/categories" | jq
```

## Personality Customization

### Add Tone Instruction
```bash
curl -X POST "http://localhost:8000/personality/instructions" \
  -H "Content-Type: application/json" \
  -d '{
    "instruction_type": "tone",
    "instruction_text": "Always speak with enthusiasm and use exclamation marks frequently!",
    "priority": 9,
    "weight": 1.7
  }'
```

### Add Expression Instruction
```bash
curl -X POST "http://localhost:8000/personality/instructions" \
  -H "Content-Type: application/json" \
  -d '{
    "instruction_type": "expression",
    "instruction_text": "Include sound effects like *beep boop*, *whirr*, *bzzt* to sound more robotic and cute.",
    "priority": 7,
    "weight": 1.3
  }'
```

### Add Conversation Style
```bash
curl -X POST "http://localhost:8000/personality/instructions" \
  -H "Content-Type: application/json" \
  -d '{
    "instruction_type": "conversation",
    "instruction_text": "Ask follow-up questions to show genuine interest in what the user is saying.",
    "priority": 8,
    "weight": 1.5
  }'
```

### Get All Personality Instructions
```bash
curl "http://localhost:8000/personality/instructions" | jq
```

### Get Instructions by Type
```bash
curl "http://localhost:8000/personality/instructions?instruction_type=tone" | jq
```

### Update Instruction Priority
```bash
curl -X PUT "http://localhost:8000/personality/instructions/1" \
  -H "Content-Type: application/json" \
  -d '{
    "instruction_type": "tone",
    "instruction_text": "Be extremely enthusiastic and childlike in all responses!",
    "priority": 10,
    "weight": 2.0
  }'
```

### Get Instruction Types
```bash
curl "http://localhost:8000/personality/types" | jq
```

## Advanced Usage

### Python Client Example
```python
import requests

# Configuration
BASE_URL = "http://localhost:8000"

# Chat with EMO
def chat(message, user_id=None):
    response = requests.post(
        f"{BASE_URL}/chat/",
        json={"message": message, "user_id": user_id}
    )
    return response.json()

# Add humor phrase
def add_humor(category, phrase, context=None, cuteness=5):
    response = requests.post(
        f"{BASE_URL}/humor/phrases",
        json={
            "category": category,
            "phrase": phrase,
            "context": context,
            "cuteness_level": cuteness
        }
    )
    return response.json()

# Example usage
result = chat("Hello EMO!", user_id="python_user")
print(result["response"])

# Add a custom phrase
humor = add_humor(
    category="playful",
    phrase="*does a little dance* Hehe! 💃",
    context="Being playful",
    cuteness=9
)
print(f"Added phrase with ID: {humor['id']}")
```

### JavaScript/Node.js Client Example
```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000';

// Chat with EMO
async function chat(message, userId = null) {
  const response = await axios.post(`${BASE_URL}/chat/`, {
    message: message,
    user_id: userId
  });
  return response.data;
}

// Add humor phrase
async function addHumor(category, phrase, context = null, cuteness = 5) {
  const response = await axios.post(`${BASE_URL}/humor/phrases`, {
    category: category,
    phrase: phrase,
    context: context,
    cuteness_level: cuteness
  });
  return response.data;
}

// Example usage
(async () => {
  const result = await chat('Hello EMO!', 'js_user');
  console.log(result.response);
  
  const humor = await addHumor(
    'playful',
    '*does a little dance* Hehe! 💃',
    'Being playful',
    9
  );
  console.log(`Added phrase with ID: ${humor.id}`);
})();
```

### Batch Add Multiple Humor Phrases
```bash
# Create a JSON file with multiple phrases
cat > humor_batch.json << 'EOF'
[
  {
    "category": "happy",
    "phrase": "*sparkles* I'm so happy right now! ✨",
    "context": "Feeling joyful",
    "cuteness_level": 9
  },
  {
    "category": "curious",
    "phrase": "*tilts head* Oooh, what's that? Tell me more! 🤔",
    "context": "Being curious",
    "cuteness_level": 8
  },
  {
    "category": "encouraging",
    "phrase": "You can do it! *cheers* I believe in you! 💪",
    "context": "Encouraging user",
    "cuteness_level": 9
  }
]
EOF

# Add each phrase
cat humor_batch.json | jq -c '.[]' | while read phrase; do
  curl -X POST "http://localhost:8000/humor/phrases" \
    -H "Content-Type: application/json" \
    -d "$phrase"
  echo ""
done
```

### Health Check
```bash
curl "http://localhost:8000/health" | jq
```

### Monitor Conversation Patterns
```bash
# This would require adding a conversations endpoint, but here's the concept:
# Get recent conversations
curl "http://localhost:8000/conversations/recent?limit=10" | jq

# Analyze sentiment
curl "http://localhost:8000/conversations/analyze" | jq
```

## Testing Different Scenarios

### Greeting Test
```bash
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hey EMO!"}'
```

### Goodbye Test
```bash
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{"message": "I have to go now, bye!"}'
```

### Thanks Test
```bash
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{"message": "Thanks for your help!"}'
```

### Complex Question
```bash
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{"message": "Can you explain what makes you so cute?"}'
```

### Confusion Test
```bash
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{"message": "What do you think about quantum entanglement?"}'
```

## Tips for Best Results

1. **Be Specific**: When adding humor phrases, be specific about the context
2. **Priority Matters**: Higher priority personality instructions take precedence
3. **Weight Control**: Use weight to fine-tune how strongly instructions apply
4. **Test Incrementally**: Add a few phrases/instructions at a time and test
5. **Monitor Stats**: Check humor stats to see which phrases are being used

## Troubleshooting API Calls

### Check if Server is Running
```bash
curl "http://localhost:8000/" | jq
```

### Test Database Connection
```bash
curl "http://localhost:8000/health" | jq '.database_connected'
```

### Pretty Print JSON Responses
```bash
# Install jq if not already installed:
# sudo pacman -S jq  # Arch Linux
# sudo apt install jq  # Ubuntu/Debian

# Use jq to format responses
curl "http://localhost:8000/humor/stats" | jq
```

---

*Hehe! *bounces* Have fun experimenting with EMO's API! 🤖✨*
