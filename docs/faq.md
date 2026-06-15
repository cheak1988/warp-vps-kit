# FAQ

## 已经被 GFW 影响的 VPS IP，还能用这套方案复活吗？

有机会，但不是“解封 IP”。

这套方案救的是这种情况：

```text
本地用户 -> VPS IP 直连不稳定或不可用
Cloudflare -> VPS IP 仍然可以回源
VPS 本机仍然正常运行
```

改造后变成：

```text
用户客户端 -> Cloudflare 边缘节点 -> VPS -> WARP proxy mode -> Internet
```

所以用户不再直接连接 VPS IP。看起来像 VPS 复活了，本质是入口路径换成了 Cloudflare CDN。

## 什么情况救不了？

- VPS 被服务商关停。
- VPS 被 null route。
- Cloudflare 也无法回源到 VPS。
- 域名或 Cloudflare 边缘线路不可用。
- VPS 无法安装或连接 WARP。
- 客户端配置仍然写 VPS IP，绕过了 Cloudflare。

## 为什么不用 WARP full tunnel？

WARP full tunnel 会改变 VPS 默认路由，可能让 Cloudflare 回源流量也被绕走，导致入口断掉。

本项目使用 proxy mode：

```text
Xray outbound -> 127.0.0.1:40000 SOCKS5 -> WARP
```

入口保持正常，出口交给 WARP。

## 为什么要用 Cloudflare Worker 托管配置？

很多低价 VPS 初次救援只能用服务商 VNC。VNC 里复制长 JSON、UUID、特殊符号很容易错。

Worker 托管配置后，VPS 只需要：

```bash
curl -s https://cfg.example.com/ > /usr/local/etc/xray/config.json
```

这比手敲配置稳定得多。

## 这是不是一键脚本？

首版不是纯一键脚本，而是“工具包 + 教程 + 诊断”。

原因是 Cloudflare、域名、VPS、客户端环境差异很大。先把配置生成、关键路径和坑位诊断做稳，比盲目一键更靠谱。

## 4K YouTube 一定能流畅吗？

不保证。

作者在自己的低价 VPS 上实测可以流畅 4K，但速度受 VPS 机房、运营商、Cloudflare 路由、WARP 状态和时间段影响。请用 [benchmark](benchmark.md) 里的方法记录自己的结果。

## 这和买订阅服务有什么区别？

区别是控制权。

- VPS 是你的。
- 域名是你的。
- 配置是你的。
- 日志和数据路径更可控。

代价是你需要自己维护 VPS、域名、Cloudflare 和客户端配置。

