#!/usr/bin/env bash
set -euo pipefail

RUN="${RUN:-0}"

run() {
  if [[ "$RUN" == "1" ]]; then
    "$@"
  else
    printf '[dry-run] %q ' "$@"
    printf '\n'
  fi
}

if [[ "${EUID:-$(id -u)}" -ne 0 ]]; then
  echo "Run this script as root on the VPS."
  exit 1
fi

if ! command -v apt-get >/dev/null 2>&1; then
  echo "This script currently supports Debian/Ubuntu systems with apt-get."
  exit 1
fi

echo "Installing Cloudflare WARP and enabling proxy mode on 127.0.0.1:40000"

run apt-get update
run apt-get install -y curl gpg lsb-release
run bash -c 'curl -fsSL https://pkg.cloudflareclient.com/pubkey.gpg | gpg --dearmor -o /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg'
run bash -c 'echo "deb [signed-by=/usr/share/keyrings/cloudflare-warp-archive-keyring.gpg] https://pkg.cloudflareclient.com/ $(lsb_release -cs) main" > /etc/apt/sources.list.d/cloudflare-client.list'
run apt-get update
run apt-get install -y cloudflare-warp
run warp-cli --accept-tos registration new
run warp-cli --accept-tos mode proxy
run warp-cli --accept-tos connect
run warp-cli --accept-tos status

echo "Done. Verify with:"
echo "curl -s --socks5 127.0.0.1:40000 https://ifconfig.me"

