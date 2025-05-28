# test_text_chat.py

from src.text_chat import text_chat
import os
import pytest

def test_grok():
    """Test Grok API integration"""
    api_key = os.getenv("GROK_API_KEY")
    if not api_key:
        pytest.skip("GROK_API_KEY environment variable not set")
    
    chat = text_chat(api_key, "grok-1", provider="grok")
    result = chat("Hello, Grok!")
    assert isinstance(result, str)
    assert len(result) > 0
    print("✅ Test passed. Response:", result)

def test_openai():
    """Test OpenAI API integration"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY environment variable not set")
    
    chat = text_chat(api_key, "gpt-3.5-turbo", provider="openai")
    result = chat("Hello, OpenAI!")
    assert isinstance(result, str)
    assert len(result) > 0
    print("✅ Test passed. Response:", result)

def test_invalid_provider():
    """Test that invalid provider raises ValueError"""
    with pytest.raises(ValueError, match="Unknown provider: invalid"):
        text_chat("fake-key", "fake-model", provider="invalid")

if __name__ == "__main__":
    # Run tests manually if called directly
    test_invalid_provider()
    print("✅ Invalid provider test passed")
    
    # Try real API tests only if keys are available
    if os.getenv("GROK_API_KEY"):
        test_grok()
    else:
        print("⚠️ Skipping Grok test - GROK_API_KEY not set")
    
    if os.getenv("OPENAI_API_KEY"):
        test_openai()
    else:
        print("⚠️ Skipping OpenAI test - OPENAI_API_KEY not set")
