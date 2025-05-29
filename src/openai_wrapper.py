"""OpenAI API wrapper with direct dictionary input/output."""
import httpx
from pydantic import BaseModel, ValidationError
from typing import List, Dict, Any, Optional


class Message(BaseModel):
  """Single message in the conversation."""
  role: str
  content: str


class OpenAIRequest(BaseModel):
  """Schema for OpenAI API request input."""
  api_key: str
  model: str
  messages: List[Message]
  headers: Optional[Dict[str, str]] = None
  timeout: Optional[int] = 10
  # Allow additional fields for OpenAI parameters
  class Config:
    extra = "allow"


def validate_input(input_object: dict) -> OpenAIRequest:
  """
  Validate input object against OpenAI request schema.
  
  Args:
    input_object (dict): Raw input dictionary
    
  Returns:
    OpenAIRequest: Validated request object
    
  Raises:
    ValidationError: If input doesn't match schema
  """
  try:
    return OpenAIRequest(**input_object)
  except ValidationError as e:
    raise ValueError(f"Invalid input object: {e}") from e


def openai_wrapper(input_object: dict) -> dict:
  """
  Generic OpenAI API wrapper that takes a complete request object and returns response.
  
  Args:
    input_object (dict): Complete request configuration including:
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
  validated = validate_input(input_object)
  
  # Create complete request object at once
  request_object = {
    "method": "POST",
    "url": "https://api.openai.com/v1/chat/completions",
    "headers": {
      "Authorization": f"Bearer {validated.api_key}",
      "Content-Type": "application/json",
      **(validated.headers or {})  # Merge additional headers
    },
    "json": {
      "model": validated.model,
      "messages": [msg.dict() for msg in validated.messages],
      # Add any extra fields (temperature, max_tokens, etc.)
      **{k: v for k, v in validated.dict().items() 
         if k not in ["api_key", "headers", "timeout"]}
    },
    "timeout": validated.timeout
  }
  
  # Make the API call using the complete request object
  response = httpx.request(**request_object)
  response.raise_for_status()
  return response.json()
