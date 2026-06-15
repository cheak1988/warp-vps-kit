# Security

Do not post real VPS origin IPs, root passwords, Cloudflare API tokens, VLESS UUIDs, private domains, or raw diagnostic logs in public issues.

Use:

```bash
python vps-proxy-deploy/scripts/redact.py your-file.txt --check
```

If a security-sensitive issue is found, open a minimal public issue without secrets and describe the category of problem.

