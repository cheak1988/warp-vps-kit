import tempfile
import unittest
from pathlib import Path

from warp_vps_kit.config import KitConfig, parse_simple_yaml, validate_config
from warp_vps_kit.render import clash_yaml, render_all, v2rayn_link, xray_config


class ConfigRenderTests(unittest.TestCase):
    def test_parse_simple_yaml(self):
        data = parse_simple_yaml(
            """
            domain: example.com
            proxy_subdomain: ws
            xray_inbound_port: 80
            allow_insecure: true
            """
        )
        self.assertEqual(data["domain"], "example.com")
        self.assertEqual(data["xray_inbound_port"], 80)
        self.assertIs(data["allow_insecure"], True)

    def test_render_outputs(self):
        config = KitConfig(
            domain="example.com",
            proxy_subdomain="ws",
            config_subdomain="cfg",
            vps_host="1.2.3.4",
            vless_uuid="VLESS_UUID_HERE",
        )
        xray = xray_config(config)
        self.assertEqual(xray["inbounds"][0]["streamSettings"]["wsSettings"]["path"], "/ws")
        self.assertIn("servername: ws.example.com", clash_yaml(config))
        self.assertIn("vless://VLESS_UUID_HERE@ws.example.com:443", v2rayn_link(config))

    def test_render_all_writes_files(self):
        config = KitConfig(
            domain="example.com",
            proxy_subdomain="ws",
            config_subdomain="cfg",
            vps_host="1.2.3.4",
            vless_uuid="VLESS_UUID_HERE",
        )
        with tempfile.TemporaryDirectory() as tmp:
            files = render_all(config, tmp)
            self.assertTrue((Path(tmp) / "worker.js").exists())
            self.assertIn("clash-verge.yaml", files)

    def test_validate_warns_on_placeholders(self):
        config = KitConfig(
            domain="example.com",
            proxy_subdomain="ws",
            config_subdomain="cfg",
            vps_host="1.2.3.4",
            vless_uuid="VLESS_UUID_HERE",
        )
        findings = validate_config(config)
        self.assertTrue(any(level == "warn" for level, _ in findings))


if __name__ == "__main__":
    unittest.main()

