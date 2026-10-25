from pathlib import Path


def load_text_document(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")
    
    if not path.is_file():
        raise ValueError(f"The path is not a file: {path}")
    
    if path.suffix.lower() != ".txt":
        raise ValueError("Unsupported file type. Please provide .txt file.")
    
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(f"Could not read the document as UTF-8 text: {path}") from error
    
