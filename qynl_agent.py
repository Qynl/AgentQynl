"""Qynl Agent: a small, extensible tool-using AI agent."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = os.getenv("QYNL_MODEL", "gpt-5-mini")
MAX_STEPS = int(os.getenv("QYNL_MAX_STEPS", "12"))

SYSTEM_PROMPT = """You are Qynl, a capable personal AI agent.
You plan tasks, use available tools, inspect their results, and continue until the user's goal is complete.
Be concise but explain important actions. Never claim an action succeeded unless a tool confirms it.
Before destructive filesystem or shell operations, ask for approval through the approval tool.
Never expose secrets or environment variables.
"""


def approval(action: str, reason: str) -> str:
    """Require explicit terminal approval for a potentially consequential action."""
    answer = input(f"\n[QYNL APPROVAL] {action}\nReason: {reason}\nApprove? [y/N]: ").strip().lower()
    return "approved" if answer in {"y", "yes"} else "denied"


def read_file(path: str) -> str:
    """Read a UTF-8 text file."""
    return Path(path).read_text(encoding="utf-8")


def list_directory(path: str = ".") -> str:
    """List files in a directory."""
    p = Path(path)
    return json.dumps([x.name for x in p.iterdir()], indent=2)


def write_file(path: str, content: str) -> str:
    """Write a UTF-8 text file after approval."""
    if approval(f"Write file: {path}", "This changes data on disk.") != "approved":
        return "denied by user"
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return f"wrote {path}"


def run_command(command: str) -> str:
    """Run a shell command after explicit approval."""
    if approval(f"Run command: {command}", "Shell commands can modify the system.") != "approved":
        return "denied by user"
    result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
    return json.dumps({"returncode": result.returncode, "stdout": result.stdout[-12000:], "stderr": result.stderr[-12000:]})


TOOLS = [
    {"type": "function", "name": "read_file", "description": "Read a UTF-8 text file.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
    {"type": "function", "name": "list_directory", "description": "List a directory.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}}},
    {"type": "function", "name": "write_file", "description": "Write a UTF-8 file. Requires approval.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}},
    {"type": "function", "name": "run_command", "description": "Run a shell command. Requires approval.", "parameters": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]}},
]

FUNCTIONS = {"read_file": read_file, "list_directory": list_directory, "write_file": write_file, "run_command": run_command}


def execute(user_message: str) -> str:
    client = OpenAI()
    messages: list[Any] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    for _ in range(MAX_STEPS):
        response = client.responses.create(model=MODEL, input=messages, tools=TOOLS)
        output_items = response.output
        messages.extend(output_items)

        calls = [item for item in output_items if getattr(item, "type", None) == "function_call"]
        if not calls:
            return response.output_text

        for call in calls:
            try:
                args = json.loads(call.arguments)
                result = FUNCTIONS[call.name](**args)
            except Exception as exc:
                result = f"tool error: {type(exc).__name__}: {exc}"
            messages.append({"type": "function_call_output", "call_id": call.call_id, "output": str(result)})

    return "Stopped after reaching the maximum tool steps."


if __name__ == "__main__":
    print("Qynl Agent online. Type 'exit' to quit.")
    while True:
        try:
            user = input("\nYou > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if user.lower() in {"exit", "quit"}:
            break
        if user:
            print(f"\nQynl > {execute(user)}")
