#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote, urlencode


TEMPLATE = """domain: example.com
proxy_subdomain: ws
config_subdomain: cfg
vps_host: 1.2.3.4
vless_uuid: VLESS_UUID_HERE
ws_path: /ws
client_name: MyVPS
client_server:
xray_inbound_port: 80
warp_socks_host: 127.0.0.1
warp_socks_port: 40000
allow_insecure: true
"""


@dataclass(frozen=True)
class Config:
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


def parse_scalar(value: str):
    value = value.strip()
    if not value:
        return ""
    if value.lower() in {"true", "yes"}:
        return True
    if value.lower() in {"false", "no"}:
        return False
    if value.isdigit():
        return int(value)
    return value


def parse_config(path: Path) -> Config:
    data = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = parse_scalar(value.split(" #", 1)[0])
    required = ["domain", "proxy_subdomain", "config_subdomain", "vps_host", "vless_uuid"]
    missing = [key for key in required if not data.get(key)]
    if missing:
        raise SystemExit(f"missing required fields: {', '.join(missing)}")
    allowed = set(Config.__dataclass_fields__)
    return Config(**{key: value for key, value in data.items() if key in allowed})


def xray_config(config: Config) -> dict:
    return {
        "log": {"loglevel": "warning"},
        "dns": {"servers": ["8.8.8.8", "1.1.1.1"]},
        "inbounds": [
            {
                "port": config.xray_inbound_port,
                "protocol": "vless",
                "settings": {"clients": [{"id": config.vless_uuid}], "decryption": "none"},
                "streamSettings": {"network": "ws", "wsSettings": {"path": config.ws_path}},
            }
        ],
        "outbounds": [
            {
                "protocol": "socks",
                "settings": {
                    "servers": [
                        {"address": config.warp_socks_host, "port": config.warp_socks_port}
                    ]
                },
            }
        ],
    }


def worker_js(config: Config) -> str:
    cfg = json.dumps(xray_config(config), ensure_ascii=False, indent=2)
    return f"""export default {{
  async fetch() {{
    const cfg = {cfg};
    return new Response(JSON.stringify(cfg, null, 2), {{
      headers: {{ "content-type": "application/json; charset=utf-8" }}
    }});
  }}
}};
"""


def clash_yaml(config: Config) -> str:
    allow = "true" if config.allow_insecure else "false"
    return f"""proxies:
  - name: {config.client_name}
    type: vless
    server: {config.client_target}
    port: 443
    uuid: {config.vless_uuid}
    udp: true
    tls: true
    servername: {config.proxy_host}
    skip-cert-verify: {allow}
    network: ws
    ws-opts:
      path: {config.ws_path}
      headers:
        Host: {config.proxy_host}
"""


def v2rayn_link(config: Config) -> str:
    params = urlencode(
        {
            "encryption": "none",
            "type": "ws",
            "host": config.proxy_host,
            "path": config.ws_path,
            "security": "tls",
            "sni": config.proxy_host,
            "allowInsecure": "1" if config.allow_insecure else "0",
        }
    )
    return f"vless://{config.vless_uuid}@{config.client_target}:443?{params}#{quote(config.client_name)}"


def next_steps(config: Config) -> str:
    return f"""# Next steps

1. Cloudflare DNS: create A `{config.proxy_subdomain}` -> `{config.vps_host}` with Proxied / orange cloud.
2. Deploy `worker.js` to route `https://{config.config_host}/*` if using Worker config hosting.
3. VPS:
   - `VLESS_UUID={config.vless_uuid} WS_PATH={config.ws_path} RUN=1 bash scripts/install-xray-ws.sh`
   - `RUN=1 bash scripts/install-warp-proxy.sh`
   - `curl -s https://{config.config_host}/ > /usr/local/etc/xray/config.json`
   - `systemctl restart xray`
4. Client: import `clash-verge.yaml` or `v2rayn-link.txt`.
5. Diagnose: `python scripts/doctor.py --config config.yaml --network`.
"""


def render(config: Config, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    files = {
        "xray-config.json": json.dumps(xray_config(config), ensure_ascii=False, indent=2) + "\n",
        "worker.js": worker_js(config),
        "clash-verge.yaml": clash_yaml(config),
        "v2rayn-link.txt": v2rayn_link(config) + "\n",
        "next-steps.md": next_steps(config),
    }
    for name, content in files.items():
        path = out / name
        path.write_text(content, encoding="utf-8")
        print(f"rendered {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render VPS proxy configs for the skill.")
    parser.add_argument("--init", metavar="PATH", help="write starter config and exit")
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--out", default="out")
    args = parser.parse_args()
    if args.init:
        path = Path(args.init)
        path.write_text(TEMPLATE, encoding="utf-8")
        print(f"created {path}")
        return 0
    render(parse_config(Path(args.config)), Path(args.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

