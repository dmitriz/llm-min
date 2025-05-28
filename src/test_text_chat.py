from text_chat import text_chat, DEFAULT_MODEL
import sys
import os
from .secrets.openai import OPENAI_API_KEY

# Constants
TEST_MESSAGE = "Hello, OpenAI! Please respond with a brief greeting."
EXPECTED_MIN_RESPONSE_LENGTH = 5

def test_openai_chat():
  """Test OpenAI API integration with default model"""
  chat = text_chat(OPENAI_API_KEY, model=DEFAULT_MODEL)
  result = chat(TEST_MESSAGE)
  
  assert isinstance(result, str)
  assert len(result) > EXPECTED_MIN_RESPONSE_LENGTH
  print(f"✅ OpenAI test passed. Response: {result}")

if __name__ == "__main__":
  # Run test directly
  print("Running OpenAI test...")
  
  try:
    test_openai_chat()
    print("🎉 Test passed!")
    
  except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
