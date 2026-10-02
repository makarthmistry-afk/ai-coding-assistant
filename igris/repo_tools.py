from __future__ import annotations

import json
from typing import Any, Dict

from fastapi import FastAPI

from igris.agent import CodingAgent

app = FastAPI(title="Igris")
agent = CodingAgent()


@app.get("/")
def root() -> Dict[str, Any]:
    return {"message": "Igris is running", "status": "ok"}


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok"}


@app.get("/status")
def status() -> Dict[str, Any]:
    return {"assistant": "Igris", "mode": "local-fallback"}


@app.get("/inspect")
def inspect_repo(path: str = ".") -> Dict[str, Any]:
    return agent.inspect_repo(path)


@app.post("/plan")
def plan_task(payload: Dict[str, str]) -> Dict[str, Any]:
    prompt = payload.get("prompt", "General coding task")
    plan = agent.plan(prompt)
    return agent.as_dict(plan)


@app.post("/generate")
def generate_code(payload: Dict[str, str]) -> Dict[str, Any]:
    prompt = payload.get("prompt", "Create a starter app")
    language = payload.get("language", "python")
    project_type = payload.get("project_type", "cli")
    return agent.generate_code(prompt, language, project_type)


@app.post("/patch")
def patch_file(payload: Dict[str, str]) -> Dict[str, Any]:
    repo_root = payload.get("repo_root", ".")
    file_path = payload.get("file_path", "")
    content = payload.get("content", "")
    if not file_path:
        return {"status": "error", "message": "file_path is required"}
    return agent.patch_repo(repo_root, file_path, content)


@app.get("/memory")
def memory() -> Dict[str, Any]:
    return agent.recall()
