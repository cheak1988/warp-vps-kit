# 快速部署清单

## 1. 准备

- 一台 VPS。
- 一个托管在 Cloudflare 的域名。
- VPS 服务商 VNC 控制台。
- 本地 Python 3.9+。

## 2. 生成配置

```bash
warp-vps-kit init --out config.yaml
warp-vps-kit render --config config.yaml --out out
```

## 3. Cloudflare DNS

创建：

```text
Type: A
Name: ws
Target: VPS_IP
Proxy status: Proxied / orange cloud
```

创建 Worker route：

```text
cfg.example.com/*
```

Worker 内容使用 `out/worker.js`。

## 4. VPS

```bash
VLESS_UUID=VLESS_UUID_HERE WS_PATH=/ws RUN=1 bash scripts/install-xray-ws.sh
RUN=1 bash scripts/install-warp-proxy.sh
curl -s https://cfg.example.com/ > /usr/local/etc/xray/config.json
systemctl restart xray
```

## 5. 客户端

导入：

- Clash Verge：`out/clash-verge.yaml`
- V2RayN：`out/v2rayn-link.txt`

## 6. 诊断

```bash
warp-vps-kit doctor --config config.yaml --network
bash scripts/doctor-vps.sh
```

