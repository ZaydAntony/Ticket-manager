from django.conf import settings
import requests
import json

def generate_ai_summarry(ticket):
    prompt = f"""
                Analyze the following support ticket and return a JSON response with:

                category: C, B, N or T
                priority: H or L
                summarry: short explanation
                suggestion: recommended action

                Ticket:{ticket}
            """

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "Ticket Summarry"
        },
        json={
            "model": "openai/gpt-4o-mini",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 200,
            "response_format": {"type": "json_object"},
        },
        timeout=15
    )

    data = response.json()
    return data["choices"][0]["message"]["content"]