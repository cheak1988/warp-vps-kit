# Architecture

The skill solves two separate problems:

- Ingress: how the client reaches the VPS.
- Egress: how the VPS reaches the internet.

Recommended path:

```text
Client
  -> Cloudflare CDN (ws.example.com:443, orange cloud)
  -> VPS origin (Xray VLESS+WS on :80)
  -> WARP SOCKS5 proxy (127.0.0.1:40000)
  -> Internet
```

Cloudflare CDN hides the origin from the client configuration and avoids direct client-to-VPS traffic. WARP proxy mode improves outbound routing without changing the VPS default route.

This is not an IP unblock. It is service recovery through path replacement. It works only if the VPS still runs and Cloudflare can still reach the origin.

