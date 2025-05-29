"""OpenAI API wrapper with direct dictionary input/output."""
import httpx


def openai_wrapper(input_object: dict) -> dict:
  """
  Generic OpenAI API wrapper that takes a complete request object and returns response.
  
  Args:
    input_object (dict): Complete request configuration including:
      - api_key (str): OpenAI API key
      - model (str): Model name
      - messages (list): List of message objects
      - headers (dict, optional): Additional headers
      - timeout (int, optional): Request timeout in seconds
      
  Returns:
    dict: Complete API response object as returned by OpenAI
    
  Raises:
    httpx.HTTPStatusError: If HTTP request fails
    ValueError: If input object is malformed
  """
  # Extract required fields
  api_key = input_object.get("api_key")
  if not api_key:
    raise ValueError("Missing required field: api_key")
    
  model = input_object.get("model")
  if not model:
    raise ValueError("Missing required field: model")
    
  messages = input_object.get("messages")
  if not messages:
    raise ValueError("Missing required field: messages")
  
  # Build headers
  headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
  }
  
  # Add any additional headers from input
  if "headers" in input_object:
    headers.update(input_object["headers"])
  
  # Build request payload
  payload = {
    "model": model,
    "messages": messages
  }
  
  # Add any additional payload fields (temperature, max_tokens, etc.)
  for key, value in input_object.items():
    if key not in ["api_key", "headers", "timeout"] and key not in payload:
      payload[key] = value
  
  # Get timeout
  timeout = input_object.get("timeout", 10)
  
  # Make the request
  response = httpx.post(
    "https://api.openai.com/v1/chat/completions",
    headers=headers,
    json=payload,
    timeout=timeout
  )
  
  response.raise_for_status()
  return response.json()
