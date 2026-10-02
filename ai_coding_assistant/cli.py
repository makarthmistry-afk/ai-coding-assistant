from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class TaskPlan:
    objective: str
    steps: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)


class CodingAgent:
    """A simple coding agent with local fallback logic and optional LLM integration."""

    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model

    def plan(self, prompt: str) -> TaskPlan:
        if self.api_key:
            return self._plan_via_llm(prompt)
        return self._plan_locally(prompt)

    def generate_code(self, prompt: str, language: str = "python") -> Dict[str, Any]:
        if self.api_key:
            return self._generate_via_llm(prompt, language)
        return self._generate_locally(prompt, language)

    def fix_bug(self, prompt: str, language: str = "python") -> Dict[str, Any]:
        if self.api_key:
            return self._fix_via_llm(prompt, language)
        return {
            "status": "ok",
            "language": language,
            "summary": "Bug fix workflow prepared.",
            "patch": self._fallback_fix(prompt, language),
            "note": "No API key configured. This is a local-ready fix template."
        }

    def _plan_locally(self, prompt: str) -> TaskPlan:
        normalized = prompt.strip()
        return TaskPlan(
            objective=normalized,
            steps=[
                "Understand the task and identify the main user requirement.",
                "Inspect the project structure and relevant files.",
                "Implement the smallest correct solution.",
                "Validate behavior with tests or a sanity check.",
                "Summarize the change and any assumptions."
            ],
            risks=[
                "Missing user constraints or edge cases.",
                "Ambiguous requirements require follow-up clarification.",
                "No validation step may leave hidden regressions."
            ]
        )

    def _generate_locally(self, prompt: str, language: str) -> Dict[str, Any]:
        return {
            "status": "ok",
            "language": language,
            "summary": f"Drafted a starter implementation for: {prompt}",
            "code": self._fallback_code(prompt, language),
            "note": "No API key configured. Local fallback mode is active."
        }

    def _plan_via_llm(self, prompt: str) -> TaskPlan:
        # Replace this block with your preferred API call when connected to a real model.
        return self._plan_locally(prompt)

    def _generate_via_llm(self, prompt: str, language: str) -> Dict[str, Any]:
        # Replace this block with your preferred API call when connected to a real model.
        return self._generate_locally(prompt, language)

    def _fix_via_llm(self, prompt: str, language: str) -> Dict[str, Any]:
        return self.fix_bug(prompt, language)

    def _fallback_code(self, prompt: str, language: str) -> str:
        if language.lower() == "python":
            return '''def main():
    """Starter implementation for: {prompt}"""
    print("This is a generated starter for: {prompt}")


if __name__ == "__main__":
    main()
'''.format(prompt=prompt)

        if language.lower() == "javascript":
            return '''function main() {
  console.log("This is a generated starter for: {prompt}");
}

main();
'''.format(prompt=prompt)

        return f"// No implementation template available for language: {language}"

    def _fallback_fix(self, prompt: str, language: str) -> str:
        if language.lower() == "python":
            return '''
# Recommended fix checklist:
# 1. Validate input before using it.
# 2. Guard optional values and empty collections.
# 3. Add a focused test for the failing case.
# 4. Log or report the root cause clearly.

try:
    value = data["key"]
except KeyError:
    value = None

if value is None:
    return "safe fallback"

return value
'''

        return "// Add defensive validation and targeted tests for the reported bug."

    def as_dict(self, plan: TaskPlan) -> Dict[str, Any]:
        return {
            "objective": plan.objective,
            "steps": plan.steps,
            "risks": plan.risks,
        }


if __name__ == "__main__":
    agent = CodingAgent()
    plan = agent.plan("Create a web app to manage tasks")
    print(json.dumps(agent.as_dict(plan), indent=2))
