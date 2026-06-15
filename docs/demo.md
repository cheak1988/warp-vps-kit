# CLI Demo

## 生成配置模板

```bash
warp-vps-kit init --out config.yaml
```

输出：

```text
created config.yaml
```

## 生成 Xray / Worker / 客户端配置

```bash
warp-vps-kit render --config config.yaml --out out
```

输出：

```text
rendered xray-config.json: out/xray-config.json
rendered worker.js: out/worker.js
rendered clash-verge.yaml: out/clash-verge.yaml
rendered v2rayn-link.txt: out/v2rayn-link.txt
rendered next-steps.md: out/next-steps.md
```

## 检查配置

```bash
warp-vps-kit doctor --config config.yaml
```

输出：

```text
[WARN] config: domain still uses placeholder value: example.com
[WARN] config: vps_host still uses placeholder value: 1.2.3.4
[WARN] config: vless_uuid still uses placeholder value: VLESS_UUID_HERE
[OK] config: basic config shape is valid
[INFO] network: skipped network checks; pass --network to enable
```

## 扫描敏感信息

```bash
warp-vps-kit redact README.md --check
```

输出：

```text
no secrets found in README.md
```

