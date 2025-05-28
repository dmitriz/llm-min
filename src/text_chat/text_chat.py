# text_chat.py

import openai
import requests

def text_chat(api_key, model, provider="openai"):
    """
    Create a text chat function for different LLM providers.
    
    Args:
        api_key (str): API key for the provider
        model (str): Model name to use
        provider (str): Provider name ("openai" or "grok")
    
    Returns:
        function: A send_message function that takes a message and returns a response
    """
    if provider == "openai":
        def send_message(message):
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": message}]
            )
            return response.choices[0].message.content

    elif provider == "grok":
        def send_message(message):
            response = requests.post(
                "https://api.grok.x.ai/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": message}]
                }, 
            timeout=60)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

    else:
        raise ValueError(f"Unknown provider: {provider}")

    return send_message
