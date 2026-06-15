#!/usr/bin/env bash
set -euo pipefail

echo "== system =="
uname -a || true
uptime || true

echo
echo "== xray =="
systemctl is-active xray || true
systemctl status xray --no-pager -l | sed -n '1,12p' || true
ss -tlnp | grep -E ':(80|443|40000)\b' || true

echo
echo "== warp =="
warp-cli --accept-tos status || true
curl -s --max-time 8 --socks5 127.0.0.1:40000 https://ifconfig.me || true
echo

