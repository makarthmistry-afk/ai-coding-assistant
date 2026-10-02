# Igris

Igris is a Python-based AI coding assistant designed to help with:
- planning coding tasks
- generating starter code
- fixing bug reports
- reviewing code for reliability
- exposing a simple web API for interactive use

It is built as a practical starter project for a coding agent that can work in local fallback mode without an API key and can be upgraded to a real model later.

## Features

- Python CLI tool for planning, generation, review, and bug-fix workflows
- FastAPI web API for interactive use
- Starter templates for CLI apps, APIs, and web apps
- Fallback logic when no external AI provider is configured
- Extendable architecture for future LLM integration, repo scanning, and project patching

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

3. Plan a task
   ```bash
   python -m igris.cli plan "Build a login page in Flask"
   ```

4. Generate a starter app
   ```bash
   python -m igris.cli generate "Create a Python CLI that reads a CSV file" --language python --project-type cli
   ```

5. Fix a bug report
   ```bash
   python -m igris.cli fix "The app crashes when a required field is missing" --language python
   ```

6. Launch the web API
   ```bash
   python -m igris.cli serve
   ```

Then visit:
- http://localhost:8000/health
- http://localhost:8000/docs

## Project structure

```text
igris/
    __init__.py
    __main__.py
    agent.py
    cli.py
    templates.py
    web.py
main.py
requirements.txt
README.md
```

## Notes

- This works in local demo mode without an API key.
- To connect to a real model, set `OPENAI_API_KEY` and plug it into the LLM hooks inside `igris/agent.py`.
- Igris is designed to be a strong foundation for a more advanced autonomous coding agent.

## License

MIT
