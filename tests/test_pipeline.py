
import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

import main


class TestDocumentAnalysisPipeline(unittest.TestCase):
    @patch("main.generate_answer", return_value="Mock evidence-based answer.")
    @patch(
        "builtins.input",
        side_effect=[
            "2",
            (
                "What should a document analysis system do "
                "if the supplied documents do not contain enough information?"
            ),
        ],
    )
    def test_answerable_question_uses_retrieved_evidence(
        self,
        mock_input,
        mock_generate_answer,
    ) -> None:
        output = StringIO()

        with redirect_stdout(output):
            main.main()

        displayed_output = output.getvalue()

        self.assertIn("Retrieved", displayed_output)
        self.assertIn("Answer:", displayed_output)
        self.assertIn("Mock evidence-based answer.", displayed_output)

        mock_generate_answer.assert_called_once()

        call_arguments = mock_generate_answer.call_args.kwargs

        self.assertEqual(
            call_arguments["query"],
            ("What should a document analysis system do if the supplied documents do not contain enough information?"),
        )
        self.assertGreater(
            len(call_arguments["retrieved_chunks"]),
            0,
        )

    @patch("main.generate_answer")
    @patch("builtins.input",
        side_effect=["2", "What is the capital of Japan?"],
    )
    def test_unanswerable_question_skips_gemini(
        self,
        mock_input,
        mock_generate_answer,
    ) -> None:
        output = StringIO()

        with redirect_stdout(output):
            main.main()

        displayed_output = output.getvalue()

        self.assertIn("No matching passages found.", displayed_output)
        mock_generate_answer.assert_not_called()

    @patch(
        "main.generate_answer",
        side_effect=main.APIError(
            503,
            {"error": {"message": "Service temporarily unavailable"}},
        ),
    )
    @patch(
        "builtins.input",
        side_effect=[
            "2",
            (
                "What should a document analysis system do "
                "if the supplied documents do not contain enough information?"
            ),
        ],
    )
    def test_gemini_api_error_is_handled_gracefully(
        self,
        mock_input,
        mock_generate_answer,
    ) -> None:
        output = StringIO()

        with redirect_stdout(output):
            main.main()

        displayed_output = output.getvalue()

        self.assertIn(
            "Gemini could not process your request",
            displayed_output,
        )
        self.assertNotIn(
            "Traceback (most recent call last)",
            displayed_output,
        )

        mock_generate_answer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
