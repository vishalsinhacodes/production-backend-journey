import os
import json
import re
from openai import OpenAI

from dotenv import load_dotenv


load_dotenv()

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

def summarize_document(text: str) -> dict:
    prompt = f"""
    You are an AI assistant that summarizes documents.
    Return ONLY valid JSON in the following format:
    {{
        "summary": "Short paragraph summary",
        "key_points": ["Point 1", "Point 2"],
        "action_items": ["Action 1", "Action 2"]
    }}
    
    Document:
    {text}
    """
    completion = client.chat.completions.create(
        model=AI_MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a structured summarization assistant."},
            {"role": "user", "content": prompt}                
        ],
        temperature=AI_TEMPERATURE,
    )
    
    content = completion.choices[0].message.content.strip()
    
    # Extract JSON block if extra text exists
    json_match = re.search(r"\{.*\}", content, re.DOTALL)
    if not json_match:
        raise Exception("No valid JSON found in AI response.")
    
    try:
        return json.loads(json_match.group())
    except json.JSONDecodeError:
        raise Exception("Failed to parse AI JSON response.")