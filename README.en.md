# warp-vps-kit

`warp-vps-kit` is a low-cost self-hosted VPS recovery and acceleration toolkit using Cloudflare CDN, WARP proxy mode, and open-source proxy tools.

It is written Chinese-first because the original pain point is very specific: cheap VPS origins that become unstable or unreachable from some networks, while the server itself still works.

## What it does

- Moves ingress behind Cloudflare CDN so clients do not connect to the VPS origin IP directly.
- Routes outbound traffic through Cloudflare WARP proxy mode.
- Generates Xray, Worker, Clash Verge, and V2RayN configs.
- Provides diagnostics for common DNS, WebSocket, WARP, and config mismatch failures.
- Keeps the setup self-hosted: your VPS, your domain, your configs.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .

warp-vps-kit init --out config.yaml
warp-vps-kit render --config config.yaml --out out
warp-vps-kit doctor --config config.yaml
```

See [README.md](README.md) for the complete Chinese guide.

## FAQ

The short version: this does not unblock an origin IP. It moves client ingress to Cloudflare CDN and uses WARP proxy mode for outbound traffic. If Cloudflare can still reach the VPS origin, a direct-connect-broken VPS may become usable again.

