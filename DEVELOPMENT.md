# Development Guide

## Package Management Standard

**This project uses UV for ALL package management operations.**

UV is faster, more reliable, and provides better dependency resolution than pip.

### Installation Commands

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

# Run scripts with UV
uv run script-name

# Run python with UV
uv run python script.py
```

### Testing

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

### Available UV Commands

When you run `uv run <command>`, these are the main commands available:

- **`pytest`** - Run your tests (recommended)
- **`python`** - Run Python interpreter with your project dependencies
- **`pydoc`** - Python documentation tool

### Running Your Code

```bash
# Interactive Python with your project loaded
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
