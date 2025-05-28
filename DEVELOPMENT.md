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
uv run pytest tests/test_text_chat.py

# Run tests with coverage
uv run pytest --cov=src
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
