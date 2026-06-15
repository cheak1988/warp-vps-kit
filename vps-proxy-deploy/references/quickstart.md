# Quickstart

## Required Inputs

```yaml
domain: example.com
proxy_subdomain: ws
config_subdomain: cfg
vps_host: 1.2.3.4
vless_uuid: VLESS_UUID_HERE
ws_path: /ws
client_name: MyVPS
```

Generate configs:

```bash
python vps-proxy-deploy/scripts/render_config.py --config config.yaml --out out
```

Cloudflare:

- Add A record `ws.example.com -> VPS_IP`.
- Enable Proxied / orange cloud.
- Deploy `out/worker.js` if using Worker config hosting.

VPS:

```bash
VLESS_UUID=VLESS_UUID_HERE WS_PATH=/ws RUN=1 bash vps-proxy-deploy/scripts/install-xray-ws.sh
RUN=1 bash vps-proxy-deploy/scripts/install-warp-proxy.sh
curl -s https://cfg.example.com/ > /usr/local/etc/xray/config.json
systemctl restart xray
```

Client:

- Clash Verge: import `out/clash-verge.yaml`.
- V2RayN: import `out/v2rayn-link.txt`.

Diagnosis:

```bash
python vps-proxy-deploy/scripts/doctor.py --config config.yaml --network
```

