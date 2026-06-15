# Troubleshooting

## Cloudflare 525

Likely causes:

- Cloudflare expects TLS to origin but Xray is listening as HTTP/WebSocket on port 80.
- `ws.example.com` is not orange-cloud proxied.
- Xray is not listening on port 80.

Fix:

- Confirm orange cloud.
- Confirm Xray listens on `:80`.
- Use the chosen Cloudflare SSL mode consistently with HTTP origin.

## Client alive=false

Likely causes:

- UUID mismatch.
- WebSocket path mismatch.
- `Host` or SNI is not `ws.example.com`.
- VPS config is stale.

Regenerate and restart:

```bash
python vps-proxy-deploy/scripts/render_config.py --config config.yaml --out out
curl -s https://cfg.example.com/ > /usr/local/etc/xray/config.json
systemctl restart xray
```

## WARP broke ingress

Likely cause: WARP full tunnel changed the VPS default route.

Fix:

```bash
warp-cli --accept-tos mode proxy
warp-cli --accept-tos connect
curl -s --socks5 127.0.0.1:40000 https://ifconfig.me
```

## SSH is still bad

Do not spend too long debugging direct SSH from a poor network. Use the provider VNC console for rescue. After proxy works, harden SSH with keys, a non-standard port, and fail2ban.

