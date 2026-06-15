# Security Policy

## Reporting

如果你发现安全问题，请不要在公开 issue 中贴真实 IP、token、UUID、密码或日志。

可以先开一个不含敏感信息的 issue，描述问题类型和影响范围。维护者会再约定安全传递细节的方式。

## Secrets

这个项目默认不需要 Cloudflare API token。后续如果使用自动化 Cloudflare API 功能，请只授予最小权限，并在部署后撤销不再需要的 token。

发布 issue 或 PR 前请运行：

```bash
warp-vps-kit redact README.md --check
warp-vps-kit redact your-log.txt --check
```

## Supported Versions

当前项目处于 `0.x` 阶段，API 和 CLI 可能调整。安全修复会优先进入最新版本。

