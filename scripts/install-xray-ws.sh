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
  echo "Set VLESS_UUID before running, for example:"
  echo "VLESS_UUID=VLESS_UUID_HERE RUN=1 bash scripts/install-xray-ws.sh"
  exit 1
fi

if [[ "${EUID:-$(id -u)}" -ne 0 ]]; then
  echo "Run this script as root on the VPS."
  exit 1
fi

echo "Installing Xray VLESS+WebSocket on port ${XRAY_PORT} with path ${WS_PATH}"

run bash -c 'curl -fsSL https://github.com/XTLS/Xray-install/raw/main/install-release.sh | bash -s -- install'

CONFIG="/usr/local/etc/xray/config.json"
TMP_CONFIG="$(mktemp)"
cat > "$TMP_CONFIG" <<JSON
{
  "log": {"loglevel": "warning"},
  "dns": {"servers": ["8.8.8.8", "1.1.1.1"]},
  "inbounds": [
    {
      "port": ${XRAY_PORT},
      "protocol": "vless",
      "settings": {
        "clients": [{"id": "${VLESS_UUID}"}],
        "decryption": "none"
      },
      "streamSettings": {
        "network": "ws",
        "wsSettings": {"path": "${WS_PATH}"}
      }
    }
  ],
  "outbounds": [
    {
      "protocol": "socks",
      "settings": {
        "servers": [{"address": "127.0.0.1", "port": 40000}]
      }
    }
  ]
}
JSON

run install -m 0644 "$TMP_CONFIG" "$CONFIG"
run systemctl enable xray
run systemctl restart xray

rm -f "$TMP_CONFIG"
echo "Done. If this was a dry run, rerun with RUN=1."

