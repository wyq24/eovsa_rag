# EOVSA RAG Agent

This repository contains a retrieval-augmented generation (RAG) assistant for
EOVSA operations, procedures, and source-code documentation. It processes EOVSA
wiki pages and code snapshots into searchable chunks, stores embeddings in a
local Chroma database, and serves answers through a console smoke test or a
Streamlit chat UI.

## What Is Included

- `llm_agent.py`: core retriever and LLM agent.
- `streamlit_app_v_2.py`: Streamlit chat interface.
- `enhanced_processor_complete.py`: document processor for wiki/code inputs.
- `enhanced_processor_complete_all_kind.py`: multi-language processor variant.
- `vector_database_creator.py`: Chroma vector database builder.
- `wiki_scraper.py`: helper for collecting wiki pages.
- `data`: local source corpora and generated retrieval artifacts. These files
  are intentionally ignored by git because they may contain private operational
  documentation or large generated data.

Generated files are intentionally not committed, including `.env`,
`data/raw`, `data/processed`, `data/vector_db`, zip archives, caches, and IDE
metadata.

## Requirements

- Python 3.10 or newer
- An OpenAI API key available as `OPENAI_API_KEY`
- Local disk space for generated processed chunks and Chroma data

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create local configuration:

```bash
cp .env.example .env
```

Then edit `.env` and set `OPENAI_API_KEY`. Never commit real keys.

## Build The Knowledge Base

Process the raw corpus into chunks:

```bash
python enhanced_processor_complete_all_kind.py \
  --input-dir data/raw \
  --output data/processed/enhanced_chunks.json
```

Build the Chroma vector store:

```bash
python vector_database_creator.py \
  --input data/processed/enhanced_chunks.json \
  --output-dir data/vector_db \
  --collection telescope_docs
```

The generated Chroma files and processed JSON stay local by default.

## Run

Console smoke test:

```bash
python llm_agent.py
```

Streamlit UI:

```bash
streamlit run streamlit_app_v_2.py -- \
  --collection telescope_docs \
  --db-path data/vector_db
```

Useful optional environment variables:

- `OPENAI_MODEL`: chat model used by the agent, default `gpt-5`.
- `MAX_RETRIEVED_DOCS`: number of chunks retrieved per query, default `15`.
- `CHROMA_COLLECTION`: default collection used by the UI.
- `DB_PATH`: base path containing `chunk_metadata.json` and `chroma`.

## Repository Hygiene

Before committing, check that no keys or generated artifacts are staged:

```bash
git status --short
git diff --cached --name-only
rg -n "(s[k]-(proj-|live-|test-)?[A-Za-z0-9_-]{20,}|OPENAI[_]API[_]KEY[=][^[:space:]]+|ghp_[A-Za-z0-9]|github_pat_[A-Za-z0-9]|xox[baprs]-|AKIA[0-9A-Z])" .
```

The `.gitignore` excludes local secrets, vector database files, processed data,
zip archives, caches, and Slack exports.

## More Documentation

- [Architecture](docs/architecture.md)
- [Data Pipeline](docs/data-pipeline.md)
- [Security](docs/security.md)
