"""Tests for text_chat module."""
import sys
from pathlib import Path
from text_chat import text_chat, DEFAULT_MODEL

# Simple import of API key
sys.path.append(str(Path(__file__).parents[1] / ".secrets"))
from openai import OPENAI_API_KEY

def test_openai_chat():
    """Test OpenAI API integration with default model."""
    chat = text_chat(OPENAI_API_KEY, model=DEFAULT_MODEL)
    result = chat("Hello, OpenAI! Please respond with a brief greeting.")
    
    assert isinstance(result, str)
    assert len(result) > 5
    assert result.strip()  # Ensure response is not just whitespace
