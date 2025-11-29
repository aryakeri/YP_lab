import string
import unittest
from datetime import datetime
from unittest import mock

from passgen import utils


class BuildCharsetsTests(unittest.TestCase):
    def test_all_disabled_raises(self):
        with self.assertRaises(ValueError):
            utils.build_charsets(
                include_lower=False,
                include_upper=False,
                include_digits=False,
                include_special=False,
            )

    def test_selected_charsets_are_returned_in_order(self):
        charsets = utils.build_charsets(
            include_lower=True,
            include_upper=False,
            include_digits=True,
            include_special=False,
        )
        self.assertEqual(charsets, [string.ascii_lowercase, string.digits])


class ValidateLengthTests(unittest.TestCase):
    def test_length_below_minimum_raises(self):
        with self.assertRaises(ValueError):
            utils.validate_length(1, min_required=2)

    def test_valid_length_is_returned(self):
        self.assertEqual(utils.validate_length(5, min_required=2), 5)


class HashingAndLabelsTests(unittest.TestCase):
    def test_hash_password_is_deterministic(self):
        expected = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        self.assertEqual(utils.hash_password("abc"), expected)

    def test_current_timestamp_is_iso_format(self):
        timestamp = utils.current_timestamp()
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        self.assertEqual(parsed.tzinfo.utcoffset(parsed).total_seconds(), 0)
        self.assertTrue(timestamp.endswith("Z"))
        self.assertIn("T", timestamp)

    def test_default_label_uses_timestamp(self):
        with mock.patch("passgen.utils.current_timestamp", return_value="2024-01-01T00:00:00Z"):
            self.assertEqual(utils.default_label(), "entry-2024-01-01T00:00:00Z")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
