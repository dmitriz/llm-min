# Text Chat - Minimal LLM Interface

A minimal, clean Python package for interfacing with different LLM providers (OpenAI and Grok).

## Installation

### Using uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Install in development mode
uv pip install -e .
```

### Using pip

```bash
pip install -e .
```

### From requirements

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from text_chat import text_chat
import os

# Using OpenAI
api_key = os.getenv("OPENAI_API_KEY")
chat = text_chat(api_key, "gpt-3.5-turbo", provider="openai")
response = chat("Hello, OpenAI!")
print(response)

# Using Grok
api_key = os.getenv("GROK_API_KEY")
chat = text_chat(api_key, "grok-1", provider="grok")
response = chat("Hello, Grok!")
print(response)
```

### API Reference

#### `text_chat(api_key, model, provider="openai")`

Creates a chat function for the specified provider.

**Parameters:**

- `api_key` (str): API key for the provider
- `model` (str): Model name to use
- `provider` (str): Provider name ("openai" or "grok")

**Returns:**

- `function`: A `send_message(message)` function that takes a message string and returns the LLM response

**Supported Providers:**

- `"openai"`: OpenAI GPT models (gpt-3.5-turbo, gpt-4, etc.)
- `"grok"`: Grok models via X.AI API

## Environment Variables

Set your API keys as environment variables:

```bash
export OPENAI_API_KEY="sk-..."
export GROK_API_KEY="sk-..."
```

Or create a `.secrets` directory with your keys:

```python
# .secrets/openai.py
api_key = "sk-..."
```

```python
# .secrets/grok.py
api_key = "sk-..."
```

## Testing

Run tests with pytest:

```bash
# Using uv
uv run pytest tests/

# Using pip
pip install pytest
pytest tests/
```

Or run the test file directly:

```bash
python tests/test_text_chat.py
```

**Note:** Tests require actual API keys to test real API calls. Set the environment variables `OPENAI_API_KEY` and/or `GROK_API_KEY` to run the integration tests.

## Development

### Using uv

```bash
# Install all dependencies including dev dependencies
uv sync

# Run tests
uv run pytest

# Run formatting
uv run black src/ tests/

# Run linting
uv run ruff check src/ tests/
```

### Using pip

```bash
pip install -e ".[dev]"
```

This includes:

- pytest for testing
- black for code formatting
- ruff for linting

## Project Structure

```text
text-chat/
├── src/
│   └── text_chat/
│       ├── __init__.py
│       └── text_chat.py
├── tests/
│   └── test_text_chat.py
├── .secrets/
├── .python-version
├── pyproject.toml
├── requirements.txt
└── README.md
```

## License

MIT License
