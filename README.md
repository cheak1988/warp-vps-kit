# warp-vps-kit

> 一台便宜 VPS 直连废了，不一定真的废了。  
> 只要 Cloudflare 还能回源，就可以把它改造成 **Cloudflare CDN 入口 + WARP 出口加速** 的自托管网络网关。

[![CI](https://github.com/cheak1988/warp-vps-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/cheak1988/warp-vps-kit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 一句话

`warp-vps-kit` 是一个中文首发的开源工具包：**把一台便宜 VPS 从“直连废了、出口很慢、配置容易错”改造成“Cloudflare CDN 中转入口 + WARP proxy mode 加速出口 + 可诊断配置”的自托管网络网关。**

## 项目亮点

| 你遇到的问题 | 这个项目做什么 |
| --- | --- |
| VPS IP 直连被干扰 | 客户端走 Cloudflare CDN，不再直连源站 IP |
| 便宜 VPS 出口慢 | Xray 出站走 WARP SOCKS5 proxy mode |
| VNC 里配置容易输错 | 用 Worker 托管 Xray 配置，VPS `curl` 拉取 |
| Clash/V2RayN 配置细节多 | 自动生成客户端配置和 VLESS 链接 |
| 失败时不知道错哪 | `doctor` 诊断 DNS、TCP、WebSocket、占位符 |
| 怕误传敏感信息 | `redact` 扫描 IP、UUID、token、password |

## 这个项目解决什么问题

很多人买了每年 20-25 美元的低价 VPS，刚开始还能用，过一阵就会遇到：

- VPS IP 直连受阻，SSH 抽风，端口连着连着就不稳定。
- 节点能连但速度很慢，YouTube、GitHub、Google 体验很差。
- 买订阅服务不放心，数据和节点都不在自己手里。
- 网上教程很多，但坑位分散，照着做很容易卡两天。

`warp-vps-kit` 把这些坑整理成一个可复现的工具包：

- 用 **Cloudflare CDN** 做免费入口中转，隐藏 VPS 真实 IP。
- 用 **Cloudflare WARP proxy mode** 做 VPS 出口加速。
- 用 **Cloudflare Workers** 托管配置，避免 VNC 复制长 JSON 时出错。
- 用 **Xray/VLESS/WebSocket** 提供自托管代理服务。
- 生成 **Clash Verge / V2RayN** 客户端配置。
- 提供 `doctor` 诊断命令定位 525、DNS、UUID/path、WARP full tunnel 等常见问题。

作者实测：低价 VPS 方案在特定线路下可流畅播放 4K YouTube。实际速度取决于 VPS 机房、运营商、Cloudflare 路由、时间段和配置，不保证每台机器都复现同样结果。

## 架构

```text
Client
  -> Cloudflare CDN (ws.example.com:443, orange cloud)
  -> VPS origin (Xray VLESS+WS on :80)
  -> WARP SOCKS5 proxy (127.0.0.1:40000)
  -> Internet
```

这不是给 VPS IP 真正“解封”。它的核心是：**用户不再直连 VPS IP，而是通过 Cloudflare 边缘节点回源到 VPS**。如果 Cloudflare 仍能连接你的 VPS，那么原来直连不可用的服务就有机会恢复。

## 能救什么，不能救什么

适合：

- VPS IP 从本地直连很不稳定，但 VPS 本身还活着。
- SSH 从本地经常卡住，但 VNC 或国外网络还能进机器。
- 代理端口直连失败，希望改成 CDN 中转入口。
- VPS 出口线路慢，希望用 WARP proxy mode 改善出站路径。
- 想用便宜 VPS 自己掌控节点和配置。

不适合：

- VPS 已被服务商关停、null route 或机器本身故障。
- Cloudflare 无法回源到你的 VPS。
- 域名、DNS、Cloudflare 线路本身不可用。
- VPS 无法安装或连接 WARP。
- 期待“永久免费、永远高速、永远可用”的托管服务。

更多边界说明见 [FAQ](docs/faq.md)。

## 快速开始

```bash
# clone this repository first, then:
cd warp-vps-kit
python -m venv .venv
source .venv/bin/activate
pip install -e .

warp-vps-kit init --out config.yaml
```

30 秒看效果：

```bash
warp-vps-kit render --config config.yaml --out out
warp-vps-kit doctor --config config.yaml
```

示例输出：

```text
rendered xray-config.json: out/xray-config.json
rendered worker.js: out/worker.js
rendered clash-verge.yaml: out/clash-verge.yaml
rendered v2rayn-link.txt: out/v2rayn-link.txt
rendered next-steps.md: out/next-steps.md
[WARN] config: domain still uses placeholder value: example.com
[WARN] config: vps_host still uses placeholder value: 1.2.3.4
[WARN] config: vless_uuid still uses placeholder value: VLESS_UUID_HERE
[OK] config: basic config shape is valid
[INFO] network: skipped network checks; pass --network to enable
```

完整演示见 [CLI Demo](docs/demo.md)。

编辑 `config.yaml`：

```yaml
domain: example.com
proxy_subdomain: ws
config_subdomain: cfg
vps_host: 1.2.3.4
vless_uuid: VLESS_UUID_HERE
ws_path: /ws
client_name: MyVPS
```

生成配置：

```bash
warp-vps-kit render --config config.yaml --out out
```

输出目录会包含：

- `out/xray-config.json`：VPS 上的 Xray 配置。
- `out/worker.js`：Cloudflare Worker 配置托管脚本。
- `out/clash-verge.yaml`：Clash Verge 配置片段。
- `out/v2rayn-link.txt`：V2RayN 导入链接。
- `out/next-steps.md`：部署步骤提醒。

诊断配置：

```bash
warp-vps-kit doctor --config config.yaml
warp-vps-kit doctor --config config.yaml --network
```

发布前扫描敏感信息：

```bash
warp-vps-kit redact README.md --check
warp-vps-kit redact out/xray-config.json --check
```

## Cloudflare 设置要点

最容易配错的是这里：

- `ws.example.com` 指向 VPS IP，必须开启 **Proxied / orange cloud**。
- Cloudflare 到 VPS 的回源端口用 `80`，Xray 监听 `80`。
- 该方案默认用 Flexible/HTTP 回源思路，客户端到 Cloudflare 仍是 TLS。
- Worker 只用于托管配置，避免在 VNC 里手敲长 JSON。

如果 `ws.example.com` 是灰云 DNS-only，客户端仍可能直连 VPS，CDN 中转和隐藏源站 IP 就不会生效。

## VPS 端脚本

脚本默认是 dry run，不会直接改机器。确认后传 `RUN=1`：

```bash
VLESS_UUID=VLESS_UUID_HERE WS_PATH=/ws RUN=1 bash scripts/install-xray-ws.sh
RUN=1 bash scripts/install-warp-proxy.sh
bash scripts/doctor-vps.sh
```

建议先通过 VPS 服务商 VNC 执行初始化。直连 SSH 不稳定时，不要把排查时间浪费在本地 SSH 客户端上。

## 和普通一键脚本有什么不同

普通一键脚本通常假设 SSH 能稳定连接、VPS IP 能直连、用户能顺利复制配置。这个项目针对的是更狼狈但很常见的情况：

- VPS 还活着，但本地直连已经很差。
- SSH 不稳定，只能靠 VNC 救援。
- 配置稍微错一个 UUID/path/Host 就全线失败。
- Cloudflare/WARP 的模式选错会让入口或出口互相打架。

所以首版选择“工具包 + 教程 + 诊断”，先保证每一步可解释、可验证，再逐步做自动化。

## 安全提醒

- `PermitRootLogin yes` 和 `PasswordAuthentication yes` 只适合救援阶段，完成后应改回密钥登录和非 root 管理。
- 不要把真实 IP、UUID、Cloudflare token、root 密码提交到 GitHub。
- Cloudflare API token 请只给最小权限，用完可撤销。
- 请遵守所在地法律、VPS 服务商条款和 Cloudflare 服务条款。

## 路线图

- [x] 配置生成器：Xray / Worker / Clash Verge / V2RayN。
- [x] 本地 doctor：占位符、DNS、TCP、WebSocket 基础检查。
- [x] 敏感信息扫描：IP、UUID、token、password 模式。
- [x] 中文 FAQ、benchmark 方法、首发文案和社区模板。
- [ ] Cloudflare API 自动创建 DNS 和 Worker。
- [ ] 交互式 TUI 安装器。
- [ ] 多协议模板：Trojan、Reality fallback、Hysteria2 对比。
- [ ] 英文文档完善。

## 参考资料

- [Cloudflare Workers documentation](https://developers.cloudflare.com/workers/)
- [Cloudflare WARP documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-devices/warp/)
- [XTLS/Xray-install](https://github.com/XTLS/Xray-install)

## License

MIT
