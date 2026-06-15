from __future__ import annotations

import socket
import ssl
from dataclasses import dataclass

from .config import KitConfig, validate_config


@dataclass
class CheckResult:
    level: str
    name: str
    message: str


def tcp_connect(host: str, port: int, timeout: float = 5.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def websocket_handshake(host: str, path: str, servername: str, timeout: float = 8.0) -> bool:
    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {servername}\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n"
        "Sec-WebSocket-Version: 13\r\n"
        "\r\n"
    )
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, 443), timeout=timeout) as raw:
            with ctx.wrap_socket(raw, server_hostname=servername) as wrapped:
                wrapped.settimeout(timeout)
                wrapped.sendall(request.encode("ascii"))
                response = wrapped.recv(4096)
        return b" 101 " in response or response.startswith(b"HTTP/1.1 101")
    except OSError:
        return False


def run_doctor(config: KitConfig, network: bool = False) -> list[CheckResult]:
    results: list[CheckResult] = []
    for level, message in validate_config(config):
        results.append(CheckResult(level, "config", message))

    if not any(item.level == "fail" for item in results):
        results.append(CheckResult("ok", "config", "basic config shape is valid"))

    if not network:
        results.append(
            CheckResult("info", "network", "skipped network checks; pass --network to enable")
        )
        return results

    try:
        records = socket.getaddrinfo(config.proxy_host, 443, proto=socket.IPPROTO_TCP)
        addresses = sorted({record[4][0] for record in records})
        results.append(
            CheckResult("ok", "dns", f"{config.proxy_host} resolves to {', '.join(addresses)}")
        )
    except OSError as exc:
        results.append(CheckResult("fail", "dns", f"cannot resolve {config.proxy_host}: {exc}"))
        return results

    if tcp_connect(config.proxy_host, 443):
        results.append(CheckResult("ok", "tcp", f"{config.proxy_host}:443 is reachable"))
    else:
        results.append(CheckResult("fail", "tcp", f"{config.proxy_host}:443 is not reachable"))

    if websocket_handshake(config.proxy_host, config.ws_path, config.proxy_host):
        results.append(CheckResult("ok", "websocket", "WebSocket upgrade returned 101"))
    else:
        results.append(
            CheckResult(
                "warn",
                "websocket",
                "WebSocket upgrade did not return 101; check UUID/path/Xray/Cloudflare mode",
            )
        )

    return results


def format_results(results: list[CheckResult]) -> str:
    labels = {"ok": "OK", "info": "INFO", "warn": "WARN", "fail": "FAIL"}
    return "\n".join(
        f"[{labels.get(item.level, item.level.upper())}] {item.name}: {item.message}"
        for item in results
    )

