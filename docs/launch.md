# 首发 checklist

## GitHub 设置

- Repository name: `warp-vps-kit`
- Description: `低成本 VPS 复活与加速：Cloudflare CDN + WARP + Xray 自托管工具包`
- Topics:
  - `cloudflare`
  - `warp`
  - `vps`
  - `xray`
  - `vless`
  - `websocket`
  - `clash-verge`
  - `v2rayn`
  - `self-hosted`
  - `networking`

## 首发标题

```text
我把一台 $20/年的 VPS 用 Cloudflare CDN + WARP 救活了，整理成了开源工具包
```

更多平台文案见 [social-posts.md](social-posts.md)。

## 首发摘要

```text
便宜 VPS 的 IP 被直连干扰后，不一定只能换 IP 或扔掉。

我把这两天踩坑整理成了一个开源项目：warp-vps-kit。
核心思路是：
- Cloudflare CDN 做免费入口中转，隐藏源站 IP
- WARP proxy mode 做 VPS 出口加速
- Worker 托管 Xray 配置，避免 VNC 手输长 JSON
- 自动生成 Clash Verge / V2RayN 配置
- doctor 命令诊断 525、DNS、WARP、UUID/path 等常见坑

我的低价 VPS 实测可以流畅 4K YouTube，但不保证所有线路复现。
项目更准确的定位是：低成本 VPS 复活与加速工具包。
```

## 发布前必须确认

- [ ] 没有提交真实 IP、UUID、token、密码。
- [ ] `python -m unittest discover -s tests` 通过。
- [ ] `python -m compileall src tests` 通过。
- [ ] GitHub Actions 首次运行通过。
