
import unittest
from unittest.mock import patch

from src.llm_client import generate_answer, summarize_document


class TestLLMClient(unittest.TestCase):
    def setUp(self) -> None:
        self.query = "What does the document say?"
        self.chunks = [
            {
                "text": "Document analysis should use evidence.",
                "source": "sample.txt",
                "chunk_index": 1,
            }
        ]

    @patch("src.llm_client.genai.Client")
    @patch("src.llm_client.os.getenv", return_value="fake-test-key")
    def test_generates_answer_from_retrieved_evidence(
        self,
        mock_getenv,
        mock_client_class,
    ) -> None:
        mock_client = mock_client_class.return_value
        mock_response = (
            mock_client.models.generate_content.return_value
        )
        mock_response.text = "The document analysis should use evidence."

        answer = generate_answer(self.query, self.chunks)

        self.assertEqual(
            answer,
            "The document analysis should use evidence.",
        )
        mock_client_class.assert_called_once_with(
            api_key="fake-test-key"
        )
        mock_client.models.generate_content.assert_called_once()

    @patch("src.llm_client.genai.Client")
    def test_returns_message_when_no_chunks_are_found(
        self,
        mock_client_class,
    ) -> None:
        answer = generate_answer(self.query, [])

        self.assertIn("couldn't find relevant passages", answer)
        mock_client_class.assert_not_called()

    def test_rejects_non_string_query(self) -> None:
        with self.assertRaises(TypeError):
            generate_answer(123, self.chunks)

    def test_rejects_blank_query(self) -> None:
        with self.assertRaises(ValueError):
            generate_answer("   ", self.chunks)

    @patch("src.llm_client.genai.Client")
    @patch("src.llm_client.os.getenv", return_value=None)
    def test_reports_missing_api_key(
        self,
        mock_getenv,
        mock_client_class,
    ) -> None:
        with self.assertRaisesRegex(
            RuntimeError,
            "GEMINI_API_KEY is missing",
        ):
            generate_answer(self.query, self.chunks)

        mock_client_class.assert_not_called()

    @patch("src.llm_client.genai.Client")
    @patch("src.llm_client.os.getenv", return_value="fake-test-key")
    def test_rejects_empty_model_response(
        self,
        mock_getenv,
        mock_client_class,
    ) -> None:
        mock_client = mock_client_class.return_value
        mock_response = (
            mock_client.models.generate_content.return_value
        )
        mock_response.text = None

        with self.assertRaisesRegex(
            RuntimeError,
            "Gemini returned an empty response",
        ):
            generate_answer(self.query, self.chunks)

    
    @patch("src.llm_client.genai.Client")
    @patch("src.llm_client.os.getenv", return_value="fake-test-key")
    def test_summarizes_document(
        self,
        mock_getenv,
        mock_client_class,
    ) -> None:
        mock_client = mock_client_class.return_value
        mock_response = (
            mock_client.models.generate_content.return_value
        )
        mock_response.text = "The document explains AI research basics."

        summary = summarize_document(
            "Language models can summarize documents."
        )

        self.assertEqual(
            summary,
            "The document explains AI research basics.",
        )
        mock_client.models.generate_content.assert_called_once()

    def test_rejects_empty_document_for_summary(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            "Document text cannot be empty",
        ):
            summarize_document("   ")

    def test_rejects_non_string_document_for_summary(self) -> None:
        with self.assertRaises(TypeError):
            summarize_document(123)



if __name__ == "__main__":
    unittest.main()
