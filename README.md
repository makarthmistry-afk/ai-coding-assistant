from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


class RepoTools:
    """Small repository utilities for scanning, patching, and generated test stubs."""

    def __init__(self, repo_root: str = "."):
        self.root = Path(repo_root).resolve()

    def scan_repo(self) -> Dict[str, Any]:
        files = []
        for path in sorted(self.root.rglob("*")):
            if path.is_file():
                rel = path.relative_to(self.root).as_posix()
                files.append(rel)
        return {
            "status": "ok",
            "repo_root": str(self.root),
            "total_files": len(files),
            "files": files[:200],
            "summary": {
                "python": sum(1 for f in files if f.endswith(".py")),
                "markdown": sum(1 for f in files if f.endswith(".md")),
                "config": sum(1 for f in files if f.endswith((".json", ".toml", ".yaml", ".yml"))),
            },
        }

    def read_file(self, file_path: str) -> str:
        target = (self.root / file_path).resolve()
        return target.read_text(encoding="utf-8")

    def write_file(self, file_path: str, content: str) -> Dict[str, Any]:
        target = (self.root / file_path).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return {
            "status": "ok",
            "path": file_path,
            "updated": True,
        }

    def generate_test_stub(self, file_path: str) -> str:
        if not file_path.endswith(".py"):
            return "# No Python test stub generated for a non-Python file."

        module_name = file_path.replace("/", ".").replace("\\", ".")[:-3]
        if module_name.startswith("."):
            module_name = module_name[1:]
        return (
            "import pytest\n\n"
            f"from {module_name} import *\n\n\n"
            "def test_smoke():\n"
            "    assert True\n"
        )

    def save_memory(self, key: str, value: Any) -> Dict[str, Any]:
        memory_dir = self.root / ".igris"
        memory_dir.mkdir(parents=True, exist_ok=True)
        memory_file = memory_dir / "memory.json"
        data = json.loads(memory_file.read_text(encoding="utf-8")) if memory_file.exists() else {}
        data[key] = value
        memory_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return {"status": "ok", "key": key, "value": value, "path": str(memory_file)}

    def load_memory(self) -> Dict[str, Any]:
        memory_file = self.root / ".igris" / "memory.json"
        if not memory_file.exists():
            return {"status": "ok", "memory": {}}
        return {"status": "ok", "memory": json.loads(memory_file.read_text(encoding="utf-8"))}
