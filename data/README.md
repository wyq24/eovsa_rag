# Local Data

The data directories are intentionally untracked.

Use this layout for local builds:

- `data/raw`: raw wiki, code, and optional private source material.
- `data/processed`: processed chunk JSON files.
- `data/vector_db`: generated Chroma database and metadata.

Do not commit raw private corpora, generated vector databases, processed JSON,
zip archives, or API keys.
