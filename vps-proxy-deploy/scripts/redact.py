#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


UUID_RE = re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b")
TOKEN_RE = re.compile(r"\b(?:cf[a-z0-9_-]{20,}|[A-Za-z0-9_-]{32,})\b")
IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
PASSWORD_LINE_RE = re.compile(r"(?i)(password\s*[:=]\s*)(\S+)")
ALLOW_IPS = {"1.1.1.1", "1.2.3.4", "8.8.8.8", "119.29.29.29", "127.0.0.1", "223.5.5.5"}


def redact_ip(match: re.Match[str]) -> str:
    value = match.group(0)
    if value in ALLOW_IPS:
        return value
    parts = value.split(".")
    if all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
        return "IP_REDACTED"
    return value


def redact_text(text: str) -> str:
    text = UUID_RE.sub("UUID_REDACTED", text)
    text = PASSWORD_LINE_RE.sub(r"\1PASSWORD_REDACTED", text)
    text = TOKEN_RE.sub("TOKEN_REDACTED", text)
    text = IPV4_RE.sub(redact_ip, text)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="Redact likely secrets before sharing logs.")
    parser.add_argument("path")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    path = Path(args.path)
    original = path.read_text(encoding="utf-8")
    redacted = redact_text(original)
    changed = redacted != original
    if args.check:
        if changed:
            print(redacted)
            return 1
        print(f"no secrets found in {path}")
        return 0
    if changed:
        path.write_text(redacted, encoding="utf-8")
        print(f"redacted {path}")
    else:
        print(f"no changes: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

