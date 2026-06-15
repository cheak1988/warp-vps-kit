# Security

Never ask the user to paste real root passwords or Cloudflare API tokens into public chat.

Do not publish:

- VPS origin IP.
- Root password.
- Cloudflare API token.
- Real VLESS UUID.
- Private domain configs.
- Raw diagnostic logs.

Before sharing logs:

```bash
python vps-proxy-deploy/scripts/redact.py your-file.txt --check
```

SSH rescue settings such as `PermitRootLogin yes` and `PasswordAuthentication yes` are temporary. Switch back to key-based login after recovery.

