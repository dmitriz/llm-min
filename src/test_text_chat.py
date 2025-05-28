"""Tests for text_chat module."""
from pathlib import Path
from text_chat import text_chat, DEFAULT_MODEL

# Simple and clean - just read the key directly
secrets_file = Path(__file__).parent.parent / ".secrets" / "openai.py"
OPENAI_API_KEY = secrets_file.read_text().split('"')[1]

def test_openai_chat():
    """Test OpenAI API integration with default model."""
    chat = text_chat(OPENAI_API_KEY, model=DEFAULT_MODEL)
    result = chat("Hello, OpenAI! Please respond with a brief greeting.")
    
    assert isinstance(result, str)
    assert len(result) > 5
    assert result.strip()  # Ensure response is not just whitespace
