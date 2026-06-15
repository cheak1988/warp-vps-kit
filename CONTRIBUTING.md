# Contributing

欢迎贡献。这个项目的目标不是堆协议，而是把“低价 VPS 复活与加速”这件事做得可复现、可诊断、可维护。

## 什么贡献最有价值

- 不同 VPS 机房、运营商、地区的 benchmark。
- Cloudflare 525、DNS、WARP、WebSocket、客户端配置失败案例。
- 更安全的默认配置。
- 更清楚的中文文档和截图。
- 不依赖真实账号的自动化测试。

## 提交前检查

```bash
python -m unittest discover -s tests
python -m compileall src tests
warp-vps-kit redact README.md --check
warp-vps-kit redact examples/config.example.yaml --check
```

如果你在 Linux/macOS 或 GitHub Actions 中：

```bash
bash -n scripts/*.sh
```

## 不要提交

- 真实 VPS IP。
- 真实 UUID。
- Cloudflare API token。
- root 密码。
- 私有域名完整配置。
- 原始故障日志。

请先用：

```bash
warp-vps-kit redact your-file.txt --check
```

## 文案原则

- README 中文优先，英文简版跟进。
- 避免承诺“永久可用”“保证 4K”“永久免费高速”。
- 可以写个人实测，但要说明线路和时间会影响结果。
- 项目定位用“自托管网络网关 / VPS 复活与加速 / Cloudflare CDN + WARP”，不要写成黑盒托管服务。

