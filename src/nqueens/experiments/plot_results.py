# src/nqueens/experiments/plot_results.py
from __future__ import annotations
import csv
from pathlib import Path
from typing import List, Dict, Any
import math

import matplotlib.pyplot as plt


def _project_root(start: Path) -> Path:
    """
    Find repo root by walking up until we see pyproject.toml.
    Fallback: parent of src.
    """
    p = start
    for _ in range(6):
        if (p / "pyproject.toml").exists():
            return p
        p = p.parent
    return start.parent


def load_results(csv_path: Path) -> List[Dict[str, Any]]:
    """Load results/results.csv into a list of dicts with proper types."""
    rows: List[Dict[str, Any]] = []
    with csv_path.open(newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                row: Dict[str, Any] = {
                    "n": int(r["n"]),
                    "method": r["method"],
                    "runs": int(r["runs"]),
                    "success": int(r["success"]),
                    "success_rate": float(r["success_rate"]),
                    "avg_time_sec": float(r["avg_time_sec"]) if r["avg_time_sec"] else math.nan,
                }
                rows.append(row)
            except (KeyError, ValueError) as e:
                print(f"Skipping row due to parse error: {r} ({e})")
    return rows


def plot_csp_internal(rows: List[Dict[str, Any]], out_dir: Path) -> None:
    """
    Plot CSP_basic vs CSP_dynamic: avg_time_sec vs n.
    """
    methods = ["CSP_basic", "CSP_dynamic"]
    data = {m: {} for m in methods}

    for r in rows:
        m = r["method"]
        if m in methods:
            data[m][r["n"]] = r["avg_time_sec"]

    plt.figure()
    for m in methods:
        ns = sorted(data[m].keys())
        ys = [data[m][n] for n in ns]
        plt.plot(ns, ys, marker="o", label=m)

    plt.xlabel("Board size N")
    plt.ylabel("Average runtime (s)")
    plt.title("CSP Basic vs CSP Dynamic – Runtime vs N")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    out_path = out_dir / "csp_internal_runtime.png"
    plt.savefig(out_path, bbox_inches="tight", dpi=200)
    plt.close()
    print(f"Saved CSP internal plot -> {out_path}")


def plot_all_runtime(rows: List[Dict[str, Any]], out_dir: Path) -> None:
    """
    Plot all methods: avg_time_sec vs n (log-scale y-axis).
    """
    methods = sorted({r["method"] for r in rows})
    data: Dict[str, Dict[int, float]] = {m: {} for m in methods}

    for r in rows:
        m = r["method"]
        data[m][r["n"]] = r["avg_time_sec"]

    plt.figure()
    for m in methods:
        ns = sorted(data[m].keys())
        ys = [data[m][n] for n in ns]
        plt.plot(ns, ys, marker="o", label=m)

    plt.xlabel("Board size N")
    plt.ylabel("Average runtime (s, log-scale)")
    plt.yscale("log")
    plt.title("All Methods – Runtime vs N (log scale)")
    plt.grid(True, linestyle="--", alpha=0.5, which="both")
    plt.legend()
    out_path = out_dir / "all_methods_runtime_log.png"
    plt.savefig(out_path, bbox_inches="tight", dpi=200)
    plt.close()
    print(f"Saved all-methods runtime plot -> {out_path}")


def plot_success_rate(rows: List[Dict[str, Any]], out_dir: Path) -> None:
    """
    Plot success_rate vs n for all methods.
    """
    methods = sorted({r["method"] for r in rows})
    data: Dict[str, Dict[int, float]] = {m: {} for m in methods}

    for r in rows:
        m = r["method"]
        data[m][r["n"]] = r["success_rate"]

    plt.figure()
    for m in methods:
        ns = sorted(data[m].keys())
        ys = [data[m][n] for n in ns]
        plt.plot(ns, ys, marker="o", label=m)

    plt.xlabel("Board size N")
    plt.ylabel("Success rate")
    plt.ylim(-0.05, 1.05)
    plt.title("Success Rate vs N")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    out_path = out_dir / "success_rate.png"
    plt.savefig(out_path, bbox_inches="tight", dpi=200)
    plt.close()
    print(f"Saved success-rate plot -> {out_path}")


def main() -> None:
    here = Path(__file__).resolve()
    root = _project_root(here)
    csv_path = root / "results" / "results.csv"
    if not csv_path.exists():
        raise SystemExit(f"CSV not found: {csv_path}")

    rows = load_results(csv_path)
    if not rows:
        raise SystemExit("No rows loaded from CSV; nothing to plot.")

    plots_dir = root / "results" / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    plot_csp_internal(rows, plots_dir)
    plot_all_runtime(rows, plots_dir)
    plot_success_rate(rows, plots_dir)


if __name__ == "__main__":
    main()
