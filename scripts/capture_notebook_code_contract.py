"""Capture exact executable-cell hashes for a released Jupyter notebook."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected an object in {path}")
    return value


def source_text(cell: dict[str, Any]) -> str:
    source = cell.get("source", "")
    if isinstance(source, list):
        return "".join(source)
    if isinstance(source, str):
        return source
    raise ValueError("Notebook cell source must be a string or list of strings.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--notebook", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-release", default="v1.0.0")
    parser.add_argument("--purpose", required=True)
    args = parser.parse_args()

    notebook = load_json(args.notebook)
    cells = []
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        cell_id = cell.get("id")
        if not isinstance(cell_id, str) or not cell_id:
            raise ValueError("Every executable cell must have a stable non-empty id.")
        text = source_text(cell)
        cells.append(
            {
                "id": cell_id,
                "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                "lines": len(text.splitlines()),
            }
        )

    if not cells:
        raise ValueError(f"No executable cells found in {args.notebook}")

    contract = {
        "schema_version": 1,
        "source_release": args.source_release,
        "notebook": args.notebook.as_posix(),
        "purpose": args.purpose,
        "code_cells": cells,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(contract, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": "CAPTURED",
                "notebook": args.notebook.as_posix(),
                "code_cells": len(cells),
                "output": args.output.as_posix(),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
