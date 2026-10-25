
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.result_saver import save_result


class TestResultSaver(unittest.TestCase):
    def test_saves_text_result(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_directory = Path(temporary_directory) / "outputs"

            with patch("src.result_saver.Path.resolve",
                return_value=output_directory.parent / "src" / "result_saver.py",
            ):
                saved_path = save_result(
                    content="This is a test summary.",
                    filename="test_summary.txt",
                )

            self.assertTrue(saved_path.exists())
            self.assertEqual(
                saved_path.read_text(encoding="utf-8"),
                "This is a test summary.",
            )
            self.assertEqual(saved_path.name, "test_summary.txt")

    def test_rejects_empty_content(self) -> None:
        with self.assertRaisesRegex(ValueError, "Content cannot be empty"):
            save_result("", "summary.txt")

    def test_rejects_non_string_content(self) -> None:
        with self.assertRaises(TypeError):
            save_result(123, "summary.txt")

    def test_rejects_empty_filename(self) -> None:
        with self.assertRaisesRegex(ValueError, "Filename cannot be empty"):
            save_result("Summary text", " ")

    def test_rejects_filename_with_directory_path(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            "Filename must not contain a directory path",
        ):
            save_result("Summary text", "../summary.txt")

    def test_rejects_non_text_filename_extension(self) -> None:
        with self.assertRaisesRegex(ValueError, "Filename must end with .txt"):
            save_result("Summary text", "summary.csv")


if __name__ == "__main__":
    unittest.main()
