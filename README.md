# ♟️ N-Queens Solver — CSP, Simulated Annealing & Genetic Algorithm

> A comparative AI project exploring different problem-solving paradigms — **CSP-Basic**, **CSP_Dynamic**, **Simulated Annealing**, and **Genetic Algorithm** — for the classic **N-Queens** puzzle.

## 🧠 Overview
This project solves the **N-Queens problem**, which asks for placing N queens on an N×N chessboard so that no two queens attack each other.  
The goal is to **implement and compare different Artificial Intelligence paradigms** to explore their strengths and limitations in constraint satisfaction and optimization problems.


### Implemented & Planned Methods

| Approach                                  | Description                                                                                    | Status          |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------- | --------------- |
| **CSP-Basic**                             | Backtracking + Forward Checking (fixed variable/value ordering)                                | ✅ Implemented   |
| **CSP-Dynamic**                           | Backtracking + Forward Checking + MRV + LCV heuristics                                         | ✅ Implemented   |
| **Simulated Annealing (SA)**              | Local search with probabilistic acceptance (geometric cooling schedule)                        | ✅ Implemented  |
| **Genetic Algorithm (GA)**                | Population-based evolutionary search with crossover & mutation                                 | ✅ Implemented  |
| **Projected Gradient (Relaxed Problem)**  | Continuous relaxation of the N-Queens constraint problem solved via projected gradient descent | 🚧 Planned      |


Each method is evaluated in terms of:
- **Success rate** (fraction of solved instances)
- **Average runtime** (seconds)
- **Scalability** as N increases (e.g. N = 8, 16, 32, 64, ...)

---

## ⚙️ Installation

```bash
# 1. Clone the repository
git clone https://github.com/miuvenk/nqueens.git
cd nqueens

# 2. (optional) Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies (editable mode)
pip install -e .
````

## Requirements:
  - Python ≥ 3.9
  - NumPy ≥ 2.0.0
  - (Optional) Matplotlib ≥ 3.0 (only for plotting results)

**NOTE:** If you want to generate result plots:
```bash
pip install matplotlib
```

⚠️ Matplotlib is used only for visualization.
It is not used inside CSP, SA, or GA solvers.

## 🚀 Run Experiments

```bash
python -m nqueens.experiments.run
```

By default, the script runs the CSP solver for `n = 8, 16, 32, 64`  
and saves results to **`results/results.csv`**.

You can edit **`src/nqueens/experiments/run.py`** to customize experiments:

- Add or remove methods in  
  ```python
  methods = ("CSP-basic", "CSP-dynamic "SA", "GA")
  ```

- Change board sizes
  ```python
  ns = (8, 16, 32, 64)
  ```

- Adjust runtime limits or repeat counts
   ```python
   time_limit_each = 5.0
   repeats = 3
   repeats_map = {"SA": 10, "GA": 10, "CSP_basic": 1, "CSP_dynamic": 1}
   ```
## 🔧 Tuning SA & GA Parameters

The hyper-parameters for Simulated Annealing and Genetic Algorithm are configured in
src/nqueens/experiments/run.py, inside the SOLVERS dictionary:
```bash
# Map method name -> callable(n, time_limit, seed) -> np.ndarray | None
SOLVERS: Dict[str, Callable[[int, float, Optional[int]], Optional[np.ndarray]]] = {
    "CSP_basic":   solve_basic,
    "CSP_dynamic": solve_dynamic,

    # Balanced Simulated Annealing configuration
    "SA": lambda n, tl, seed: sa_solve(
        n,
        time_limit=tl,
        seed=seed,
        T0=4.0,          # initial temperature
        alpha=0.993,     # cooling rate
        Tmin=5e-4,       # minimum temperature
        iters_per_T=max(10, n),
        max_steps=120_000,
        use_swap_prob=0.15,
    ),

    # Balanced Genetic Algorithm configuration
    "GA": lambda n, tl, seed: ga_solve(
        n,
        time_limit=tl,
        seed=seed,
        pop_size=100,
        cx_prob=0.8,
        mut_prob=0.05,
        max_generations=2000,
        tournament_size=5,
        elitism=True,
    ),
}
```

You can modify these values to study how different parameter settings affect:
  -convergence speed,
  -success rate,
  -and scalability for larger N.

This allows you to reproduce the experiments in the report and also explore alternative SA/GA behaviors under the same unified experiment runner.

## 📊 Generate Plots

To visualize runtimes and success rates:
```bash
python -m nqueens.experiments.plot_results
```
This creates figures under:

results/plots/
    ├── csp_internal_runtime.png
    ├── all_methods_runtime_log.png
    └── success_rate.png

## 📁 Project Structure

```bash
nqueens/
├── pyproject.toml                # project configuration (editable install)
├── README.md                     # documentation
├── results/                      # experiment outputs
│   └── results.csv
└── src/
    └── nqueens/
        ├── __init__.py
        ├── common/               # shared utilities
        │   ├── state.py          # conflict checker, board visualization
        │   ├── metrics.py        # timing utilities
        │   └── io.py             # CSV I/O helpers
        ├── csp/                  # constraint satisfaction approach
        │   ├── heuristics.py     # MRV, LCV heuristics
        │   └── solver.py         # backtracking + forward checking
        ├── sa/                   # simulated annealing approach
        │   └── solver.py         # probabilistic local search
        ├── ga/                   # genetic algorithm approach
        │   └── solver.py         # population evolution
        └── experiments/          # experiment driver
            ├── run.py            # main entry point (python -m nqueens.experiments.run)
            └── plot_results.py   # result visualization (python -m nqueens.experiments.plot_results)
```

## 📈 Experimental Setup

Each algorithm is executed on various board sizes (n = 8, 16, 32, 64)
for multiple repetitions per configuration.
Metrics logged for each run:

 - n — board size
 - method — algorithm name
 - success_rate — proportion of runs solved
 - avg_time_sec — average runtime per run

All results are automatically exported to results/results.csv.

## 🧠 Theoretical Notes

- CSP ensures completeness (always finds a solution if time allows)
but may become slow for large N.
- Simulated Annealing uses randomness to escape local minima.
- Genetic Algorithm explores globally via population diversity.
- Comparing their trade-offs helps understand systematic vs stochastic search.

## 👩‍💻 Author
**Esma Nur Kocakaya**  
*MSc Computer Science and Information Technology — Ca’ Foscari University of Venice*

