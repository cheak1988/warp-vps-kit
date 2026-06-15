# Contributing

This is a skill-first repository. Keep the `vps-proxy-deploy/` folder useful when copied by itself into a Codex skills directory.

## Rules

- Put core agent instructions in `vps-proxy-deploy/SKILL.md`.
- Put long docs in `vps-proxy-deploy/references/`.
- Put deterministic helpers in `vps-proxy-deploy/scripts/`.
- Do not make the root README the main source of operational knowledge.
- Do not commit real IPs, UUIDs, tokens, passwords, or raw private logs.

## Validate

```bash
python -m compileall vps-proxy-deploy/scripts
python vps-proxy-deploy/scripts/render_config.py --init config.yaml
python vps-proxy-deploy/scripts/render_config.py --config config.yaml --out out
python vps-proxy-deploy/scripts/doctor.py --config config.yaml
python vps-proxy-deploy/scripts/redact.py README.md --check
```

