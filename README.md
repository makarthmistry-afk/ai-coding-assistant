# AI Coding Assistant

A practical coding-focused AI project that can:
- understand a coding task
- plan the work
- generate project files or code snippets
- propose fixes for bugs
- scaffold starter apps
- review code quality

This repository is a strong starting point for an agent-style coding assistant. It is intentionally simple, readable, and extendable so you can connect it to real LLM providers later.

## Features

- CLI-based workflow for coding tasks
- Task planning and breakdown
- Code generation templates for common app patterns
- Optional OpenAI integration
- Local fallback mode when no API key is configured
- Easy extension points for adding GitHub repo inspection, IDE integration, or a web UI

## Quick start

1. Create a virtual environment
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Run the assistant
   ```bash
   python -m ai_coding_assistant.cli plan "Build a login page in Flask"
   ```

   Or generate a starter app:
   ```bash
   python -m ai_coding_assistant.cli generate "Create a Python CLI that reads a CSV and prints summary stats" --language python
   ```

   Or review a bug:
   ```bash
   python -m ai_coding_assistant.cli fix "Fix the bug where the app crashes when a CSV row is missing a value" --language python
   ```

## Example commands

```bash
python -m ai_coding_assistant.cli plan "Create a REST API for todo items"
python -m ai_coding_assistant.cli generate "Create a Python script that fetches weather data from an API" --language python
python -m ai_coding_assistant.cli fix "The app throws a KeyError on empty API response" --language python
```

## Project structure

```text
ai_coding_assistant/
    __init__.py
    agent.py
    cli.py
    templates.py
main.py
requirements.txt
README.md
```

## Notes

- The project works in demo mode without an API key.
- To enable real LLM-backed generation, set `OPENAI_API_KEY` and update `agent.py` to call your preferred provider.
- This repo is designed as a foundation for a more advanced coding agent, not as a magical "codes everything" system by itself.

## Roadmap

- add repo-aware file reading and patching
- add GitHub integration
- add test-generation workflow
- add a web dashboard
- add multi-file code editing
- add agent memory and project context

## License

MIT
