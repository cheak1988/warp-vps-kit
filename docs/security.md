# 安全和发布前检查

## 不要提交的内容

- VPS 真实 IP。
- root 密码。
- Cloudflare API token。
- 真实 VLESS UUID。
- 私有域名的完整配置。
- VPS 故障排查原始日志。

## 发布前扫描

```bash
warp-vps-kit redact README.md --check
warp-vps-kit redact examples/config.example.yaml --check
```

## SSH 救援配置

文档中出现的 `PermitRootLogin yes` 和 `PasswordAuthentication yes` 只适合救援阶段。部署完成后建议：

```bash
sed -i 's/^PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sed -i 's/^PermitRootLogin yes/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config
systemctl restart ssh
```

## Cloudflare token

首版默认不自动调用 Cloudflare API。后续如果启用自动化，应使用最小权限 token，并支持部署后撤销。

