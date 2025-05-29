import httpx

# Constants
DEFAULT_MODEL = "gpt-4o-mini"  # Cheapest OpenAI model
USER_ROLE = "user"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

def create_request_object(api_key: str, model: str, message: str) -> dict:
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
  
  Raises:
    httpx.HTTPStatusError: If HTTP request fails
    ValueError: If API response format is unexpected
  """
  response = httpx.request(**request_object, timeout=10)
  response.raise_for_status()

  try:
    data = response.json()
    choices = data.get("choices", [])
    if not choices:
      raise ValueError("Empty choices array in API response")
    
    message = choices[0].get("message", {})
    content = message.get("content")
    if content is None:
      raise ValueError("Missing 'content' in API response")
      
    return content
  except (KeyError, IndexError) as e:
    raise ValueError(f"Unexpected API response format: {e}") from e

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
