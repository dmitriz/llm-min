"""Pytest configuration for automatic test markers."""
import pytest


def pytest_collection_modifyitems(config, items):
  """Automatically apply markers based on file names."""
  for item in items:
    # Get the file path of the test
    test_file = item.fspath.basename
    
    # Apply markers based on file naming convention
    if "_unit" in test_file:
      item.add_marker(pytest.mark.unit)
    elif "_e2e" in test_file:
      item.add_marker(pytest.mark.e2e)
    elif test_file in ["test_text_chat.py"]:
      # Specific files that are e2e tests
      item.add_marker(pytest.mark.e2e)
    else:
      # Default fallback - check for API key usage to determine if it's e2e
      if hasattr(item, 'function'):
        # Look for API key usage in the test source
        source = item.function.__code__.co_names
        if 'OPENAI_API_KEY' in source:
          item.add_marker(pytest.mark.e2e)
        else:
          item.add_marker(pytest.mark.unit)
