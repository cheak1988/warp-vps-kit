# 架构说明

`warp-vps-kit` 把一台 VPS 拆成两个方向来看：

- 入口：用户如何连到 VPS。
- 出口：VPS 如何访问互联网。

传统直连方式的问题是入口和出口都依赖 VPS 自身线路。一旦 VPS IP 直连受阻，或者机房出口质量差，整套服务就会变得不稳定。

本项目的方案：

```text
Client
  -> Cloudflare CDN
  -> VPS origin
  -> WARP proxy mode
  -> Internet
```

## 入口：Cloudflare CDN

`ws.example.com` 指向 VPS IP，并开启 Cloudflare orange cloud。客户端连接 `ws.example.com:443`，Cloudflare 再回源到 VPS 的 Xray WebSocket 服务。

这有两个好处：

- 客户端不直接连接 VPS IP。
- 源站 IP 不暴露给普通客户端配置。

## 出口：WARP proxy mode

WARP full tunnel 会改 VPS 的默认路由，可能导致 Cloudflare 回源流量也被绕走，进而让入口失效。

所以本项目使用 proxy mode：

```text
Xray outbound -> SOCKS5 127.0.0.1:40000 -> WARP -> Internet
```

入口仍由 VPS 正常接收，出口流量再交给 WARP。

## 配置托管：Cloudflare Worker

VNC 控制台复制长 JSON 很容易出错。Worker 可以托管一份 Xray 配置，让 VPS 通过 `curl` 下载，减少手工输入错误。

