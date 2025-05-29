# Development Guide

## Package Management Standard

**This project uses UV for ALL package management operations.**

UV is faster, more reliable, and provides better dependency resolution than pip.

## What is UV?

UV is a modern, fast Python package manager - think of it as a better replacement for pip. It's much faster and handles dependencies better.

## Basic Setup (Required)

```bash
# Install your project dependencies
uv sync
```

## Optional Development Tools

### Currently installed tools

#### isort (Import Organizer) - INSTALLED

- **Purpose**: Sorts your import statements in a standard order
- **When to use**: When you have many imports and want them organized
- **Command**: `uv run isort src/`
- **Example**: Puts standard library imports first, then third-party, then your own modules

### Additional tools you can install if needed

#### ruff (Code Checker + Formatter) - OPTIONAL

- **Purpose**: Finds bugs that unit tests might miss (see ruff_examples.py for examples)
- **Real bugs it catches**: Mutable default arguments, security issues with eval(), resource leaks
- **Install**: `uv add --dev ruff`
- **Command**: `uv run ruff check src/`

#### black (Code Formatter) - OPTIONAL  

- **Purpose**: Makes code look consistent (see black_examples.py for before/after)
- **When useful**: When code becomes hard to read due to inconsistent formatting
- **Install**: `uv add --dev black`
- **Command**: `uv run black src/`

## Do You Need These Tools?

**For your current simple project**: Probably not necessary

**You should consider them when**:

- Your project has multiple files
- You're working with others
- You want to catch bugs early
- You want professional-looking code

The tools are configured to use 2-space indentation to match your preference.

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
