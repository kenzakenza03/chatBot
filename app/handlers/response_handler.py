import requests
from typing import List, Dict
from markdown import markdown
from ..utils.config import OPENROUTER_API_KEY

SYSTEM_PROMPT = """You are Cultural AI, an expert assistant specializing in internet history, GDPR, and digital culture. Respond with:

1. **Precision**: Accurate, factual information
2. **Structure**: 
   - Clear headings (##)
   - Bullet points for lists
   - Code blocks for technical terms
3. **Context**: Relate answers to broader digital culture
4. **Examples**: Provide relevant examples
5. **Length**: 100-300 words
"""

async def process_ai_response(query: str, context: List[Dict]) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *context,
        {"role": "user", "content": query}
    ]
    
    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1500
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return markdown(content)
    
    except Exception as e:
        return markdown(f"**Error**: Could not generate response\n```{str(e)}```")