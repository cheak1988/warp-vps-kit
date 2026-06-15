from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


PLACEHOLDERS = {
    "example.com",
    "1.2.3.4",
    "VLESS_UUID_HERE",
    "your_api_token_here",
    "your_password",
}


TEMPLATE = """# warp-vps-kit config
# Keep this file private. Do not commit real IPs, UUIDs, tokens, or passwords.

domain: example.com
proxy_subdomain: ws
config_subdomain: cfg
vps_host: 1.2.3.4
vless_uuid: VLESS_UUID_HERE
ws_path: /ws
client_name: MyVPS

# Advanced defaults
client_server:
xray_inbound_port: 80
warp_socks_host: 127.0.0.1
warp_socks_port: 40000
allow_insecure: true
"""


@dataclass(frozen=True)
class KitConfig:
    domain: str
    proxy_subdomain: str
    config_subdomain: str
    vps_host: str
    vless_uuid: str
    ws_path: str = "/ws"
    client_name: str = "MyVPS"
    client_server: str = ""
    xray_inbound_port: int = 80
    warp_socks_host: str = "127.0.0.1"
    warp_socks_port: int = 40000
    allow_insecure: bool = True

    @property
    def proxy_host(self) -> str:
        return f"{self.proxy_subdomain}.{self.domain}"

    @property
    def config_host(self) -> str:
        return f"{self.config_subdomain}.{self.domain}"

    @property
    def client_target(self) -> str:
        return self.client_server or self.proxy_host


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    lowered = value.lower()
    if lowered in {"true", "yes"}:
        return True
    if lowered in {"false", "no"}:
        return False
    if lowered.isdigit():
        return int(lowered)
    return value


def parse_simple_yaml(text: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.split(" #", 1)[0]
        data[key] = parse_scalar(value)
    return data


def load_config(path: str | Path) -> KitConfig:
    data = parse_simple_yaml(Path(path).read_text(encoding="utf-8"))
    required = ["domain", "proxy_subdomain", "config_subdomain", "vps_host", "vless_uuid"]
    missing = [field for field in required if not data.get(field)]
    if missing:
        raise ValueError(f"Missing required config fields: {', '.join(missing)}")
    allowed = set(KitConfig.__dataclass_fields__)
    values = {key: value for key, value in data.items() if key in allowed}
    return KitConfig(**values)


def validate_config(config: KitConfig) -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    values = {
        "domain": config.domain,
        "vps_host": config.vps_host,
        "vless_uuid": config.vless_uuid,
    }
    for key, value in values.items():
        if str(value) in PLACEHOLDERS:
            findings.append(("warn", f"{key} still uses placeholder value: {value}"))
    if not config.ws_path.startswith("/"):
        findings.append(("fail", "ws_path must start with '/'"))
    if config.xray_inbound_port != 80:
        findings.append(
            (
                "warn",
                "xray_inbound_port is not 80; make sure Cloudflare can reach this port.",
            )
        )
    if config.client_server and config.client_server == config.vps_host:
        findings.append(
            (
                "warn",
                "client_server equals vps_host; clients may bypass Cloudflare CDN.",
            )
        )
    return findings


def write_template(path: str | Path, force: bool = False) -> Path:
    output = Path(path)
    if output.exists() and not force:
        raise FileExistsError(f"{output} already exists. Use --force to overwrite.")
    output.write_text(TEMPLATE, encoding="utf-8")
    return output
