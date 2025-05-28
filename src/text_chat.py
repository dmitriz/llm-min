import requests
import json

# Constants
DEFAULT_MODEL = "gpt-4o-mini"  # Cheapest OpenAI model
USER_ROLE = "user"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

def create_request_object(api_key, model, message):
  """
  Create a complete HTTP request object for OpenAI API.
  
  Args:
    api_key (str): API key for OpenAI
    model (str): Model name to use
    message (str): User message
    
  Returns:
    dict: Complete request object with method, url, headers, and json payload
  """
  return {
    "method": "POST",
    "url": OPENAI_API_URL,
    "headers": {
      "Authorization": f"Bearer {api_key}",
      "Content-Type": "application/json"
    },
    "json": {
      "model": model,
      "messages": [{"role": USER_ROLE, "content": message}]
    }
  }

def send_http_request(request_object):
  """
  Send HTTP request using the request object.
  
  Args:
    request_object (dict): Complete request object
    
  Returns:
    str: Response content from OpenAI
  """
  response = requests.request(**request_object)
  response.raise_for_status()
  return response.json()["choices"][0]["message"]["content"]

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
    # Create complete request object
    request_obj = create_request_object(api_key, model, message)
    
    # Send single HTTP request with the request object
    return send_http_request(request_obj)
  
  return send_message
