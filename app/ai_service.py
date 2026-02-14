import os
from openai import OpenAI

from dotenv import load_dotenv


load_dotenv()

print("GROQ_API_KEY from env:", os.getenv("GROQ_API_KEY"))


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
AI_MODEL_NAME = os.getenv("AI_MODEL_NAME", "llama-3.1-8b-instant")
AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", "0.7"))

if not GROQ_API_KEY:
    raise Exception("GROQ_API_KEY is not set in environment variables.")

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def chat_with_ai(user_message: str) -> str:
    completion = client.chat.completions.create(
        model=AI_MODEL_NAME,
        messages=[
            {"role": "system", "content":"You are a helpful AI assistant."},
            {"role": "user", "content": user_message}
        ],
        temperature=AI_TEMPERATURE
    )
    
    return completion.choices[0].message.content