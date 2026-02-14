# AI Integration Layer – Groq (OpenAI-Compatible)

## Objective

Integrate a production-ready LLM endpoint into the backend using:

- Groq (OpenAI-compatible API)
- Environment-based configuration
- Proper error propagation
- Separation of service and route layers

---

## Architecture

Client
↓
FastAPI Route (/ai/chat)
↓
AI Service Layer (ai_service.py)
↓
Groq API
↓
Response returned to client

---

## Configuration Strategy

Environment Variables:

- GROQ_API_KEY
- AI_MODEL_NAME (default: llama-3.1-8b-instant)
- AI_TEMPERATURE (default: 0.7)

Configuration loaded via:
python-dotenv

load_dotenv()

---

## Error Handling Design

Service Layer:

- No try/except
- Exceptions bubble upward

Route Layer:

- Catches exceptions
- Raises HTTPException(500)
- Prevents silent failures

This ensures:

- Correct HTTP contract
- No hidden AI failures
- Stable server behavior

---

## Lessons Learned

- Model deprecations require configurable model names
- Environment variables differ between OS session and .env
- load_dotenv requires override=True if variable already exists
- Returning error strings leads to incorrect 200 responses
- Service layer should not swallow exceptions
- Proper HTTP error handling is critical for production APIs

---

## Current Endpoints

POST /ai/chat
POST /health
