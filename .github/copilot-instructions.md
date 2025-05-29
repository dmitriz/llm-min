# GitHub Copilot Instructions

## Core Principles
- **NEVER add packages to pyproject.toml or requirements without explicit user approval**
- **NEVER create example files unless specifically requested**
- **Always wait for approval before installing or configuring tools**
- **Keep the project minimal - remove noise, not add it**
- **Use `uv` instead of `pip` for all Python package management**
- **Edit existing files instead of replacing them when user says "update" or "edit"**

## Indentation Style
- This project uses 2-space indentation for Python (not PEP 8's 4 spaces)
- Respect existing formatting unless there's a clear problem
- Don't create formatting scripts if code is already properly formatted

## Workflow Rules
1. Listen carefully to what the user is asking for
2. Show concrete, realistic examples when justifying tools
3. Ask for permission before adding dependencies
4. Focus on actual value, not theoretical benefits
5. Remove unnecessary files and complexity when identified
6. Pay attention to user feedback and adjust behavior accordingly

## Code Quality
- Only suggest tools that catch bugs unit tests would miss
- Show realistic examples, not contrived ones
- Explain the actual value proposition clearly
- Don't add complexity without clear benefits
