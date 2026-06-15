#!/usr/bin/env python3
from __future__ import annotations

import argparse
import socket
import ssl
from pathlib import Path


PLACEHOLDERS = {"example.com", "1.2.3.4", "VLESS_UUID_HERE"}


def parse_config(path: Path) -> dict:
    data = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().split(" #", 1)[0]
    return data


def tcp_connect(host: str, port: int, timeout: float = 5.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def websocket_handshake(host: str, path: str, timeout: float = 8.0) -> bool:
    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n"
        "Sec-WebSocket-Version: 13\r\n"
        "\r\n"
    )
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, 443), timeout=timeout) as raw:
            with ctx.wrap_socket(raw, server_hostname=host) as wrapped:
                wrapped.settimeout(timeout)
                wrapped.sendall(request.encode("ascii"))
                response = wrapped.recv(4096)
        return response.startswith(b"HTTP/1.1 101") or b" 101 " in response
    except OSError:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Diagnose vps-proxy-deploy config.")
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--network", action="store_true")
    args = parser.parse_args()
    data = parse_config(Path(args.config))
    failed = False

    for key in ["domain", "proxy_subdomain", "vps_host", "vless_uuid"]:
        value = data.get(key, "")
        if not value:
            print(f"[FAIL] missing {key}")
            failed = True
        elif value in PLACEHOLDERS:
            print(f"[WARN] {key} is still placeholder: {value}")

    domain = data.get("domain", "example.com")
    proxy_subdomain = data.get("proxy_subdomain", "ws")
    proxy_host = f"{proxy_subdomain}.{domain}"
    ws_path = data.get("ws_path", "/ws") or "/ws"
    if not ws_path.startswith("/"):
        print("[FAIL] ws_path must start with /")
        failed = True
    if not failed:
        print("[OK] basic config shape is valid")

    if not args.network:
        print("[INFO] network checks skipped; pass --network to enable")
        return 1 if failed else 0

    try:
        addresses = sorted({item[4][0] for item in socket.getaddrinfo(proxy_host, 443)})
        print(f"[OK] DNS {proxy_host}: {', '.join(addresses)}")
    except OSError as exc:
        print(f"[FAIL] DNS {proxy_host}: {exc}")
        return 1

    print("[OK] TCP 443 reachable" if tcp_connect(proxy_host, 443) else "[FAIL] TCP 443 failed")
    print(
        "[OK] WebSocket upgrade returned 101"
        if websocket_handshake(proxy_host, ws_path)
        else "[WARN] WebSocket did not return 101; check Xray/path/Cloudflare"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

