"""Tests for openai_wrapper module."""
import os

import pytest
from dotenv import load_dotenv

from openai_wrapper import openai_wrapper

# Load environment variables from .env file
load_dotenv()
# Get OpenAI API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    pytest.skip("OPENAI_API_KEY environment variable not set")
  raise EnvironmentError("OPENAI_API_KEY not found. Create .env file with OPENAI_API_KEY=your_key")


def test_openai_wrapper_basic():
  """Test OpenAI wrapper with basic input object."""
  # Set up input object with all required data
  input_object = {
    "api_key": OPENAI_API_KEY,
    "model": "gpt-4o-mini",
    "messages": [
      {"role": "user", "content": "Hello, OpenAI! Please respond with a brief greeting."}
    ]
  }
  
  try:
    # Call the wrapper with the input object
    response = openai_wrapper(input_object)
    
    # Test that we get a complete response object (dictionary)
    assert isinstance(response, dict), f"Expected dict, got {type(response)}"
    
    # Test standard OpenAI response structure
    assert "id" in response, "Response missing 'id' field"
    assert "object" in response, "Response missing 'object' field"
    assert "created" in response, "Response missing 'created' field"
    assert "choices" in response, "Response missing 'choices' field"
    assert "usage" in response, "Response missing 'usage' field"
    
    # Test choices structure
    choices = response["choices"]
    assert isinstance(choices, list), "Choices should be a list"
    assert len(choices) > 0, "Choices array is empty"
    
    # Test first choice structure - this is where the actual response content is
    first_choice = choices[0]
    assert "message" in first_choice, "Choice missing 'message' field"
    assert "finish_reason" in first_choice, "Choice missing 'finish_reason' field"
    
    # Test message structure - contains the AI's actual response
    message = first_choice["message"]
    assert "role" in message, "Message missing 'role' field"
    assert "content" in message, "Message missing 'content' field"
    assert message["role"] == "assistant", f"Expected role 'assistant', got {message['role']}"
    
    # Test content quality - the actual text response from AI
    content = message["content"]
    assert isinstance(content, str), f"Expected str content, got {type(content)}"
    assert len(content) > 5, f"Response too short: {len(content)} chars"
    assert content.strip(), "Response is empty or whitespace only"
    
    # Test 'usage' field - important for tracking token consumption and costs
    assert "usage" in response, "Response missing 'usage' field"
    usage = response["usage"]
    assert "prompt_tokens" in usage, "Usage missing 'prompt_tokens' field"
    assert "completion_tokens" in usage, "Usage missing 'completion_tokens' field"
    assert "total_tokens" in usage, "Usage missing 'total_tokens' field"
    
  except Exception as e:
    pytest.fail(f"OpenAI wrapper test failed with {type(e).__name__}: {e}")


def test_openai_wrapper_with_additional_params():
  """Test OpenAI wrapper with additional parameters."""
  input_object = {
    "api_key": OPENAI_API_KEY,
    "model": "gpt-4o-mini",
    "messages": [
      {"role": "user", "content": "Say exactly: 'Testing 123'"}
    ],
    "temperature": 0,
    "max_tokens": 10
  }
  
  try:
    response = openai_wrapper(input_object)
    
    # Basic structure tests
    assert isinstance(response, dict), f"Expected dict, got {type(response)}"
    assert "choices" in response, "Response missing 'choices' field"
    
    # Test that additional params were applied
    content = response["choices"][0]["message"]["content"]
    assert isinstance(content, str), f"Expected str content, got {type(content)}"
    
  except Exception as e:
    pytest.fail(f"OpenAI wrapper with additional params test failed: {e}")


def test_openai_wrapper_missing_fields():
  """Test OpenAI wrapper error handling for missing required fields."""
  # Test missing api_key
  with pytest.raises(ValueError, match="Missing required field: api_key"):
    openai_wrapper({"model": "gpt-4o-mini", "messages": []})
  
  # Test missing model
  with pytest.raises(ValueError, match="Missing required field: model"):
    openai_wrapper({"api_key": "test", "messages": []})
  
  # Test missing messages
  with pytest.raises(ValueError, match="Missing required field: messages"):
    openai_wrapper({"api_key": "test", "model": "gpt-4o-mini"})
