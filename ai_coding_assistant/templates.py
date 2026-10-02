from __future__ import annotations

import argparse
import json

from ai_coding_assistant.agent import CodingAgent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI coding assistant CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan_parser = subparsers.add_parser("plan", help="Break a task into implementation steps")
    plan_parser.add_argument("prompt")

    generate_parser = subparsers.add_parser("generate", help="Generate a starter code snippet")
    generate_parser.add_argument("prompt")
    generate_parser.add_argument("--language", default="python")

    fix_parser = subparsers.add_parser("fix", help="Generate a bug-fix plan and patch")
    fix_parser.add_argument("prompt")
    fix_parser.add_argument("--language", default="python")

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
        }, indent=2))
        return

    if args.command == "generate":
        result = agent.generate_code(args.prompt, args.language)
        print(json.dumps(result, indent=2))
        return

    if args.command == "fix":
        result = agent.fix_bug(args.prompt, args.language)
        print(json.dumps(result, indent=2))
        return


if __name__ == "__main__":
    main()
