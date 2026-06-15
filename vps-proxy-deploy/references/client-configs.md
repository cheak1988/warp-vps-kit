# Client Configs

## Clash Verge

Use `ws.example.com` as `servername` and `Host`. The `server` field should usually be the Cloudflare-proxied hostname, not the raw VPS IP.

Include `default-nameserver` if DNS resolution fails:

```yaml
dns:
  enable: true
  default-nameserver:
    - 223.5.5.5
    - 119.29.29.29
```

## V2RayN

Use the generated `v2rayn-link.txt`. Check:

- `security=tls`
- `type=ws`
- `host=ws.example.com`
- `sni=ws.example.com`
- `path=/ws`

