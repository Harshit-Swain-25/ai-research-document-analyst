from pathlib import Path


def save_result(content: str, filename: str) -> Path:
    if not isinstance(content, str):
        raise TypeError("Content must be a string.")
    
    if not content.strip():
        raise ValueError("Content cannot be empty.")
    
    if not isinstance(filename, str):
        raise TypeError("Filename must be a string.")
    
    if not filename.strip():
        raise ValueError("Filename cannot be empty.")
    
    if Path(filename).name != filename or filename in {".", ".."}:
        raise ValueError("Filename must not contain a directory path.")

    if Path(filename).suffix.lower() != ".txt":
        raise ValueError("Filename must end with .txt.")

    project_root = Path(__file__).resolve().parent.parent
    output_directory = project_root / "outputs"
    output_directory.mkdir(parents=True, exist_ok=True)

    output_path = output_directory / filename
    output_path.write_text(content, encoding="utf-8")

    return output_path
