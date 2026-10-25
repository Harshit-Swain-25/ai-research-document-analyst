# AI Research / Document Analyst

A beginner-friendly Python project that explores document analysis using a large language model (LLM). It loads a text document, splits it into chunks, retrieves relevant passages, and uses Gemini to answer questions based on the supplied evidence.

The application can also generate a document summary and save analysis results as text files.

## Features

- **Text Document Loading:** Load a local `.txt` document.
- **Text Chunking:** Split document text into smaller, overlapping chunks.
- **Passage Retrieval:** Find relevant chunks for a user's question.
- **Evidence-Based Answers:** Generate answers using retrieved document passages.
- **Source Evidence:** Display the source document, chunk number, and passage used.
- **Document Summarization:** Generate a concise summary using Gemini.
- **Save Results:** Save summaries and question-answer reports in the `outputs/` directory.
- **Automated Tests:** Test core functionality with Python's `unittest` framework.

## Project Structure

```text
ai-research-document-analyst/
├── data/
│   └── sample_documents/
│       └── ai_research_basics.txt
├── outputs/
├── src/
│   ├── document_loader.py
│   ├── llm_client.py
│   ├── result_saver.py
│   ├── retriever.py
│   └── text_chunker.py
├── tests/
├── .env.example
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## Requirements

- Python 3.13 or a compatible Python version
- A Gemini API key
- An internet connection for Gemini requests

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Harshit-Swain-25/ai-research-document-analyst.git
cd ai-research-document-analyst
```

### 2. Create and activate a virtual environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure your API key

Create a local `.env` file based on the example:

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder with your Gemini API key:

```text
GEMINI_API_KEY=your_actual_api_key
```

**Never commit your `.env` file or publish your API key.**

## Run the application

```bash
python main.py
```

Choose an option from the menu:

1. Summarize the sample document.
2. Ask a question about the sample document.

Generated results are saved to:

- `outputs/document_summary.txt`
- `outputs/question_answer.txt`

The `outputs/` directory is excluded from Git, so generated reports remain local to your machine.

## Run tests

Run the full test suite:

```bash
python -m unittest discover -v
```

Check code style with Ruff:

```bash
ruff check .
```

## Current Scope and Limitations

- The current application analyzes a local plain-text sample document.
- Answers depend on the passages retrieved from that document.
- Gemini API access and usage may be subject to account quotas and pricing.
- Generated answers should be checked against their displayed source evidence.

## Future Improvements

- Add a simple user interface.
- Improve retrieval and evidence presentation where testing demonstrates a need.
- Support additional document formats when appropriate.

## Learning Purpose

This project is part of my hands-on learning journey in Generative AI and AI Engineering. It focuses on understanding the practical building blocks of a document analysis application: loading text, chunking, retrieval, LLM calls, evidence display, result saving, and automated testing.