from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Any, Union
import csv

PathLike = Union[str, Path]

def ensure_dir(path: PathLike) -> Path:
    """
    Ensure the given directory (and its parents) exists.
    Returns the created Path object.
    """
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def write_rows_csv(path: PathLike, rows: List[Dict[str, Any]]) -> None:
    """
    Write a list of dictionaries to a CSV file.
    Column headers are inferred from rows[0].keys().
    """
    if not rows:
        return
    p = Path(path)
    ensure_dir(p.parent)
    with p.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def append_row_csv(path: PathLike, row: Dict[str, Any]) -> None:
    """
    Append a single row to an existing CSV file, creating it if necessary.
    """
    p = Path(path)
    ensure_dir(p.parent)
    file_exists = p.exists()
    with p.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def read_rows_csv(path: PathLike) -> List[Dict[str, str]]:
    """
    Read a CSV file into a list of dictionaries (all values as strings).
    """
    p = Path(path)
    if not p.exists():
        return []
    with p.open("r", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)