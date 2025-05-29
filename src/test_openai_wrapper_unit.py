"""Unit tests for openai_wrapper module using mocked API calls."""
import json
from unittest.mock import MagicMock, patch

import pytest
from httpx import Response

from openai_wrapper import openai_wrapper


def create_mock_response(content: str = "Hello! How can I help you?", status_code: int = 200):
  """Create a mock httpx Response object."""
  mock_response = MagicMock(spec=Response)
  mock_response.status_code = status_code
  mock_response.headers = {"content-type": "application/json"}
  
  # Mock successful OpenAI API response format
  response_data = {
    "id": "chatcmpl-test123",
    "object": "chat.completion",
    "created": 1699123456,
    "model": "gpt-4o-mini",
    "choices": [
      {
        "index": 0,
        "message": {
          "role": "assistant",
          "content": content
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
  
  mock_response.json.return_value = response_data
  mock_response.text = json.dumps(response_data)
  return mock_response


class TestOpenAIWrapperUnit:
  """Unit tests for OpenAI wrapper with mocked API calls."""
  
  @patch('openai_wrapper.httpx.request')
  def test_basic_request_structure(self, mock_request):
    """Test that the wrapper creates correct HTTP request structure."""
    # Setup mock response
    mock_request.return_value = create_mock_response()
    
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
    mock_request.assert_called_once()
    call_kwargs = mock_request.call_args[1]  # Get keyword arguments
    
    # Check method and URL
    assert call_kwargs['method'] == "POST"
    assert call_kwargs['url'] == "https://api.openai.com/v1/chat/completions"
    
    # Check headers
    headers = call_kwargs['headers']
    assert headers['Authorization'] == "Bearer sk-test123"
    assert headers['Content-Type'] == "application/json"
    
    # Check request payload
    json_data = call_kwargs['json']
    assert json_data['model'] == "gpt-4o-mini"
    assert json_data['messages'] == [{"role": "user", "content": "Hello, OpenAI!"}]
    
    # Check response structure
    assert isinstance(response, dict)
    assert "choices" in response
    assert "usage" in response
    assert response["choices"][0]["message"]["content"] == "Hello! How can I help you?"

  @patch('openai_wrapper.httpx.request')
  def test_additional_parameters(self, mock_request):
    """Test that additional parameters are passed correctly."""
    mock_request.return_value = create_mock_response()
    
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
    call_kwargs = mock_request.call_args[1]
    json_data = call_kwargs['json']
    
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

  def test_missing_required_fields_validation(self):
    """Test validation of required fields without making API calls."""
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

  @patch('openai_wrapper.httpx.request')
  def test_http_error_handling(self, mock_request):
    """Test handling of HTTP errors."""
    # Mock HTTP error response
    mock_response = MagicMock(spec=Response)
    mock_response.status_code = 401
    mock_response.text = '{"error": {"message": "Invalid API key"}}'
    mock_response.raise_for_status.side_effect = Exception("Client error '401 Unauthorized'")
    mock_request.return_value = mock_response
    
    input_object = {
      "api_key": "invalid-key",
      "model": "gpt-4o-mini",
      "messages": [{"role": "user", "content": "Test"}]
    }
    
    with pytest.raises(Exception, match="401 Unauthorized"):
      openai_wrapper(input_object)

  @patch('openai_wrapper.httpx.request')
  def test_custom_headers_and_timeout(self, mock_request):
    """Test that custom headers and timeout are applied."""
    mock_request.return_value = create_mock_response()
    
    input_object = {
      "api_key": "sk-test123",
      "model": "gpt-4o-mini",
      "messages": [{"role": "user", "content": "Test"}],
      "headers": {"Custom-Header": "test-value"},
      "timeout": 30
    }
    
    openai_wrapper(input_object)
    
    call_kwargs = mock_request.call_args[1]
    
    # Check timeout
    assert call_kwargs['timeout'] == 30
    
    # Check custom headers are included
    headers = call_kwargs['headers']
    assert headers['Custom-Header'] == "test-value"
    assert headers['Authorization'] == "Bearer sk-test123"  # Still includes auth

  @patch('openai_wrapper.httpx.request') 
  def test_response_parsing(self, mock_request):
    """Test that responses are parsed correctly."""
    test_content = "This is a test response from the API."
    mock_request.return_value = create_mock_response(content=test_content)
    
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
