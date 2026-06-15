# 常见问题

## Cloudflare 525

症状：客户端或 WebSocket 检查返回 525。

常见原因：

- Cloudflare 使用 Full/Strict SSL，但 VPS 端只有 HTTP 回源。
- Xray 没有监听 `80`。
- DNS 记录没有开启 orange cloud。

处理：

- 确认 `ws.example.com` 是 Proxied。
- 确认 Xray 监听 `80`。
- 如果采用 Flexible/HTTP 回源，Cloudflare 到源站不应期待 TLS。

## 客户端显示 alive=false

常见原因：

- `uuid` 不一致。
- `ws_path` 不一致。
- `Host` / `servername` 不等于 `ws.example.com`。
- VPS 上配置还是旧版本。

处理：

```bash
warp-vps-kit render --config config.yaml --out out
curl -s https://cfg.example.com/ > /usr/local/etc/xray/config.json
systemctl restart xray
```

## 开 WARP 后入口失效

常见原因：使用了 WARP full tunnel，VPS 默认路由被改掉，Cloudflare 回源连接被影响。

处理：使用 proxy mode。

```bash
warp-cli --accept-tos mode proxy
warp-cli --accept-tos connect
curl -s --socks5 127.0.0.1:40000 https://ifconfig.me
```

## SSH 仍然很难连

这套方案的重点不是修 SSH 直连，而是让代理服务通过 Cloudflare 入口恢复。初始配置建议用 VPS 服务商 VNC。

完成后可以通过代理环境再 SSH，或改用密钥登录、非 22 端口和 fail2ban。

