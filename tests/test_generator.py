import string
import unittest

from passgen import generator


class GeneratePasswordTests(unittest.TestCase):
    def test_generates_digits_only(self):
        password = generator.generate_password(
            10,
            use_digits=True,
            use_special=False,
            use_uppercase=False,
            use_lowercase=False,
        )
        self.assertEqual(len(password), 10)
        self.assertTrue(all(char in string.digits for char in password))

    def test_requires_length_for_selected_charsets(self):
        with self.assertRaises(ValueError):
            generator.generate_password(
                1,
                use_digits=True,
                use_special=False,
                use_uppercase=False,
                use_lowercase=True,
            )

    def test_contains_at_least_one_character_from_each_charset(self):
        password = generator.generate_password(
            6,
            use_digits=True,
            use_special=False,
            use_uppercase=True,
            use_lowercase=True,
        )
        self.assertTrue(any(char in string.digits for char in password))
        self.assertTrue(any(char in string.ascii_lowercase for char in password))
        self.assertTrue(any(char in string.ascii_uppercase for char in password))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
