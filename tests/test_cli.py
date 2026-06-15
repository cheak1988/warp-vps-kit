import tempfile
import unittest
from pathlib import Path

from warp_vps_kit.cli import main


class CliTests(unittest.TestCase):
    def test_init_render_doctor_flow(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = root / "config.yaml"
            out = root / "out"

            self.assertEqual(main(["init", "--out", str(config)]), 0)
            self.assertTrue(config.exists())

            self.assertEqual(main(["render", "--config", str(config), "--out", str(out)]), 0)
            self.assertTrue((out / "xray-config.json").exists())
            self.assertTrue((out / "v2rayn-link.txt").exists())

            self.assertEqual(main(["doctor", "--config", str(config)]), 0)

    def test_init_existing_file_returns_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "config.yaml"
            config.write_text("domain: example.com\n", encoding="utf-8")
            self.assertEqual(main(["init", "--out", str(config)]), 2)


if __name__ == "__main__":
    unittest.main()

