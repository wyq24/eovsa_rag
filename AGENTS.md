# Repository Guidelines

## Project Structure & Module Organization
- Core agent logic lives in `llm_agent.py` (EnhancedTelescopeLLMAgent + Chroma retriever) and reads vector data from `data/vector_db/chroma` with `chunk_metadata.json`.
- `streamlit_app_v_2.py` provides the Streamlit UI for queries; run it locally for demos.
- Data prep: raw inputs in `data/raw/{code,slack,wiki}` flow through `enhanced_processor_complete*.py` into `data/processed/enhanced_chunks.json`, and `vector_database_creator.py` turns that JSON into a Chroma collection.
- Utilities such as `wiki_scraper.py` and `enhanced_processor_complete_all_kind.py` expand coverage of documentation sources; keep outputs in `data/processed` and archive large artifacts (`processed_0805.zip`, `vector_db_no_eovsa.zip`) outside version control.

## Build, Test, and Development Commands
- Create a virtual environment and install deps: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.
- Build or refresh the vector store (requires `OPENAI_API_KEY` and processed chunks): `python vector_database_creator.py --input data/processed/enhanced_chunks.json --output-dir data/vector_db --collection eovsa`.
- Launch the UI: `streamlit run streamlit_app_v_2.py -- --collection eovsa` (use `--chroma-path` if you place the DB elsewhere).
- Console smoke test against the current DB: `python llm_agent.py` (runs canned queries and prints sources/confidence).

## Coding Style & Naming Conventions
- Python 3.10+; follow PEP 8 with 4-space indents, snake_case for functions/variables, and PascalCase for classes.
- Keep type hints and docstrings aligned with existing patterns; prefer `logging` over prints except for explicit CLI progress.
- Guard optional dependencies (ChromaDB, OpenAI, streamlit) as done in current modules, and keep configuration through environment variables rather than hard-coding paths or keys.

## Testing Guidelines
- No automated tests exist; validate changes by rebuilding the vector DB (if data/schema changed) and running `python llm_agent.py` plus a couple of real queries through Streamlit.
- When modifying retrieval or embedding logic, confirm the regenerated `chunk_metadata.json` matches expectations and that top-k results still return sensible source titles/summaries.

## Commit & Pull Request Guidelines
- If using git, keep commit messages short and imperative (e.g., `feat: update retriever scoring`, `chore: refresh vector db`) and group data regenerations in their own commits when possible.
- PRs should describe the intent, list regeneration steps (scrape, process, create DB), note any required secrets (`OPENAI_API_KEY`), and include screenshots of UI changes or sample Q&A outputs for verification.

## Security & Configuration Tips
- Never commit API keys; load them via `.env` and `load_dotenv()`.
- Large artifacts and raw data can grow quickly—store interim zips outside source control and document any external paths used for private datasets.
