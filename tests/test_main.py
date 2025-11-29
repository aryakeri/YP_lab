import io
import unittest
from unittest import mock

from passgen import main


class ParserTests(unittest.TestCase):
    def test_parser_sets_defaults_for_generate(self):
        parser = main.build_parser()
        args = parser.parse_args(["generate", "--length", "10", "--no-digits"])
        self.assertTrue(hasattr(args, "func"))
        self.assertEqual(args.length, 10)
        self.assertFalse(args.use_digits)
        self.assertTrue(args.use_special)
        self.assertTrue(args.use_uppercase)
        self.assertTrue(args.use_lowercase)


class MainDispatchTests(unittest.TestCase):
    def test_main_without_command_prints_help(self):
        with mock.patch("sys.stdout", new_callable=io.StringIO) as stdout:
            exit_code = main.main([])
        self.assertEqual(exit_code, 1)
        self.assertIn("usage:", stdout.getvalue().lower())

    def test_main_invokes_generate_handler(self):
        with mock.patch("passgen.main.commands.handle_generate", return_value=0) as handler:
            exit_code = main.main(["generate"])
        self.assertEqual(exit_code, 0)
        handler.assert_called_once()

    def test_main_invokes_search_handler(self):
        with mock.patch("passgen.main.commands.handle_search", return_value=0) as handler:
            exit_code = main.main(["search"])
        self.assertEqual(exit_code, 0)
        handler.assert_called_once()


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
