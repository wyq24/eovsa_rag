# Architecture

The project has four main stages: source collection, chunk processing, vector
database creation, and answer generation.

## Components

### Source Collection

`wiki_scraper.py` can collect wiki pages into Markdown files under
`data/raw/wiki`. Code and configuration snapshots can live under
`data/raw/code`. The full `data/raw` tree is intentionally ignored by git
because it may contain private operational documentation or conversation data.

### Chunk Processing

`enhanced_processor_complete.py` and `enhanced_processor_complete_all_kind.py`
convert raw documents into structured JSON chunks. The processor extracts
metadata such as titles, source type, commands, hardware references, summaries,
and cross-reference hints. AI enrichment can be disabled with `--no-ai`.

### Vector Store

`vector_database_creator.py` embeds processed chunks and writes:

- `data/vector_db/chroma`: Chroma persistent database files.
- `data/vector_db/chunk_metadata.json`: metadata keyed by chunk ID.
- `data/vector_db/database_stats.json`: summary counts for inspection.

These files are generated artifacts and are ignored by git.

### Retrieval And Generation

`llm_agent.py` loads `chunk_metadata.json`, connects to the Chroma collection,
creates an OpenAI embedding for each user query, retrieves relevant chunks, and
builds a grounded prompt for the chat model. The response includes formatted
sources, a confidence score, and safety-critical metadata when detected.

`streamlit_app_v_2.py` wraps the same agent with a chat UI, a model selector,
top-k display, source expansion, and conversation reset.

## Runtime Configuration

Runtime configuration is environment-driven:

- `OPENAI_API_KEY`: required for embeddings and chat completions.
- `OPENAI_MODEL`: optional model override.
- `MAX_RETRIEVED_DOCS`: optional default top-k retrieval limit.
- `CHROMA_COLLECTION`: optional UI collection default.
- `DB_PATH`: optional vector database base path.

Use `.env` locally and keep it out of git.
