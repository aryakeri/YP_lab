import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from passgen import storage, utils


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.storage_path = Path(self.tmpdir.name) / "passwords.json"

    def test_search_returns_empty_for_missing_file(self):
        entries, path = storage.search_passwords(storage_file=str(self.storage_path))
        self.assertEqual(entries, [])
        self.assertEqual(path, self.storage_path.resolve())

    def test_store_and_verify_password(self):
        entry, path = storage.store_password(
            "secret",
            label="label-one",
            length=12,
            options={"digits": True},
            storage_file=str(self.storage_path),
        )
        self.assertEqual(path, self.storage_path.resolve())
        self.assertTrue(self.storage_path.exists())
        self.assertEqual(entry["label"], "label-one")
        self.assertEqual(entry["hash"], utils.hash_password("secret"))

        entries, _ = storage.verify_password("secret", storage_file=str(self.storage_path))
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["label"], "label-one")

    def test_label_filtering(self):
        storage.store_password(
            "secret-one",
            label="alpha",
            length=8,
            options={},
            storage_file=str(self.storage_path),
        )
        storage.store_password(
            "secret-two",
            label="beta",
            length=8,
            options={},
            storage_file=str(self.storage_path),
        )

        entries, _ = storage.search_passwords(label_query="alp", storage_file=str(self.storage_path))
        self.assertEqual([entry["label"] for entry in entries], ["alpha"])

    def test_invalid_json_raises_value_error(self):
        self.storage_path.write_text("{invalid json", encoding="utf-8")
        with self.assertRaises(ValueError):
            storage.search_passwords(storage_file=str(self.storage_path))

    def test_non_list_storage_raises_value_error(self):
        self.storage_path.write_text(json.dumps({"not": "a list"}), encoding="utf-8")
        with self.assertRaises(ValueError):
            storage.search_passwords(storage_file=str(self.storage_path))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
