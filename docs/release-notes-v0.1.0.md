# v0.1.0 Release Notes

`warp-vps-kit` 的第一版目标很简单：把“低价 VPS 被直连干扰后如何复活并加速”这件事整理成一个能复现的开源工具包。

## Highlights

- 中文首发 README，围绕 `$20/年 VPS + Cloudflare 免费组件 + WARP proxy mode` 这个真实痛点展开。
- CLI 支持生成 Xray、Worker、Clash Verge、V2RayN 配置。
- `doctor` 命令检查占位符、DNS、TCP、WebSocket 基础问题。
- `redact` 命令帮助发布前扫描 IP、UUID、token、password。
- VPS 端脚本默认 dry run，需要 `RUN=1` 才会执行修改。

## Known Limits

- 首版不自动调用 Cloudflare API。
- 首版不保证所有 VPS/地区复现同样速度。
- Windows 本地如未安装 Git Bash，shell 脚本语法检查建议交给 GitHub Actions。

## Suggested GitHub Description

```text
低成本 VPS 复活与加速：Cloudflare CDN + WARP + Xray 自托管工具包
```

