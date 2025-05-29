#!/bin/bash
# Run only end-to-end tests (requires API key)
pytest -m e2e "$@"
