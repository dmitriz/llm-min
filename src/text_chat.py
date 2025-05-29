import httpx

# Constants
DEFAULT_MODEL = "gpt-4o-mini"  # Cheapest OpenAI model
USER_ROLE = "user"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

def create_request_object(api_key: str, model: str, message: str) -> dict:
  """
  Constructs a dictionary representing an HTTP POST request to the OpenAI chat completions API.
  
  The returned dictionary includes the request method, endpoint URL, authorization headers, and a JSON payload containing the specified model and user message.
  
  Args:
      api_key: The OpenAI API key for authentication.
      model: The name of the OpenAI model to use.
      message: The user message to send in the chat.
  
  Returns:
      A dictionary suitable for use with HTTP client libraries to send a chat completion request.
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
  Sends an HTTP request to the OpenAI API and returns the generated message content.
  
  Raises:
      httpx.HTTPStatusError: If the HTTP request fails.
      ValueError: If the API response is missing expected fields or is improperly formatted.
  
  Returns:
      The content of the first message choice from the API response.
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
  Creates a reusable chat function for sending messages to the OpenAI API.
  
  Args:
      api_key: The OpenAI API key.
      model: The model name to use for chat completions.
  
  Returns:
      A function that takes a message string and returns the generated response from the OpenAI chat completions API.
  """
  def send_message(message):
    # Create complete request object
    """
    Sends a user message to the OpenAI chat completions API and returns the generated response.
    
    Args:
        message: The user message to send to the chat model.
    
    Returns:
        The content of the model's response as a string.
    
    Raises:
        httpx.HTTPStatusError: If the HTTP request fails.
        ValueError: If the API response format is invalid or missing expected fields.
    """
    request_obj = create_request_object(api_key, model, message)
    
    # Send single HTTP request with the request object
    return send_http_request(request_obj)
  
  return send_message
