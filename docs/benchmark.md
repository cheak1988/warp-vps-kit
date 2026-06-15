# Benchmark 方法

不要把“4K 流畅”写成保证。建议用可复现的方式记录你的结果。

## 测试项

1. 直连 VPS 出口：

```bash
curl -L --max-time 30 -o /dev/null -w '%{speed_download}\n' https://speed.cloudflare.com/__down?bytes=50000000
```

2. 通过 WARP SOCKS5：

```bash
curl -L --max-time 30 --socks5 127.0.0.1:40000 -o /dev/null -w '%{speed_download}\n' https://speed.cloudflare.com/__down?bytes=50000000
```

3. 客户端体感：

- YouTube 1080p / 2K / 4K 是否缓冲。
- GitHub clone 是否稳定。
- Google 搜索打开速度。

## 结果模板

```text
VPS provider:
Region:
OS:
Client ISP:
Time:

Direct VPS outbound:
WARP proxy outbound:
Cloudflare CDN + WARP client:
YouTube:
GitHub:
Notes:
```

## 发布建议

README 中可以写：

> 作者在一台低价 VPS 上实测，开启 Cloudflare CDN + WARP proxy mode 后可流畅播放 4K YouTube。

不要写：

> 保证 4K、保证 8 倍、永久免费高速。

