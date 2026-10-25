
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.document_loader import load_text_document


class TestDocumentLoader(unittest.TestCase):

    def test_load_text_document(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "sample.txt"
            file_path.write_text("Hello, AI research!", encoding="utf-8")

            result = load_text_document(str(file_path))

            self.assertEqual(result, "Hello, AI research!")

    def test_missing_document(self):
        with self.assertRaises(FileNotFoundError):
            load_text_document("missing_document.txt")

    def test_unsupported_file_type(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "sample.pdf"
            file_path.touch()

            with self.assertRaises(ValueError):
                load_text_document(str(file_path))

    def test_directory_instead_of_file(self):
        with TemporaryDirectory() as temp_dir, self.assertRaises(ValueError):
            load_text_document(temp_dir)


if __name__ == "__main__":
    unittest.main()
