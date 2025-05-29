"""OpenAI API wrapper with direct dictionary input/output."""
# HTTP client for making API requests
# Type hints
from typing import Any, Dict, List, Optional, Union

import httpx
# Data validation and parsing
from pydantic import BaseModel, ValidationError

# Constants
DEFAULT_TIMEOUT = 10


class Message(BaseModel):
  """Single message in conversation with AI model via OpenAI API."""
  role: str
  # Content can be string or dict to support future features (images, etc.)
  content: Union[str, Dict[str, Any]]


class OpenAIRequest(BaseModel):
  """Schema for OpenAI API request input."""
  api_key: str
  model: str
  messages: List[Message]
  # Empty dict is more consistent than None
  headers: Optional[Dict[str, str]] = {}
  timeout: Optional[int] = DEFAULT_TIMEOUT
  

def validate_input(input_object: dict) -> bool:
  """
  Validate input object against OpenAI request schema.
  
  Args:
    input_object (dict): Raw input dictionary
    
  Returns:
    bool: True if valid, raises ValueError if invalid
    
  Raises:
    ValueError: If input doesn't match schema
  """
  try:
    OpenAIRequest(**input_object)
    return True
  except ValidationError as e:
    # Parse validation errors to provide specific field missing messages
    for error in e.errors():
      if error['type'] == 'missing':
        field_name = error['loc'][0] if error['loc'] else 'unknown'
        raise ValueError(f"Missing required field: {field_name}") from e
    # Fallback for other validation errors
    raise ValueError(f"Invalid input object: {e}") from e


def openai_wrapper(input_object: dict) -> dict:
  """
  Generic OpenAI API wrapper that takes a complete input object and returns response.
  
  Args:
    input_object (dict): Complete input configuration including:
      - api_key (str): OpenAI API key
      - model (str): Model name
      - messages (list): List of message objects with role and content
      - headers (dict, optional): Additional headers to merge
      - timeout (int, optional): Request timeout in seconds
      - Any additional OpenAI parameters (temperature, max_tokens, etc.)
      
  Returns:
    dict: Complete API response object as returned by OpenAI
    
  Raises:
    ValueError: If input object is malformed
    httpx.HTTPStatusError: If HTTP request fails
  """
  # Validate input using Pydantic schema
  validate_input(input_object)
  
  # Extract extra OpenAI parameters (temperature, max_tokens, etc.)
  
  # Create complete request object for HTTP call
  request_object = {
    "method": "POST",
    "url": "https://api.openai.com/v1/chat/completions",
    "headers": {
      "Authorization": f"Bearer {input_object['api_key']}",
      "Content-Type": "application/json",
      # Merge additional headers with defaults
      **input_object.get("headers", {})
    },
    # API payload for the request body
    "json": {
      "model": input_object["model"],
      "messages": input_object["messages"],
      # Merge extra OpenAI parameters
      **{k: v for k, v in input_object.items() 
          if k not in ["api_key", "headers", "timeout"]}
    },
    # Request timeout with default fallback
    "timeout": input_object.get("timeout", DEFAULT_TIMEOUT)
  }
  
  # Make the API call using the complete request object
  response = httpx.request(**request_object)
  # Raises HTTPStatusError if status code indicates error
  response.raise_for_status()
  return response.json()
