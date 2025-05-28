import requests
import json

# Constants
DEFAULT_MODEL = "gpt-4o-mini"  # Cheapest OpenAI model
USER_ROLE = "user"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

def text_chat(api_key, model=DEFAULT_MODEL):
  """
  Create a text chat function for OpenAI.
  
  Args:
    api_key (str): API key for OpenAI
    model (str): Model name to use (default: gpt-4o-mini - cheapest option)
  
  Returns:
    function: A send_message function that takes a message and returns a response
  """
  def send_message(message):
    # Direct HTTP request to OpenAI API
    headers = {
      "Authorization": f"Bearer {api_key}",
      "Content-Type": "application/json"
    }
    
    payload = {
      "model": model,
      "messages": [{"role": USER_ROLE, "content": message}]
    }
    
    response = requests.post(OPENAI_API_URL, headers=headers, json=payload)
    response.raise_for_status()  # Raise an exception for bad status codes
    
    return response.json()["choices"][0]["message"]["content"]
  
  return send_message
