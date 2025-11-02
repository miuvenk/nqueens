from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List
import sys

# --- imports from our package ---
from nqueens.common.io import write_rows_csv
from nqueens.common.metrics import timer
from nqueens.common.state import conflicts
from nqueens.csp.solver import solve as csp_solve
# SA/GA can be added later when ready:
# from nqueens.sa.solver  import solve as sa_solve
# from nqueens.ga.solver  import solve as ga_solve

def run(ns=(8, 16, 32), repeats=3, seed=42, time_limit_each=5.0, methods=("CSP",)):  # start with CSP only
    rows: List[Dict[str, Any]] = []
    for n in ns:
        for m in methods:
            runs = (repeats if m != "CSP" else 1)
            success, times = 0, []
            for _ in range(runs):
                with timer() as t:
                    if m == "CSP":
                        sol = csp_solve(n, time_limit=time_limit_each)
                    else:
                        raise ValueError(f"Unknown method: {m}")
                dt = t()
                ok = (sol is not None) and (conflicts(sol) == 0)
                success += int(ok)
                times.append(dt)
            row = {
                "n": n,
                "method": m,
                "runs": runs,
                "success": success,
                "success_rate": success / runs if runs else 0.0,
                "avg_time_sec": sum(times)/len(times) if times else None,
            }
            print(row)  # ensure something is printed
            rows.append(row)

    out = Path(__file__).resolve().parents[3] / "results" / "results_csp.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    write_rows_csv(out, rows)
    print(f"\nSaved CSV -> {out}")

if __name__ == "__main__":
    # Make sure run() executes when invoked as a module
    run()