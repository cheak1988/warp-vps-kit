#!/usr/bin/env bash
set -euo pipefail

RUN="${RUN:-0}"
VLESS_UUID="${VLESS_UUID:-}"
WS_PATH="${WS_PATH:-/ws}"
XRAY_PORT="${XRAY_PORT:-80}"

run() {
  if [[ "$RUN" == "1" ]]; then
    "$@"
  else
    printf '[dry-run] %q ' "$@"
    printf '\n'
  fi
}

if [[ -z "$VLESS_UUID" ]]; then
  echo "Set VLESS_UUID first."
  exit 1
fi

if [[ "${EUID:-$(id -u)}" -ne 0 ]]; then
  echo "Run this script as root on the VPS."
  exit 1
fi

echo "Installing Xray VLESS+WebSocket on port ${XRAY_PORT}, path ${WS_PATH}"
run bash -c 'curl -fsSL https://github.com/XTLS/Xray-install/raw/main/install-release.sh | bash -s -- install'

tmp_config="$(mktemp)"
cat > "$tmp_config" <<JSON
{
  "log": {"loglevel": "warning"},
  "dns": {"servers": ["8.8.8.8", "1.1.1.1"]},
  "inbounds": [{
    "port": ${XRAY_PORT},
    "protocol": "vless",
    "settings": {"clients": [{"id": "${VLESS_UUID}"}], "decryption": "none"},
    "streamSettings": {"network": "ws", "wsSettings": {"path": "${WS_PATH}"}}
  }],
  "outbounds": [{
    "protocol": "socks",
    "settings": {"servers": [{"address": "127.0.0.1", "port": 40000}]}
  }]
}
JSON

run install -m 0644 "$tmp_config" /usr/local/etc/xray/config.json
run systemctl enable xray
run systemctl restart xray
rm -f "$tmp_config"
echo "Done. If this was a dry run, rerun with RUN=1."

