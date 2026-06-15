---
name: vps-proxy-deploy
description: >
  Help users recover and accelerate a low-cost self-hosted VPS proxy using
  Cloudflare CDN as ingress, WARP proxy mode as outbound acceleration, and
  Xray/VLESS/WebSocket client configs. Use for VPS direct-connect failures,
  Cloudflare 525 troubleshooting, WARP mode mistakes, Clash Verge/V2RayN config
  generation, and safe secret redaction before publishing.
---

# VPS Proxy Deploy

Use this skill when a user wants to turn a cheap VPS into a self-hosted network gateway with:

- Cloudflare CDN orange-cloud ingress.
- Xray VLESS + WebSocket on the VPS origin.
- Cloudflare WARP proxy mode as outbound SOCKS5.
- Clash Verge and V2RayN client configs.
- Diagnostics for common setup failures.

## Required Inputs

- `domain`: Cloudflare-managed domain, for example `example.com`.
- `proxy_subdomain`: proxy hostname, for example `ws`.
- `config_subdomain`: config Worker hostname, for example `cfg`.
- `vps_host`: VPS origin IP or hostname.
- `vless_uuid`: generated VLESS UUID.
- `ws_path`: WebSocket path, usually `/ws`.

## Recommended Flow

1. Run `warp-vps-kit init --out config.yaml`.
2. Fill placeholders in `config.yaml`.
3. Run `warp-vps-kit render --config config.yaml --out out`.
4. Create Cloudflare DNS record `ws.example.com -> VPS_IP` with orange cloud enabled.
5. Deploy `out/worker.js` to Cloudflare Workers if using config hosting.
6. On the VPS, run the Xray and WARP scripts with `RUN=1`.
7. Import generated Clash Verge or V2RayN config.
8. Run `warp-vps-kit doctor --config config.yaml --network`.

## Critical Notes

- `ws.example.com` must be Cloudflare-proxied if the goal is to avoid direct client connections to the VPS IP.
- WARP should use `proxy` mode, not full tunnel mode, to avoid breaking Cloudflare ingress.
- Root password login is acceptable only during rescue; switch to SSH keys afterward.
- Never publish real IPs, UUIDs, passwords, or Cloudflare API tokens.

