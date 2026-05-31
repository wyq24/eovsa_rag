# Data

This repository can include the current raw corpus, processed chunks, and Chroma
vector database for reproducible local demos.

Use this layout for local builds:

- `data/raw`: raw wiki, code, and optional private source material.
- `data/processed`: processed chunk JSON files.
- `data/vector_db`: generated Chroma database and metadata.

Do not commit raw private corpora, root-level zip archives, API keys, or any
other credentials.
