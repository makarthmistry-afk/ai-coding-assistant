# AI Coding Assistant

A combined coding AI project that brings together:
- planning a coding task
- generating code and starter projects
- fixing bugs with guarded patch suggestions
- reviewing code quality
- running a small web API for interactive use
- supporting a CLI workflow for terminal use

This repo is designed as a practical "all-in-one" coding assistant starter.
It is intentionally simple, readable, and extensible so you can attach a real LLM provider later.

## Features

- CLI workflow for planning, generating, and fixing tasks
- Web API for interactive project generation and analysis
- Starter project templates for CLI apps, REST APIs, and web apps
- Local fallback logic when no AI provider key is configured
- Easy extension points for GitHub repo reading, LLM APIs, tests, and dashboards

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

3. Run the CLI planner
   ```bash
   python -m ai_coding_assistant.cli plan "Build a login page in Flask"
   ```

4. Generate a starter project
   ```bash
   python -m ai_coding_assistant.cli generate "Create a Python script that reads CSV files" --language python --project-type cli
   ```

5. Fix a bug description
   ```bash
   python -m ai_coding_assistant.cli fix "The app crashes when a required field is missing" --language python
   ```

6. Launch the web API
   ```bash
   python -m ai_coding_assistant.cli serve
   ```

Then open:
- http://localhost:8000/health
- http://localhost:8000/docs

## Example commands

```bash
python -m ai_coding_assistant.cli plan "Create a REST API for task management"
python -m ai_coding_assistant.cli generate "Create a small web dashboard for sales metrics" --project-type web
python -m ai_coding_assistant.cli generate "Create a FastAPI service for users" --project-type api
python -m ai_coding_assistant.cli fix "Fix missing value handling in the CSV parser" --language python
python -m ai_coding_assistant.cli review "Check the script for reliability and edge cases"
```

## Project structure

```text
ai_coding_assistant/
    __init__.py
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
- To connect to a real LLM, set `OPENAI_API_KEY` and update the API call logic in `agent.py`.
- The web service exposes a simple interactive layer while the CLI gives you quick terminal workflows.

## Roadmap

- repo-aware file reading and patching
- GitHub integration
- multi-file editing
- smarter context memory
- support for more templates and frameworks
- automatic test generation

## License

MIT
