from django.conf import settings
import requests
import json
import logging
logger= logging.getLogger(__name__)
def generate_ai_summarry(ticket):
    prompt = f"""
                Analyze the following support ticket and return a JSON response with:

                category: C, B, N or T
                priority: H or L
                summarry: short explanation
                suggestion: recommended action

                Ticket:{ticket}
            """
    try:
        logger.info("Calling Open Ai API")
        #print("SETTINGS KEY:", repr(settings.OPENROUTER_API_KEY))
        
        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "Ticket Summary",
        }

        payload = {
            "model": "openai/gpt-4o-mini",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "max_tokens": 200,
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15,
        )

        #print("Headers:", headers)
        #print("Status:", response.status_code)
        #print("Body:", response.text)
        data = response.json()
        #print(data)
        
    except Exception as e:
        print(e)
    return data["choices"][0]["message"]["content"]