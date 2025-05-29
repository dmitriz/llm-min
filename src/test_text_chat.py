"""Tests for text_chat module."""
import os
import pytest

from text_chat import DEFAULT_MODEL, text_chat

# Get API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
  raise EnvironmentError("OPENAI_API_KEY not found in environment. Set it via: export OPENAI_API_KEY=your_key")

def test_openai_chat():
  """Test OpenAI API integration with default model."""
  try:
    chat = text_chat(OPENAI_API_KEY, model=DEFAULT_MODEL)
    result = chat("Hello, OpenAI! Please respond with a brief greeting.")
    
    assert isinstance(result, str), f"Expected str, got {type(result)}"
    assert len(result) > 5, f"Response too short: {len(result)} chars"
    assert result.strip(), "Response is empty or whitespace only"
    assert "hello" in result.lower() or "hi" in result.lower(), "Response doesn't appear to be a greeting"
  except Exception as e:
    pytest.fail(f"OpenAI API test failed: {e}")
