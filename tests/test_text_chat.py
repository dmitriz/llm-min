"""Tests for text_chat module."""
import sys
import os
from pathlib import Path

# Add src to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from text_chat import text_chat, DEFAULT_MODEL

# Import API key
secrets_file = project_root / ".secrets" / "openai.py"
secrets_globals = {}
with open(secrets_file, 'r') as f:
    exec(f.read(), secrets_globals)
OPENAI_API_KEY = secrets_globals['OPENAI_API_KEY']


def test_openai_chat():
    """Test OpenAI API integration with default model."""
    chat = text_chat(OPENAI_API_KEY, model=DEFAULT_MODEL)
    result = chat("Hello, OpenAI! Please respond with a brief greeting.")
    
    assert isinstance(result, str)
    assert len(result) > 5
    assert result.strip()  # Ensure response is not just whitespace


def test_chat_with_custom_model():
    """Test chat with explicit model specification."""
    chat = text_chat(OPENAI_API_KEY, model="gpt-3.5-turbo")
    result = chat("Say 'test passed' if you can read this.")
    
    assert isinstance(result, str)
    assert len(result) > 0
