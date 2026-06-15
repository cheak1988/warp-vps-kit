# 首发传播文案

## V2EX / NodeSeek 标题

```text
我把低价 VPS 复活方案做成了一个 AI Skill：丢给 AI，它带你用 Cloudflare CDN + WARP 跑通
```

## V2EX / NodeSeek 正文

```text
前两天折腾一台低价 VPS：IP 直连不稳定，SSH 抽风，代理端口也经常失败。

最后整理出一套能复现的思路：

- Cloudflare CDN 做入口中转，客户端不再直连 VPS 源站 IP
- Xray VLESS + WebSocket 跑在 VPS :80
- WARP proxy mode 做 VPS 出口加速，不用 full tunnel，避免打断回源
- Worker 托管 Xray 配置，VNC 救援时不用手敲长 JSON
- 生成 Clash Verge / V2RayN 配置
- 诊断 Cloudflare 525、DNS、WebSocket、UUID/path、WARP 模式等常见坑

很多用户不懂 Cloudflare、Xray、WARP、Clash 的细节，让 AI 按 skill 一步步问、生成配置、排查错误，会比自己抄命令更方便。

项目地址：
https://github.com/cheak1988/vps-proxy-deploy

一句话：把这个 skill 丢给支持 Skills 的 AI，它会引导你把一台还活着但直连很差的低价 VPS，改造成 Cloudflare CDN 入口 + WARP 出口的自托管网络网关。

不是解封 IP，也不保证所有 VPS 都能救活。本质是改入口路径 + 优化出口路径。
```

## HostLoc 简短版

```text
做了一个低价 VPS 复活/加速 AI Skill：vps-proxy-deploy

不是普通一键脚本。把 skill 丢给 AI，它会带你：
- 配 CF CDN 入口，隐藏源站 IP
- 配 Xray VLESS+WS
- 配 WARP proxy mode 出口
- 用 Worker 托管配置
- 生成 Clash/V2RayN
- 排查 525、DNS、WebSocket、WARP 模式错误

项目：
https://github.com/cheak1988/vps-proxy-deploy
```

## X / Twitter 中文版

```text
把低价 VPS 复活方案做成了一个 AI Skill。

丢给支持 Skills 的 AI，它会引导你用：
Cloudflare CDN + Xray VLESS/WS + WARP proxy mode
把直连很差但机器还活着的 VPS 改造成自托管网络网关。

https://github.com/cheak1988/vps-proxy-deploy
```

## Telegram 群版

```text
开源了一个低价 VPS 复活与加速 AI Skill：
https://github.com/cheak1988/vps-proxy-deploy

适合这种场景：VPS IP 直连很差/像废了，但机器还活着，Cloudflare 还能回源。

把 skill 丢给 AI，它会带你走完整流程：CF CDN 入口、Xray VLESS WS、WARP proxy mode 出口、Worker 托管配置、Clash/V2RayN 输出、doctor 诊断。
```

## 避免这样写

- “永久免费高速”
- “保证 4K”
- “一键绕过所有封锁”
- “所有 VPS 都能复活”

这些话会降低可信度，也会给项目带来不必要风险。
