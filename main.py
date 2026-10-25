from pathlib import Path

from google.genai.errors import APIError

from src.document_loader import load_text_document
from src.llm_client import generate_answer, summarize_document
from src.result_saver import save_result
from src.retriever import retrieve_relevant_chunks
from src.text_chunker import create_chunk_records


def answer_question(
    text: str,
    document_path: Path,
    chunk_records: list[dict[str, str | int]],
) -> None:
    query = input("\nAsk a question about the document: ").strip()

    if not query:
        print("\nPlease enter a question.")
        return

    results = retrieve_relevant_chunks(
        query=query,
        chunk_records=chunk_records,
        top_k=3,
    )

    if not results:
        print("\nNo matching passages found.")
        print("I cannot answer this question from the retrieved document evidence.")
        return

    print(f"\nRetrieved {len(results)} relevant passage(s).")
    print("\nGenerating an evidence-based answer...")

    try:
        answer = generate_answer(
            query=query,
            retrieved_chunks=results,
        )
    except APIError:
        print("\nSorry, Gemini could not process your request. "
            "Check your API key, quota, network connection, "
            "or model availability and try again.")
        return
    except RuntimeError as error:
        print(f"\nConfiguration or response error: {error}")
        return

    print("\nAnswer:")
    print(answer)

    print("\n" + "-" * 35)
    print("Source Evidence")
    print("-" * 35)

    saved_content = [
        f"Question: {query}",
        "",
        "Answer:",
        answer,
        "",
        "Source Evidence",
        "=" * 35,
    ]

    for index, chunk in enumerate(results, start=1):
        print(f"\nEvidence: {index}")
        print(f"Source: {chunk['source']}")
        print(f"Chunk: {chunk['chunk_index']}")
        print("Passage:")
        print(chunk["text"])

        saved_content.extend(
            [
                "",
                f"Evidence: {index}",
                f"Source: {chunk['source']}",
                f"Chunk: {chunk['chunk_index']}",
                "Passage:",
                chunk["text"],
            ]
        )

    try:
        saved_path = save_result(
            content="\n".join(saved_content),
            filename="question_answer.txt",
        )
    except (OSError, ValueError) as error:
        print(f"\nCould not save the answer: {error}")
        return

    print(f"\nQuestion and answer saved to: {saved_path}")


def summarize_loaded_document(text: str) -> None:
    print("\nGenerating a document summary...")

    try:
        summary = summarize_document(text)
    except APIError:
        print("\nSorry, Gemini could not process your request. "
            "Check your API key, quota, network connection, "
            "or model availability and try again.")
        return
    except RuntimeError as error:
        print(f"\nConfiguration or response error: {error}")
        return

    print("\nDocument Summary")
    print("-" * 35)
    print(summary)

    try:
        saved_path = save_result(
            content=summary,
            filename="document_summary.txt",
        )
    except (OSError, ValueError) as error:
        print(f"\nCould not save the summary: {error}")
        return

    print(f"\nSummary saved to: {saved_path}")


def main() -> None:
    document_path = Path("data/sample_documents/ai_research_basics.txt")

    try:
        text = load_text_document(str(document_path))
    except (OSError, ValueError) as error:
        print(f"\nCould not load the document: {error}")
        return
     
    chunk_records = create_chunk_records(
        text=text,
        source=document_path.name,
    )

    print("AI Research / Document Analyst")
    print("-" * 35)
    print(f"Document: {document_path}")
    print(f"Document characters: {len(text)}")
    print(f"Number of chunks: {len(chunk_records)}")

    choice = input("\nEnter your choice (1 or 2): ")

    if choice == "1":
        summarize_loaded_document(text)
    elif choice == "2":
        answer_question(text, document_path, chunk_records)
    else:
        print("\nInvalid choice. Please run the program and select 1 or 2.")

if __name__ == "__main__":
    main()