"""Unit tests for openai_wrapper module using mocked API calls."""
import json

import pytest

from openai_wrapper import openai_wrapper


def create_mock_response(content: str = "Hello! How can I help you?", status_code: int = 200):
  """Create a mock response object that mimics httpx.Response behavior."""
  class MockResponse:
    def __init__(self, content, status_code):
      self.status_code = status_code
      self.headers = {"content-type": "application/json"}
      self._content = content
      
    def json(self):
      # Mock successful OpenAI API response format
      return {
        "id": "chatcmpl-test123",
        "object": "chat.completion", 
        "created": 1699123456,
        "model": "gpt-4o-mini",
        "choices": [
          {
            "index": 0,
            "message": {
              "role": "assistant",
              "content": self._content
            },
            "finish_reason": "stop"
          }
        ],
        "usage": {
          "prompt_tokens": 10,
          "completion_tokens": 15,
          "total_tokens": 25
        }
      }
      
    def raise_for_status(self):
      if self.status_code >= 400:
        raise Exception(f"Client error '{self.status_code} Unauthorized'")
        
    @property
    def text(self):
      return json.dumps(self.json())
  
  return MockResponse(content, status_code)


class TestOpenAIWrapperUnit:
  """Unit tests for OpenAI wrapper with mocked API calls."""
  
  def test_basic_request_structure(self, monkeypatch):
    """Test that the wrapper creates correct HTTP request structure."""
    # Capture the request arguments
    captured_request = {}
    
    def mock_request(**kwargs):
      captured_request.update(kwargs)
      return create_mock_response()
    
    # Use monkeypatch to replace httpx.request
    monkeypatch.setattr("openai_wrapper.httpx.request", mock_request)
    
    # Test input
    input_object = {
      "api_key": "sk-test123",
      "model": "gpt-4o-mini",
      "messages": [
        {"role": "user", "content": "Hello, OpenAI!"}
      ]
    }
    
    # Call wrapper
    response = openai_wrapper(input_object)
    
    # Verify HTTP request was made correctly
    assert captured_request['method'] == "POST"
    assert captured_request['url'] == "https://api.openai.com/v1/chat/completions"
    
    # Check headers
    headers = captured_request['headers']
    assert headers['Authorization'] == "Bearer sk-test123"
    assert headers['Content-Type'] == "application/json"
    
    # Check request payload
    json_data = captured_request['json']
    assert json_data['model'] == "gpt-4o-mini"
    assert json_data['messages'] == [{"role": "user", "content": "Hello, OpenAI!"}]
    
    # Check response structure
    assert isinstance(response, dict)
    assert "choices" in response
    assert "usage" in response
    assert response["choices"][0]["message"]["content"] == "Hello! How can I help you?"

  def test_additional_parameters(self, monkeypatch):
    """Test that additional parameters are passed correctly."""
    captured_request = {}
    
    def mock_request(**kwargs):
      captured_request.update(kwargs)
      return create_mock_response()
    
    monkeypatch.setattr("openai_wrapper.httpx.request", mock_request)
    
    input_object = {
      "api_key": "sk-test123",
      "model": "gpt-4o-mini", 
      "messages": [{"role": "user", "content": "Test"}],
      "temperature": 0.7,
      "max_tokens": 100,
      "top_p": 0.9
    }
    
    openai_wrapper(input_object)
    
    # Check that additional parameters were included in request
    json_data = captured_request['json']
    assert json_data['temperature'] == 0.7
    assert json_data['max_tokens'] == 100
    assert json_data['top_p'] == 0.9

  def test_missing_required_fields(self):
    """Test validation of required fields."""
    # Test missing api_key
    with pytest.raises(ValueError, match="Missing required field: api_key"):
      openai_wrapper({"model": "gpt-4o-mini", "messages": []})
    
    # Test missing model
    with pytest.raises(ValueError, match="Missing required field: model"):
      openai_wrapper({"api_key": "test", "messages": []})
    
    # Test missing messages
    with pytest.raises(ValueError, match="Missing required field: messages"):
      openai_wrapper({"api_key": "test", "model": "gpt-4o-mini"})
  def test_invalid_message_format(self):
    """Test validation of message structure."""
    with pytest.raises(ValueError):
      openai_wrapper({
        "api_key": "sk-test123",
        "model": "gpt-4o-mini",
        "messages": [{"invalid": "message format"}]  # Missing role and content
      })

  def test_http_error_handling(self, monkeypatch):
    """Test handling of HTTP errors."""
    def mock_request(**kwargs):
      return create_mock_response("Error", status_code=401)
    
    monkeypatch.setattr("openai_wrapper.httpx.request", mock_request)
    
    input_object = {
      "api_key": "invalid-key",
      "model": "gpt-4o-mini",
      "messages": [{"role": "user", "content": "Test"}]
    }
    
    with pytest.raises(Exception, match="401 Unauthorized"):
      openai_wrapper(input_object)

  def test_custom_headers_and_timeout(self, monkeypatch):
    """Test that custom headers and timeout are applied."""
    captured_request = {}
    
    def mock_request(**kwargs):
      captured_request.update(kwargs)
      return create_mock_response()
    
    monkeypatch.setattr("openai_wrapper.httpx.request", mock_request)
    
    input_object = {
      "api_key": "sk-test123",
      "model": "gpt-4o-mini",
      "messages": [{"role": "user", "content": "Test"}],
      "headers": {"Custom-Header": "test-value"},
      "timeout": 30
    }
    
    openai_wrapper(input_object)
    
    # Check timeout
    assert captured_request['timeout'] == 30
    
    # Check custom headers are included
    headers = captured_request['headers']
    assert headers['Custom-Header'] == "test-value"
    assert headers['Authorization'] == "Bearer sk-test123"  # Still includes auth

  def test_response_parsing(self, monkeypatch):
    """Test that responses are parsed correctly."""
    test_content = "This is a test response from the API."
    
    def mock_request(**kwargs):
      return create_mock_response(content=test_content)
    
    monkeypatch.setattr("openai_wrapper.httpx.request", mock_request)
    
    input_object = {
      "api_key": "sk-test123",
      "model": "gpt-4o-mini",
      "messages": [{"role": "user", "content": "Test"}]
    }
    
    response = openai_wrapper(input_object)
    
    # Verify response structure
    assert response["choices"][0]["message"]["content"] == test_content
    assert response["usage"]["total_tokens"] == 25
    assert response["model"] == "gpt-4o-mini"
