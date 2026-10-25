
import re

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by",
    "can", "do", "does", "for", "from", "how", "in",
    "is", "it", "of", "on", "or", "should", "that",
    "the", "their", "this", "to", "was", "what", "when",
    "where", "which", "who", "why", "with",
}


def extract_keywords(text: str) -> set[str]:
    words = set(re.findall(r"\b[a-zA-Z0-9]+\b", text.lower()))
    return words - STOP_WORDS


def retrieve_relevant_chunks(
    query: str,
    chunk_records: list[dict[str, str | int]],
    top_k: int = 3,
) -> list[dict[str, str | int]]:
    if not isinstance(query, str):
        raise TypeError("Query must be a string.")

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero.")

    query_words = extract_keywords(query)

    if not query_words:
        return []

    scored_chunks = []

    for record in chunk_records:
        chunk_text = record["text"]

        if not isinstance(chunk_text, str):
            raise TypeError("Each chunk's text must be a string.")

        chunk_words = extract_keywords(chunk_text)
        score = len(query_words & chunk_words)

        if score > 0:
            scored_chunks.append((score, record))

    scored_chunks.sort(key=lambda item: item[0], reverse=True)

    return [
        record
        for score, record in scored_chunks[:top_k]
    ]
