from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class TaskPlan:
    objective: str
    steps: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    deliverables: List[str] = field(default_factory=list)


class CodingAgent:
    """Igris is a Python coding assistant with local fallback logic and optional LLM integration."""

    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model

    def plan(self, prompt: str) -> TaskPlan:
        if self.api_key:
            return self._plan_via_llm(prompt)
        return self._plan_locally(prompt)

    def generate_code(self, prompt: str, language: str = "python", project_type: str = "cli") -> Dict[str, Any]:
        if self.api_key:
            return self._generate_via_llm(prompt, language, project_type)
        return self._generate_locally(prompt, language, project_type)

    def fix_bug(self, prompt: str, language: str = "python") -> Dict[str, Any]:
        if self.api_key:
            return self._fix_via_llm(prompt, language)
        return {
            "status": "ok",
            "language": language,
            "summary": "Bug-fix workflow prepared.",
            "patch": self._fallback_fix(prompt, language),
            "note": "No API key configured. This is a local-ready fix template.",
        }

    def review_code(self, prompt: str) -> Dict[str, Any]:
        return {
            "status": "ok",
            "summary": f"Review prepared for: {prompt}",
            "checks": [
                "Validate input handling",
                "Check for edge cases",
                "Verify error paths",
                "Ensure tests cover the main scenario",
            ],
            "notes": "This review mode is a structured sanity-check framework.",
        }

    def _plan_locally(self, prompt: str) -> TaskPlan:
        normalized = prompt.strip() or "General coding task"
        return TaskPlan(
            objective=normalized,
            steps=[
                "Understand the requirement and identify the user goal.",
                "Inspect the project structure and any affected files.",
                "Implement the smallest correct solution.",
                "Add or update validation or tests where needed.",
                "Summarize the result and any assumptions.",
            ],
            risks=[
                "Missing edge cases or constraints.",
                "Unclear requirements may require follow-up questions.",
                "Insufficient validation can leave regressions unnoticed.",
            ],
            deliverables=[
                "Working implementation",
                "Validation results",
                "Short summary of the change",
            ],
        )

    def _generate_locally(self, prompt: str, language: str, project_type: str) -> Dict[str, Any]:
        project_type = project_type.lower()
        if project_type == "web":
            files = {
                "app.py": self._template_web_app(prompt),
                "requirements.txt": "fastapi==0.111.0\nuvicorn==0.30.3\n",
            }
        elif project_type == "api":
            files = {
                "main.py": self._template_api(prompt),
                "requirements.txt": "fastapi==0.111.0\nuvicorn==0.30.3\n",
            }
        else:
            files = {
                "main.py": self._template_cli(prompt, language),
                "requirements.txt": "",
            }

        return {
            "status": "ok",
            "language": language,
            "project_type": project_type,
            "summary": f"Generated starter code for: {prompt}",
            "files": files,
            "note": "No API key configured. Local fallback mode is active.",
        }

    def _generate_via_llm(self, prompt: str, language: str, project_type: str) -> Dict[str, Any]:
        return self._generate_locally(prompt, language, project_type)

    def _plan_via_llm(self, prompt: str) -> TaskPlan:
        return self._plan_locally(prompt)

    def _fix_via_llm(self, prompt: str, language: str) -> Dict[str, Any]:
        return self.fix_bug(prompt, language)

    def _template_cli(self, prompt: str, language: str) -> str:
        if language.lower() == "python":
            return (
                'def main():\n'
                f'    """Starter implementation for: {prompt}"""\n'
                f'    print("This CLI was generated for: {prompt}")\n\n\n'
                'if __name__ == "__main__":\n'
                '    main()\n'
            )

        if language.lower() == "javascript":
            return (
                'function main() {\n'
                f'  console.log("This CLI was generated for: {prompt}");\n'
                '}\n\n'
                'main();\n'
            )

        return f"// No template available for language: {language}"

    def _template_web_app(self, prompt: str) -> str:
        return (
            'from fastapi import FastAPI\n\n'
            'app = FastAPI()\n\n'
            "@app.get('/')\n"
            'def root():\n'
            '    return {"message": "Hello from Igris", "task": "' + prompt.replace('"', '\\"') + '"}\n\n'
            "@app.get('/health')\n"
            'def health():\n'
            '    return {"status": "ok"}\n'
        )

    def _template_api(self, prompt: str) -> str:
        return (
            'from fastapi import FastAPI\n\n'
            'app = FastAPI(title="Igris API")\n\n'
            "@app.get('/')\n"
            'def root():\n'
            '    return {"message": "AI-generated API from Igris", "task": "' + prompt.replace('"', '\\"') + '"}\n\n'
            "@app.get('/health')\n"
            'def health():\n'
            '    return {"status": "ok"}\n'
        )

    def _fallback_fix(self, prompt: str, language: str) -> str:
        if language.lower() == "python":
            return '''
# Fix strategy:
# 1. Validate inputs before using them.
# 2. Guard optional values and empty collections.
# 3. Add a focused regression test.
# 4. Keep the fix minimal and explicit.

try:
    value = data["key"]
except KeyError:
    value = None

if value is None:
    return "safe fallback"

return value
'''

        return "// Add defensive validation and a regression test for the failing case."

    def as_dict(self, plan: TaskPlan) -> Dict[str, Any]:
        return {
            "objective": plan.objective,
            "steps": plan.steps,
            "risks": plan.risks,
            "deliverables": plan.deliverables,
        }


if __name__ == "__main__":
    agent = CodingAgent()
    plan = agent.plan("Create a task manager app")
    print(json.dumps(agent.as_dict(plan), indent=2))
