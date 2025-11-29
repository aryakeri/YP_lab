import io
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest import mock

from passgen import commands


class HandleGenerateTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.storage_path = Path(self.tmpdir.name) / "store.json"

    def test_generate_saves_and_prints_password(self):
        args = SimpleNamespace(
            length=8,
            use_digits=True,
            use_special=False,
            use_uppercase=False,
            use_lowercase=True,
            save=True,
            label="custom-label",
            storage_file=str(self.storage_path),
        )
        with mock.patch("passgen.commands.generate_password", return_value="abc12345"):
            with mock.patch("sys.stdout", new_callable=io.StringIO) as stdout:
                status = commands.handle_generate(args)

        self.assertEqual(status, 0)
        output = stdout.getvalue()
        self.assertIn("abc12345", output)
        self.assertIn("label=custom-label", output)

        # Ensure entry persisted to the provided storage file.
        with self.storage_path.open("r", encoding="utf-8") as handle:
            stored = handle.read()
        self.assertIn("custom-label", stored)

    def test_generate_handles_validation_error(self):
        args = SimpleNamespace(
            length=1,
            use_digits=True,
            use_special=True,
            use_uppercase=True,
            use_lowercase=True,
            save=False,
            label=None,
            storage_file=None,
        )
        with mock.patch("passgen.commands.generate_password", side_effect=ValueError("too short")):
            with mock.patch("sys.stderr", new_callable=io.StringIO) as stderr:
                status = commands.handle_generate(args)

        self.assertEqual(status, 1)
        self.assertIn("Ошибка: too short", stderr.getvalue())


class HandleSearchTests(unittest.TestCase):
    def test_search_prints_entries(self):
        entry = {
            "label": "alpha",
            "hash": "deadbeef",
            "length": 12,
            "options": {"digits": True, "special": False},
            "created_at": "2024-01-01T00:00:00Z",
        }
        args = SimpleNamespace(label=None, password=None, storage_file=None)
        with mock.patch("passgen.commands.storage.search_passwords", return_value=([entry], Path("file.json"))):
            with mock.patch("sys.stdout", new_callable=io.StringIO) as stdout:
                status = commands.handle_search(args)

        self.assertEqual(status, 0)
        output = stdout.getvalue()
        self.assertIn("label: alpha", output)
        self.assertIn("options: digits", output)

    def test_search_handles_no_results(self):
        args = SimpleNamespace(label="query", password="secret", storage_file=None)
        with mock.patch("passgen.commands.storage.verify_password", return_value=([], Path("file.json"))):
            with mock.patch("sys.stdout", new_callable=io.StringIO) as stdout:
                status = commands.handle_search(args)

        self.assertEqual(status, 0)
        self.assertIn("Ничего не найдено", stdout.getvalue())


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
