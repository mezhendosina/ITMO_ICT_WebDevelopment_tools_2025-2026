# Lab 2 — threading, multiprocessing, asyncio

Run all commands from this directory (`Lr2`).

## Task 1 — sum 1..N (chunked closed form)

```bash
python3 task1_sum_threading.py -w 8
python3 task1_sum_multiprocessing.py -w 4
python3 task1_sum_asyncio.py -w 8
```

Options: `-n/--upper` (default `10000000000000`), `-w/--workers`.

## Task 2 — parse titles into Lab 1 database

1. Configure `../Lr1/.env` with `DATABASE_URL`, apply migrations from `../Lr1`:
  ```bash
   cd ../Lr1 && alembic upgrade head && cd ../Lr2
  ```
2. Install Lab 1 dependencies (includes `requests`, `beautifulsoup4`, `aiohttp`).

```bash
python3 task2_parse_threading.py -w 4
python3 task2_parse_multiprocessing.py -w 4
python3 task2_parse_asyncio.py -w 4
```

## MkDocs

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install mkdocs
mkdocs build
```

Open `site/index.html` or run `mkdocs serve`.

Full report: [docs/index.md](docs/index.md).