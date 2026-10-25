import unittest

from src.text_chunker import create_chunk_records, split_text


class TestTextChunker(unittest.TestCase):
    def test_split_text_into_expected_chunks(self):
        text = "A" * 1200

        chunks = split_text(text)

        self.assertEqual(len(chunks), 3)
        self.assertEqual([len(chunk) for chunk in chunks], [500, 500, 300])

    def test_chunks_preserve_overlap(self):
        text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        chunks = split_text(text, chunk_size=10, overlap=3)

        self.assertEqual(chunks[0][-3:], chunks[1][:3])
        self.assertEqual(chunks[1][-3:], chunks[2][:3])

    def test_empty_text_returns_empty_list(self):
        self.assertEqual(split_text(""), [])

    def test_text_shorter_than_chunk_size(self):
        self.assertEqual(split_text("Hello", chunk_size=10, overlap=2), ["Hello"])

    def test_invalid_chunk_size(self):
        with self.assertRaises(ValueError):
            split_text("Hello", chunk_size=0)

    def test_negative_overlap(self):
        with self.assertRaises(ValueError):
            split_text("Hello", overlap=-1)

    def test_overlap_must_be_smaller_than_chunk_size(self):
        with self.assertRaises(ValueError):
            split_text("Hello", chunk_size=10, overlap=10)

    def test_non_string_input(self):
        with self.assertRaises(TypeError):
            split_text(123)

    def test_create_chunk_records_includes_source_and_index(self):
        records = create_chunk_records(
                text="abcdefghijkl",
                source="sample.txt",
                chunk_size=10,
                overlap=2,
            )

        self.assertEqual(len(records), 2)

        self.assertEqual(
            records[0],
            {
                "text": "abcdefghij",
                "source": "sample.txt",
                "chunk_index": 1,
            },
        )

        self.assertEqual(
            records[1],
            {
                "text": "ijkl",
                "source": "sample.txt",
                "chunk_index": 2,
            },
        )

    def test_create_chunk_records_with_empty_text(self):
        records = create_chunk_records(
            text="",
            source="empty.txt",
        )

        self.assertEqual(records, [])


if __name__ == "__main__":
    unittest.main()
