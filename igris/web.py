from __future__ import annotations

import argparse
import json

from igris.agent import CodingAgent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Igris - Python AI Coding Assistant")
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan_parser = subparsers.add_parser("plan", help="Break a task into implementation steps")
    plan_parser.add_argument("prompt")

    generate_parser = subparsers.add_parser("generate", help="Generate a starter project or code snippet")
    generate_parser.add_argument("prompt")
    generate_parser.add_argument("--language", default="python")
    generate_parser.add_argument("--project-type", default="cli", choices=["cli", "web", "api"])

    fix_parser = subparsers.add_parser("fix", help="Generate a bug-fix plan and patch")
    fix_parser.add_argument("prompt")
    fix_parser.add_argument("--language", default="python")

    review_parser = subparsers.add_parser("review", help="Run a structured code review checklist")
    review_parser.add_argument("prompt")

    inspect_parser = subparsers.add_parser("inspect", help="Inspect a repository and summarize files")
    inspect_parser.add_argument("path", nargs="?", default=".")

    patch_parser = subparsers.add_parser("patch", help="Write a new version of a file in the repo")
    patch_parser.add_argument("file_path")
    patch_parser.add_argument("--repo-root", default=".")
    patch_parser.add_argument("--content", default="")

    test_parser = subparsers.add_parser("test", help="Generate a starter pytest file for a Python module")
    test_parser.add_argument("file_path")
    test_parser.add_argument("--repo-root", default=".")

    memory_parser = subparsers.add_parser("memory", help="Store or view memory for the coding assistant")
    memory_parser.add_argument("key", nargs="?", default="")
    memory_parser.add_argument("--value", default="")
    memory_parser.add_argument("--repo-root", default=".")

    serve_parser = subparsers.add_parser("serve", help="Start the built-in web API")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    agent = CodingAgent()

    if args.command == "plan":
        plan = agent.plan(args.prompt)
        print(json.dumps({
            "objective": plan.objective,
            "steps": plan.steps,
            "risks": plan.risks,
            "deliverables": plan.deliverables,
        }, indent=2))
        return

    if args.command == "generate":
        result = agent.generate_code(args.prompt, args.language, args.project_type)
        print(json.dumps(result, indent=2))
        return

    if args.command == "fix":
        result = agent.fix_bug(args.prompt, args.language)
        print(json.dumps(result, indent=2))
        return

    if args.command == "review":
        result = agent.review_code(args.prompt)
        print(json.dumps(result, indent=2))
        return

    if args.command == "inspect":
        result = agent.inspect_repo(args.path)
        print(json.dumps(result, indent=2))
        return

    if args.command == "patch":
        result = agent.patch_repo(args.repo_root, args.file_path, args.content)
        print(json.dumps(result, indent=2))
        return

    if args.command == "test":
        result = agent.generate_tests(args.repo_root, args.file_path)
        print(json.dumps(result, indent=2))
        return

    if args.command == "memory":
        if args.key:
            if args.value:
                result = agent.remember(args.key, args.value, args.repo_root)
            else:
                result = agent.recall(args.repo_root)
        else:
            result = agent.recall(args.repo_root)
        print(json.dumps(result, indent=2))
        return

    if args.command == "serve":
        from igris.web import app
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
        return


if __name__ == "__main__":
    main()
