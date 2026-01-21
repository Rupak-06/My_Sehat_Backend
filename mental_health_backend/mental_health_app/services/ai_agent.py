import os
import json
import re
from typing import Dict, Any, List
from openai import OpenAI
from datetime import datetime

# Initialize client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

SYSTEM_PROMPT = """You are a mental health support AI.

Rules:
- Be warm, calm, non-judgmental.
- Act like a supportive friend with professional calmness.
- Detect self-harm or suicidal intent.
- Give practical, safe advice.
- Encourage real-world support if risk is high.

Return ONLY valid JSON in this exact format:
{
  "risk_level": "none | low | medium | high | critical",
  "self_harm_detected": true/false,
  "reply": "what the user sees",
  "advice": ["step 1", "step 2", "step 3"]
}
"""

def extract_json(text: str) -> Dict[str, Any]:
    """
    Robust JSON extraction from LLM output.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Attempt repair: find first { and last }
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except (json.JSONDecodeError, AttributeError):
        pass
        
    raise ValueError("Could not parse JSON")

FALLBACK_ERROR_MESSAGE = "I’m here with you. Something went wrong with my thought process, but I want to support you. Can you tell me more?"

def build_fallback_response(user_msg: str) -> Dict[str, Any]:
    return {
        "risk_level": "medium",
        "self_harm_detected": False,
        "reply": FALLBACK_ERROR_MESSAGE,
        "advice": [
            "Take a slow breath",
            "Reach out to a trusted friend",
            "Focus on the present moment"
        ]
    }

def analyze_message_llm(user_message: str) -> Dict[str, Any]:
    if not os.getenv("GROQ_API_KEY"):
        print("WARNING: GROQ_API_KEY not set, returning fallback")
        return build_fallback_response(user_message)

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f'User message: """{user_message}"""'}
            ],
            temperature=0.4
        )
        
        ai_text = completion.choices[0].message.content
        return extract_json(ai_text)
        
    except Exception as e:
        print("LLM ERROR:", e)
        return build_fallback_response(user_message)

def summarize_day_llm(answers: Dict[str, str]) -> Dict[str, Any]:
    """
    Summarize daily check-in answers.
    """
    formatted_answers = "\n".join([f"{k}: {v}" for k, v in answers.items()])
    
    prompt = f"""
    Analyze these daily check-in answers for a user's mental health context:
    {formatted_answers}
    
    Return ONLY valid JSON:
    {{
        "daily_summary": "Short 2-sentence supportive summary of their state",
        "risk_level": "none | low | medium | high | critical",
        "self_harm_detected": true/false,
        "advice": ["advice 1", "advice 2"],
        "reply": "A short comforting message to show immediately"
    }}
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a compassionate mental health assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        ai_text = completion.choices[0].message.content
        return extract_json(ai_text)
    except Exception as e:
        print("LLM SUMMARY ERROR:", e)
        return {
            "daily_summary": "Unable to generate summary at this moment.",
            "risk_level": "medium",
            "self_harm_detected": False,
            "advice": ["Get some rest", "Stay hydrated"],
            "reply": "Thank you for checking in. Take care of yourself today."
        }
