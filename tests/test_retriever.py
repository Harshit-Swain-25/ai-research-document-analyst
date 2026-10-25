
import unittest

from src.retriever import retrieve_relevant_chunks


class TestRetriever(unittest.TestCase):
    def setUp(self):
        self.chunk_records = [
            {
                "text": "Document analysis systems support answers with evidence.",
                "source": "research.txt",
                "chunk_index": 1,
            },
            {
                "text": "Python is a popular programming language.",
                "source": "python.txt",
                "chunk_index": 1,
            },
            {
                "text": "Language models can summarize documents and answer questions.",
                "source": "research.txt",
                "chunk_index": 2,
            },
        ]

    def test_retrieves_relevant_chunks(self):
        results = retrieve_relevant_chunks(
            "How do document systems support answers with evidence?",
            self.chunk_records,
        )

        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]["source"], "research.txt")
        self.assertEqual(results[0]["chunk_index"], 1)

    def test_returns_no_results_for_unmatched_query(self):
        results = retrieve_relevant_chunks(
            "volcano ocean mountain",
            self.chunk_records,
        )

        self.assertEqual(results, [])

    def test_returns_empty_list_for_empty_query(self):
        results = retrieve_relevant_chunks(
            "",
            self.chunk_records,
        )

        self.assertEqual(results, [])

    def test_respects_top_k(self):
        results = retrieve_relevant_chunks(
            "documents answers",
            self.chunk_records,
            top_k=1,
        )

        self.assertEqual(len(results), 1)

    def test_rejects_invalid_top_k(self):
        with self.assertRaises(ValueError):
            retrieve_relevant_chunks(
                "documents",
                self.chunk_records,
                top_k=0,
            )

    
    def test_ignores_common_words_in_unrelated_query(self):
        results = retrieve_relevant_chunks(
            "What is the capital of Japan?",
            self.chunk_records,
        )

        self.assertEqual(results, [])

    def test_returns_empty_for_stop_words_only(self):
        results = retrieve_relevant_chunks(
            "what is the",
            self.chunk_records,
        )

        self.assertEqual(results, [])



if __name__ == "__main__":
    unittest.main()
