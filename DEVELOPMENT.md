# Development Guide

## Package Management

This project uses **UV** for package management. UV is faster and more reliable than pip.

## Setup

## Package Management Commands

```bash
# Install dependencies
uv sync

# Install test dependencies
uv sync --extra test

# Add a new dependency
uv add package-name

# Add a development dependency  
uv add --dev package-name

# Add a test dependency
uv add --group test package-name
```

## Available Commands

All tools are organized in a single `tools` group in `pyproject.toml`:

**Built-in commands:**

- **`python`** - Python interpreter with project dependencies
- **`pythonw`** - Python (Windows GUI version)
- **`pydoc`** - Python documentation tool

**Installed tools (from tools group):**

- **`pytest`** - Run tests
- **`isort`** - Sort import statements
- **`isort-identify-imports`** - Import identification tool
- **`httpx`** - HTTP client (from main dependencies)

Note: `py.test` may appear in the command list but is broken - use `pytest` instead.

## Testing

```bash
# Run all tests
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Run specific test file
uv run pytest src/test_text_chat.py

# Run tests with coverage (requires: uv add --group test pytest-cov)
uv run pytest --cov=src

# Run tests in watch mode (requires: uv add --group test pytest-watch)
uv run ptw

# Run Python directly (for testing code interactively)
uv run python

# Run specific Python scripts
uv run python src/text_chat.py
```

## Running Code

```bash
# Interactive Python
uv run python

# Run a specific script
uv run python -c "from src.text_chat import text_chat; print('Library loaded!')"
```

### Why UV?

- **Faster**: 10-100x faster than pip
- **Better resolution**: Resolves dependencies more reliably
- **Lock files**: Ensures reproducible builds
- **Project isolation**: Automatically manages virtual environments

### Never use pip directly

Instead of:

```bash
pip install package-name
python -m pytest
```

Always use:

```bash
uv add package-name
uv run pytest
```
