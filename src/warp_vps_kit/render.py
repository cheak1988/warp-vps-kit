from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote, urlencode

from .config import KitConfig


def xray_config(config: KitConfig) -> dict:
    return {
        "log": {"loglevel": "warning"},
        "dns": {"servers": ["8.8.8.8", "1.1.1.1"]},
        "inbounds": [
            {
                "port": config.xray_inbound_port,
                "protocol": "vless",
                "settings": {
                    "clients": [{"id": config.vless_uuid}],
                    "decryption": "none",
                },
                "streamSettings": {
                    "network": "ws",
                    "wsSettings": {"path": config.ws_path},
                },
            }
        ],
        "outbounds": [
            {
                "protocol": "socks",
                "settings": {
                    "servers": [
                        {
                            "address": config.warp_socks_host,
                            "port": config.warp_socks_port,
                        }
                    ]
                },
            }
        ],
    }


def worker_js(config: KitConfig) -> str:
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


def clash_yaml(config: KitConfig) -> str:
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

dns:
  enable: true
  default-nameserver:
    - 223.5.5.5
    - 119.29.29.29
  nameserver:
    - 223.5.5.5
    - 119.29.29.29
"""


def v2rayn_link(config: KitConfig) -> str:
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
    name = quote(config.client_name)
    return f"vless://{config.vless_uuid}@{config.client_target}:443?{params}#{name}"


def next_steps(config: KitConfig) -> str:
    return f"""# Next steps

1. In Cloudflare DNS, create an A record:
   - Name: `{config.proxy_subdomain}`
   - Target: `{config.vps_host}`
   - Proxy status: Proxied / orange cloud

2. Deploy `worker.js` to a Cloudflare Worker and bind it to:
   - `https://{config.config_host}/*`

3. On the VPS, install Xray and WARP proxy mode:
   - `VLESS_UUID={config.vless_uuid} WS_PATH={config.ws_path} RUN=1 bash scripts/install-xray-ws.sh`
   - `RUN=1 bash scripts/install-warp-proxy.sh`

4. Download the generated Xray config on the VPS:
   - `curl -s https://{config.config_host}/ > /usr/local/etc/xray/config.json`
   - `systemctl restart xray`

5. Import `clash-verge.yaml` or `v2rayn-link.txt` into your client.

6. Run diagnostics:
   - `warp-vps-kit doctor --config config.yaml --network`
"""


def render_all(config: KitConfig, output_dir: str | Path) -> dict[str, Path]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    files = {
        "xray-config.json": json.dumps(xray_config(config), ensure_ascii=False, indent=2)
        + "\n",
        "worker.js": worker_js(config),
        "clash-verge.yaml": clash_yaml(config),
        "v2rayn-link.txt": v2rayn_link(config) + "\n",
        "next-steps.md": next_steps(config),
    }
    written: dict[str, Path] = {}
    for name, content in files.items():
        path = out / name
        path.write_text(content, encoding="utf-8")
        written[name] = path
    return written

