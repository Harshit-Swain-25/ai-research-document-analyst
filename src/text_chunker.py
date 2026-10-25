def split_text(
        text: str,
        chunk_size: int = 500,
        overlap: int = 50
) -> list[str]:
    if not isinstance(text, str):
        raise TypeError("Text must be a string")
    
    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero.")
    
    if overlap < 0:
        raise ValueError("Overlap cannot be negative.")
    
    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk size.")
    
    if not text:
        return []
    
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])

        if end >= len(text):
            break

        start = end - overlap

    return chunks

def create_chunk_records(
        text: str,
        source: str,
        chunk_size: int = 500,
        overlap: int = 50
) -> list[dict[str, str | int]]:
    chunks = split_text(
        text,
        chunk_size=chunk_size,
        overlap=overlap,
    )

    records = []

    for index, chunk in enumerate(chunks, start=1):
        records.append(
            {
                "text": chunk,
                "source": source,
                "chunk_index": index,
            }
        )

    return records