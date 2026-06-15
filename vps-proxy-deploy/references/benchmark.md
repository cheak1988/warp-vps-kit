# Benchmark

Do not promise guaranteed speed. Use measured language:

> Author-tested setup: smooth 4K YouTube playback on one low-cost VPS. Actual speed depends on VPS region, ISP, Cloudflare routing, WARP status, and time of day.

Test direct VPS outbound:

```bash
curl -L --max-time 30 -o /dev/null -w '%{speed_download}\n' https://speed.cloudflare.com/__down?bytes=50000000
```

Test WARP SOCKS5 outbound:

```bash
curl -L --max-time 30 --socks5 127.0.0.1:40000 -o /dev/null -w '%{speed_download}\n' https://speed.cloudflare.com/__down?bytes=50000000
```

Record:

- VPS provider and region.
- Client ISP.
- Time of day.
- Direct outbound speed.
- WARP outbound speed.
- YouTube/GitHub experience.

