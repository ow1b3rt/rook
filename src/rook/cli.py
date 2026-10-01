from pathlib import Path

import typer
from rich import print

from rook.schemas import Evidence

app = typer.Typer(help="Rook — Find the signal. Collect and format market evidence.")


@app.command()
def init_db():
    """Create the initial PostgreSQL evidence table (development only)."""
    from rook.db import Base, get_engine

    Base.metadata.create_all(get_engine())
    print("[green]PostgreSQL evidence table ready.[/green]")


@app.command()
def normalize(source: Path, output: Path):
    """Validate a JSONL dataset and write consistently formatted JSONL."""
    records = []
    for number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                records.append(Evidence.model_validate_json(line))
            except ValueError as exc:
                raise typer.BadParameter(f"Invalid record on line {number}: {exc}") from exc
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("".join(r.model_dump_json() + "\n" for r in records), encoding="utf-8")
    print(f"Validated {len(records)} records → {output}")


@app.command()
def import_jsonl(source: Path):
    """Validate and insert records into PostgreSQL; skip duplicate source IDs."""
    from sqlalchemy.dialects.postgresql import insert

    from rook.db import Item, get_engine

    records = [
        Evidence.model_validate_json(line)
        for line in source.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    count = 0
    with get_engine().begin() as connection:
        for r in records:
            result = connection.execute(
                insert(Item)
                .values(
                    platform=r.platform,
                    external_id=r.external_id,
                    kind=r.kind,
                    url=str(r.url),
                    text_original=r.text_original,
                    collected_at=r.collected_at,
                    record=r.model_dump(mode="json"),
                )
                .on_conflict_do_nothing(index_elements=["platform", "external_id"])
            )
            count += result.rowcount
    print(f"Inserted {count}; skipped {len(records) - count} duplicates.")
