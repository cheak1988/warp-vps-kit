# 首发传播文案

## V2EX / NodeSeek 标题

```text
我把一台 $20/年的 VPS 用 Cloudflare CDN + WARP 救活了，整理成了开源工具包
```

## V2EX / NodeSeek 正文

```text
前两天折腾一台低价 VPS：IP 直连不稳定，SSH 抽风，代理端口也经常失败。

后来整理出一套相对稳定的方案：

- Cloudflare CDN 做入口中转，客户端不再直连 VPS 源站 IP
- Xray VLESS + WebSocket 跑在 VPS :80
- WARP proxy mode 做 VPS 出口加速，不用 full tunnel，避免打断回源
- Worker 托管 Xray 配置，VNC 救援时不用手敲长 JSON
- 自动生成 Clash Verge / V2RayN 配置
- doctor 命令检查 DNS、TCP、WebSocket、UUID/path、占位符等常见坑

我自己的低价 VPS 实测可以流畅 4K YouTube，但这个不做保证，速度取决于机房、运营商、Cloudflare 路由和时间段。

项目地址：
https://github.com/cheak1988/warp-vps-kit

更准确地说，这不是“解封 IP”，而是把用户入口从直连 VPS 改成 Cloudflare CDN 回源。只要 Cloudflare 还能连到源站，原来直连废掉的 VPS 就有机会复活。

欢迎提 benchmark，尤其是不同 VPS 商家和地区的测试结果。
```

## HostLoc 简短版

```text
整理了一个低价 VPS 复活/加速工具包：warp-vps-kit

思路：
- CF CDN 做入口，隐藏源站 IP
- Xray VLESS+WS 跑源站
- WARP proxy mode 做出口加速
- Worker 托管配置
- 自动生成 Clash/V2RayN
- doctor 检查常见坑

项目：
https://github.com/cheak1988/warp-vps-kit

不是保证满血，也不是解封 IP。本质是改入口路径 + 优化出口路径。
```

## X / Twitter 中文版

```text
把一台 $20/年的 VPS 救活了。

核心思路：
Cloudflare CDN 做入口中转，WARP proxy mode 做出口加速，Xray/VLESS/WS 跑源站。

我整理成了开源工具包：
https://github.com/cheak1988/warp-vps-kit

适合低价 VPS 直连不稳定、SSH 抽风、节点端口失败但机器本身还活着的情况。
```

## Telegram 群版

```text
开源了一个低价 VPS 复活与加速工具包：
https://github.com/cheak1988/warp-vps-kit

适合这种场景：VPS IP 直连很差/像废了，但机器还活着，Cloudflare 还能回源。

方案：CF CDN 入口 + Xray VLESS WS + WARP proxy mode 出口 + Worker 托管配置。
已经带配置生成器、doctor 诊断、Clash/V2RayN 输出。
```

## 避免这样写

- “永久免费高速”
- “保证 4K”
- “一键绕过所有封锁”
- “所有 VPS 都能复活”

这些话会降低可信度，也会给项目带来不必要风险。

