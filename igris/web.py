from __future__ import annotations

from typing import Any, Dict

from fastapi import FastAPI

app = FastAPI(title="Igris")


@app.get("/")
def root() -> Dict[str, Any]:
    return {"message": "Igris is running", "status": "ok"}


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok"}


@app.get("/status")
def status() -> Dict[str, Any]:
    return {"assistant": "Igris", "mode": "local-fallback"}
