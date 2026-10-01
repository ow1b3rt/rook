# Rook

**Find the signal.** A local-first toolkit for collecting, organizing, and exploring Nepal market evidence.

## Scope

Phase one: discovery, collection, extraction, normalization, PostgreSQL storage, and exports.
No LLM or paid API is required for the starter.

This initial scaffold implements record validation, JSONL formatting, and PostgreSQL import.
Website, YouTube, TikTok, Instagram, Facebook, Reddit, session management, discovery,
job queues, raw artifact tracking, and migrations are planned; they are not implemented yet.

## Run locally

Install Python 3.12+, uv, and Docker Compose.

```bash
uv sync --extra dev
cp .env.example .env
docker compose up -d postgres
uv run rook --help
uv run rook init-db
uv run rook normalize input.jsonl exports/normalized.jsonl
uv run rook import-jsonl exports/normalized.jsonl
uv run pytest
```

The example database password is for local development. Update both Compose and
DATABASE_URL if changing it. PostgreSQL listens only on localhost.

## Planned collectors

- Websites: HTTPX, Trafilatura, BeautifulSoup.
- YouTube: yt-dlp.
- TikTok: TikTokApi, evaluated before adoption.
- Instagram: Instaloader, evaluated before adoption.
- Facebook and Reddit: bounded Playwright adapters for accessible content.
- Discovery: locally hosted SearXNG, feeds, sitemaps, and seed URLs.

Optional collector dependencies can be installed separately, for example
`uv sync --extra browser --extra youtube`. For browser installation run
`uv run playwright install chromium`.

## Data conventions

Keep original Unicode text, source URLs, parent IDs, collection times, and raw evidence.
Unknown values stay null. Do not infer Nepal residency solely from language.
Use `(platform, external_id)` for identity. Repeated metric observations will be
stored separately when collection history is implemented.

Sessions, cookies, raw data, exports, and .env are excluded from Git. Authenticate
locally through a visible browser; never commit account passwords or session files.
Collection must report partial results and access failures rather than claim completeness.

## Next milestones

1. Website and YouTube adapters with raw artifacts and completeness metadata.
2. PostgreSQL job queue, checkpoints, and Alembic migrations.
3. Source discovery and Nepal keyword configuration.
4. Independently benchmark each social connector.
