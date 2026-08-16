import os
import time
import requests


MODEL = "openai/gpt-oss-20b:free"


def generate_response(messages):

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY is not configured."
        )

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",

        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },

        json={
            "model": MODEL,
            "messages": messages,
        },

        timeout=60,
    )

    if response.status_code == 429:
        raise RuntimeError(
            "OpenRouter rate limit reached. "
            "Please wait a little and try again."
        )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]