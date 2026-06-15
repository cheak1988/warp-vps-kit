## Summary

## Test

```bash
python -m compileall vps-proxy-deploy/scripts
bash -n vps-proxy-deploy/scripts/*.sh
python vps-proxy-deploy/scripts/render_config.py --init config.yaml
python vps-proxy-deploy/scripts/render_config.py --config config.yaml --out out
python vps-proxy-deploy/scripts/doctor.py --config config.yaml
```

## Checklist

- [ ] No real IPs, UUIDs, tokens, or passwords are included.
- [ ] `vps-proxy-deploy/SKILL.md` or references updated if behavior changed.
- [ ] Tests added or updated.
