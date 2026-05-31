# Data Pipeline

This document describes the repeatable path from raw EOVSA source material to a
queryable Chroma vector database.

## 1. Collect Source Material

Place source material under `data/raw`:

- `data/raw/wiki`: Markdown pages scraped from the EOVSA wiki.
- `data/raw/code`: code and configuration snapshots used as retrieval context.
- `data/raw/slack`: optional private exports.

Review raw corpora before committing them. Do not include private exports or
credentials.

To scrape wiki pages interactively:

```bash
python wiki_scraper.py
```

Review scraped output before processing it.

## 2. Process Documents

Recommended processor:

```bash
python enhanced_processor_complete_all_kind.py \
  --input-dir data/raw \
  --output data/processed/enhanced_chunks.json
```

For a lower-cost local pass without AI enrichment:

```bash
python enhanced_processor_complete_all_kind.py \
  --input-dir data/raw \
  --output data/processed/enhanced_chunks.json \
  --no-ai
```

The output JSON can be large. Commit it only when the repository should ship
with a prebuilt processed corpus.

## 3. Build Embeddings

```bash
python vector_database_creator.py \
  --input data/processed/enhanced_chunks.json \
  --output-dir data/vector_db \
  --collection telescope_docs \
  --embedding-model openai
```

The embedding model defaults to OpenAI embeddings. The Chroma database is stored
under `data/vector_db`.

## 4. Validate Retrieval

Run the console smoke test:

```bash
python llm_agent.py
```

Then run the UI:

```bash
streamlit run streamlit_app_v_2.py -- \
  --collection telescope_docs \
  --db-path data/vector_db
```

Ask a few operational questions and confirm that returned sources have sensible
titles, summaries, and source types.

## Regeneration Checklist

When source material changes:

1. Refresh the raw files under `data/raw`.
2. Re-run the processor.
3. Rebuild the vector database.
4. Smoke-test `llm_agent.py`.
5. Test a few real questions in Streamlit.
6. Commit regenerated data only after checking that it contains no secrets.
