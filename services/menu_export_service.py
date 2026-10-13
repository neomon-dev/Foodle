import csv
import json
from pathlib import Path
from typing import Any, Iterable, List


def export_menu_records(records: Iterable[dict], export_format: str, output_path: str | None = None):
    rows = list(records)
    if not rows:
        raise ValueError("There are no records to export.")

    export_format = (export_format or "json").lower()
    if output_path is None:
        output_path = f"foodle_export.{export_format}"

    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)

    if export_format == "json":
        target.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    elif export_format == "csv":
        fieldnames = list(rows[0].keys())
        with target.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    else:
        raise ValueError("Unsupported export format. Use 'csv' or 'json'.")

    return str(target)
