import unittest

from warp_vps_kit.redact import redact_text


class RedactTests(unittest.TestCase):
    def test_redacts_uuid_token_password_and_ip(self):
        text = (
            "uuid=123e4567-e89b-12d3-a456-426614174000\n"
            "token=cfabcdefabcdefabcdefabcdefabcdef\n"
            "password: supersecret\n"
            "origin=198.51.100.10\n"
        )
        redacted = redact_text(text)
        self.assertIn("UUID_REDACTED", redacted)
        self.assertIn("TOKEN_REDACTED", redacted)
        self.assertIn("PASSWORD_REDACTED", redacted)
        self.assertIn("IP_REDACTED", redacted)

    def test_keeps_public_dns_and_examples(self):
        text = "1.1.1.1 8.8.8.8 223.5.5.5 119.29.29.29 127.0.0.1 1.2.3.4"
        self.assertEqual(redact_text(text), text)


if __name__ == "__main__":
    unittest.main()
