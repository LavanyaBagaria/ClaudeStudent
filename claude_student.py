#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"
DEFAULT_MODEL = "claude-3-5-sonnet-latest"


def call_claude(prompt: str, max_tokens: int, model: str) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Missing ANTHROPIC_API_KEY environment variable.")

    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }

    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "x-api-key": api_key,
            "anthropic-version": API_VERSION,
            "content-type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Claude API request failed ({exc.code}): {detail}") from exc

    content_items = body.get("content", [])
    text_items = [item for item in content_items if item.get("type") == "text"]
    text_blocks = [item.get("text", "") for item in text_items]
    return "\n".join(block for block in text_blocks if block).strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send a prompt to Claude and print the response.")
    parser.add_argument("prompt", help="Prompt to send to Claude")
    parser.add_argument("--max-tokens", type=int, default=512, help="Maximum tokens in the response")
    parser.add_argument("--model", default=os.getenv("CLAUDE_MODEL", DEFAULT_MODEL), help="Claude model name")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.max_tokens <= 0:
        print("--max-tokens must be a positive integer.", file=sys.stderr)
        return 2

    try:
        output = call_claude(args.prompt, args.max_tokens, args.model)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if output:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
