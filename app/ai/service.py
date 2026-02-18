import os
import json
import re
import logging
import time

from openai import OpenAI
from fastapi import HTTPException


from app.config import *

logger = logging.getLogger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
AI_MODEL_NAME = os.getenv("AI_MODEL_NAME", "llama-3.1-8b-instant")
AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", "0.7"))

if not GROQ_API_KEY:
    raise Exception("GROQ_API_KEY is not set in environment variables.")

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
    timeout=10
)

def chat_with_ai(user_message: str, request_id: str) -> str:
    start_time = time.time()
    logger.info(f"request_id={request_id} Chat LLM call started")
    
    try:
        completion = client.chat.completions.create(
            model=AI_MODEL_NAME,
            messages=[
                {"role": "system", "content":"You are a helpful AI assistant."},
                {"role": "user", "content": user_message}
            ],
            temperature=AI_TEMPERATURE
        )
        
        llm_duration = time.time() - start_time
        logger.info(
            f"request_id={request_id} "
            f"Chat LLM call completed in {llm_duration:.2f}s"
        )
        
        return completion.choices[0].message.content
    except Exception as e:
        logger.error("LLM call timed out")
        if "timeout" in str(e).lower():
            raise HTTPException(status_code=504, detail="AI service timeout.")
        raise HTTPException(status_code=500, detail="AI service error.")
        

def summarize_document(text: str, request_id: str) -> dict:
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
    
    start_time = time.time()
    logger.info(f"request_id={request_id} Summerize LLM call started")
    
    try:
        completion = client.chat.completions.create(
            model=AI_MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a structured summarization assistant."},
                {"role": "user", "content": prompt}                
            ],
            temperature=AI_TEMPERATURE,
        )
        
        llm_duration = time.time() - start_time
        logger.info(
            f"request_id={request_id} "
            f"Summerize LLM call completed in {llm_duration:.2f}s"
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
    except Exception as e:
        logger.error("LLM call timed out")
        if "timeout" in str(e).lower():
            raise HTTPException(status_code=504, detail="AI service timeout.")
        raise HTTPException(status_code=500, detail="AI service error.")