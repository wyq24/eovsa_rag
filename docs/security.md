# Security

This project uses API keys and may process operational documentation. Treat both
configuration and source data carefully.

## Secrets

Do not commit:

- `.env` or `.env.*`
- OpenAI keys
- GitHub tokens
- Slack tokens or exports
- Streamlit secrets files
- Any private vendor or platform credentials

Use `.env.example` as the committed template and store real values only in a
local `.env`.

## Data

Generated retrieval artifacts are ignored by git:

- `data/raw`
- `data/processed`
- `data/vector_db`
- `data/processed_old`
- zip archives

If private or operational raw data is required for a local build, document where
to obtain it outside this repository.

## Pre-Commit Checks

Run these before committing or pushing:

```bash
git status --short
git diff --cached --name-only
rg -n "(s[k]-(proj-|live-|test-)?[A-Za-z0-9_-]{20,}|OPENAI[_]API[_]KEY[=][^[:space:]]+|ghp_[A-Za-z0-9]|github_pat_[A-Za-z0-9]|xox[baprs]-|AKIA[0-9A-Z])" .
```

If a real key was ever committed or shared, revoke and rotate it immediately.
