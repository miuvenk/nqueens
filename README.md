# ♟️ N-Queens Solver — CSP, Simulated Annealing & Genetic Algorithm

> A comparative AI project exploring different problem-solving paradigms — **CSP**, **Simulated Annealing**, and **Genetic Algorithm** — for the classic **N-Queens** puzzle.

## 🧠 Overview
This project solves the **N-Queens problem**, which asks for placing N queens on an N×N chessboard so that no two queens attack each other.  
The goal is to **implement and compare different Artificial Intelligence paradigms** to explore their strengths and limitations in constraint satisfaction and optimization problems.


### Implemented & Planned Methods

| Approach                                  | Description                                                                                    | Status          |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------- | --------------- |
| **CSP (Constraint Satisfaction Problem)** | Systematic search using Backtracking, Constraint Propagation, MRV & LCV heuristics             | ✅ Implemented   |
| **Simulated Annealing (SA)**              | Local search with probabilistic acceptance (geometric cooling schedule)                        | 🛠️ In Progress |
| **Genetic Algorithm (GA)**                | Population-based evolutionary search with crossover & mutation                                 | 🛠️ In Progress |
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

## 🚀 Run Experiments

```bash
python -m nqueens.experiments.run
```

By default, the script runs the CSP solver for `n = 8, 16, 32`  
and saves results to **`results/results.csv`**.

You can edit **`src/nqueens/experiments/run.py`** to customize experiments:

- Add or remove methods in  
  ```python
  methods = ("CSP", "SA", "GA")
  ```

- Change board sizes
  ```python
  ns = (8, 16, 32, 64)
  ```

- Adjust runtime limits or repeat counts
   ```python
   time_limit_each = 5.0
   repeats = 3
   ```

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
            └── run.py            # main entry point (python -m nqueens.experiments.run)
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

