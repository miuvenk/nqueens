# src/nqueens/experiments/run.py
from __future__ import annotations
from typing import Any, Dict, List, Callable, Optional
from pathlib import Path
import numpy as np
import time

from nqueens.common.io import write_rows_csv
from nqueens.common.state import conflicts
from nqueens.common.metrics import timer

# --- CSP solvers (two variants) ---
#from nqueens.csp.solver import solve_basic as csp_basic, solve_dynamic as csp_dynamic
from nqueens.csp.solver import solve_basic, solve_dynamic

# --- Optional: SA / GA (will be added later) ---
#from nqueens.sa.solver import solve as sa_solve  
#from nqueens.ga.solver import solve as ga_solve  


# Map method name -> callable(n, time_limit, seed) -> np.ndarray | None
SOLVERS: Dict[str, Callable[[int, float, Optional[int]], Optional[np.ndarray]]] = {
    "CSP_basic":   solve_basic,
    "CSP_dynamic": solve_dynamic,
}
#if sa_solve:
#    SOLVERS["SA"] = lambda n, tl, seed: sa_solve(n, time_limit=tl, seed=seed)  # type: ignore
#if ga_solve:
#    SOLVERS["GA"] = lambda n, tl, seed: ga_solve(n, time_limit=tl, seed=seed)  # type: ignore


def _project_root(start: Path) -> Path:
    """Find repo root by walking up to pyproject.toml (fallback: start's parent)."""
    p = start
    for _ in range(6):
        if (p / "pyproject.toml").exists():
            return p
        p = p.parent
    return start.parent


def run(
    ns: tuple[int, ...] = (8, 16, 32),
    repeats: int = 3,
    seed: Optional[int] = 42,
    time_limit_each: float = 5.0,
    methods: tuple[str, ...] = ("CSP_basic", "CSP_dynamic"),
    repeats_map: Optional[Dict[str, int]] = None,
    out_path: Optional[Path] = None,
) -> None:
    """
    Generic experiment runner.

    - ns: board sizes to test
    - repeats: default runs per method (stochastic methods can override via repeats_map)
    - seed: global seed to generate per-run seeds (stochastic solvers)
    - time_limit_each: seconds per single run
    - methods: which methods to execute (must be keys of SOLVERS)
    - repeats_map: per-method overrides, e.g., {"SA": 10, "GA": 10, "CSP_basic": 1}
    - out_path: optional custom CSV path
    """
    if repeats_map is None:
        repeats_map = {}

    # RNG to derive different seeds per run (stable across methods/sizes)
    rng = np.random.default_rng(seed)

    rows: List[Dict[str, Any]] = []

    # Validate methods upfront
    unknown = [m for m in methods if m not in SOLVERS]
    if unknown:
        raise ValueError(f"Unknown methods: {unknown}. Known: {list(SOLVERS.keys())}")

    for m in methods:
        solver = SOLVERS[m]
        runs_for_m = repeats_map.get(m, repeats)
        for n in ns:
            success = 0
            times: List[float] = []
            for _ in range(runs_for_m):
                # Per-run seed (stochastic solvers); CSP ignores it safely
                this_seed = None if seed is None else int(rng.integers(0, 2**31 - 1))
                with timer() as t:
                    sol = solver(n, time_limit_each, this_seed)
                dt = t()
                ok = (sol is not None) and (conflicts(sol) == 0)
                success += int(ok)
                times.append(dt)

            row = {
                "n": n,
                "method": m,
                "runs": runs_for_m,
                "success": success,
                "success_rate": (success / runs_for_m) if runs_for_m else 0.0,
                "avg_time_sec": (sum(times) / len(times)) if times else None,
            }
            print(row)
            rows.append(row)

    root = _project_root(Path(__file__).resolve())
    out = out_path or (root / "results" / "results.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    write_rows_csv(out, rows)
    print(f"\nSaved CSV -> {out}")


if __name__ == "__main__":
    # Example: CSP only
    run(
        ns=(8, 16, 32),
        repeats=3,
        seed=42,
        time_limit_each=5.0,
        methods=("CSP_basic", "CSP_dynamic"),
        # When add SA/GA,
        # methods=("CSP_basic", "CSP_dynamic", "SA", "GA"),
        # repeats_map={"SA": 10, "GA": 10, "CSP_basic": 1, "CSP_dynamic": 1},
    )
