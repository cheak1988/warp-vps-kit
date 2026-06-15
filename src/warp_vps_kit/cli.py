from __future__ import annotations

import argparse
import sys

from .config import load_config, write_template
from .doctor import format_results, run_doctor
from .redact import redact_file
from .render import render_all


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="warp-vps-kit",
        description="Chinese-first VPS recovery and acceleration toolkit.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="write a starter config file")
    init.add_argument("--out", default="config.yaml")
    init.add_argument("--force", action="store_true")

    render = sub.add_parser("render", help="render Xray, Worker, Clash, and V2RayN configs")
    render.add_argument("--config", default="config.yaml")
    render.add_argument("--out", default="out")

    doctor = sub.add_parser("doctor", help="diagnose config and optional network checks")
    doctor.add_argument("--config", default="config.yaml")
    doctor.add_argument("--network", action="store_true")

    redact = sub.add_parser("redact", help="redact possible secrets from a text file")
    redact.add_argument("path")
    redact.add_argument("--check", action="store_true", help="do not write; exit 1 if changes found")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "init":
        path = write_template(args.out, force=args.force)
        print(f"created {path}")
        return 0

    if args.command == "render":
        config = load_config(args.config)
        files = render_all(config, args.out)
        for name, path in files.items():
            print(f"rendered {name}: {path}")
        return 0

    if args.command == "doctor":
        config = load_config(args.config)
        results = run_doctor(config, network=args.network)
        print(format_results(results))
        return 1 if any(item.level == "fail" for item in results) else 0

    if args.command == "redact":
        changed, redacted = redact_file(args.path, check=args.check)
        if args.check:
            if changed:
                print(redacted)
                print(f"possible secrets found in {args.path}", file=sys.stderr)
                return 1
            print(f"no secrets found in {args.path}")
            return 0
        print(f"redacted {args.path}" if changed else f"no changes: {args.path}")
        return 0

    return 2

