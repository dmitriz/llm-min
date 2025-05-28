#!/bin/bash
# Development scripts for this project
# Usage: ./dev.sh <command>

case "$1" in
    "install")
        echo "Installing dependencies with UV..."
        uv sync --extra test
        ;;
    "test")
        echo "Running tests with UV..."
        uv run pytest
        ;;
    "test-verbose")
        echo "Running tests with verbose output..."
        uv run pytest -v
        ;;
    "add")
        if [ -z "$2" ]; then
            echo "Usage: ./dev.sh add <package-name>"
            exit 1
        fi
        echo "Adding package: $2"
        uv add "$2"
        ;;
    "add-test")
        if [ -z "$2" ]; then
            echo "Usage: ./dev.sh add-test <package-name>"
            exit 1
        fi
        echo "Adding test dependency: $2"
        uv add --group test "$2"
        ;;
    *)
        echo "Available commands:"
        echo "  install     - Install all dependencies"
        echo "  test        - Run tests"
        echo "  test-verbose - Run tests with verbose output"
        echo "  add <pkg>   - Add a dependency"
        echo "  add-test <pkg> - Add a test dependency"
        ;;
esac
