# src/nqueens/sa/solver.py
from __future__ import annotations
from typing import Optional, List
import time
import math
import numpy as np

from nqueens.common.state import conflicts
from .schedule import GeometricSchedule


def _random_state(n: int, rng: np.random.Generator) -> np.ndarray:
    """Generate an initial random assignment: one queen per row, random column."""
    return rng.integers(0, n, size=n, dtype=int)


def _propose_neighbor(state: np.ndarray, rng: np.random.Generator, use_swap_prob: float = 0.0) -> np.ndarray:
    """
    Generate a neighboring state by:
    - With probability (1 - use_swap_prob): change one queen's column randomly.
    - With probability use_swap_prob: swap two queens' columns.
    """
    n = len(state)
    neighbor = state.copy()
    if rng.random() < use_swap_prob:
        i, j = rng.choice(n, size=2, replace=False)
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
    else:
        i = rng.integers(0, n)
        new_col = rng.integers(0, n)
        while new_col == neighbor[i]:
            new_col = rng.integers(0, n)
        neighbor[i] = new_col
    return neighbor


def solve(
    n: int,
    time_limit: float = 5.0,
    seed: Optional[int] = None,
    T0: float = 1.0,
    alpha: float = 0.98,
    Tmin: float = 1e-3,
    max_steps: int = 50_000,
    iters_per_T: Optional[int] = None,
    use_swap_prob: float = 0.0,
) -> Optional[List[int]]:
    """
    Simulated Annealing solver for the N-Queens problem.
    Returns a list (assignment[row] = column) or None if no solution within time limit.

    Parameters
    ----------
    n : int
        Board size (number of queens).
    time_limit : float
        Max runtime in seconds.
    seed : int | None
        RNG seed for reproducibility.
    T0, alpha, Tmin : float
        Schedule parameters (initial temp, decay, minimum temp).
    max_steps : int
        Total number of iteration steps.
    iters_per_T : int
        How many neighbor trials per temperature level.
    use_swap_prob : float
        Probability of generating a swap neighbor instead of single-row change.
    """
    rng = np.random.default_rng(seed)
    start = time.perf_counter()

    # Initialize
    state = _random_state(n, rng)
    cost = conflicts(state)
    best_state, best_cost = state.copy(), cost
    schedule = GeometricSchedule(T0=T0, alpha=alpha, Tmin=Tmin)

    steps = 0
    while not schedule.done() and (time.perf_counter() - start < time_limit) and steps < max_steps:
        T = schedule.current()

        for _ in range(iters_per_T):
            neighbor = _propose_neighbor(state, rng, use_swap_prob)
            new_cost = conflicts(neighbor)
            delta = new_cost - cost

            # Metropolis acceptance
            if delta <= 0 or rng.random() < math.exp(-delta / T):
                state, cost = neighbor, new_cost
                if cost < best_cost:
                    best_state, best_cost = state.copy(), cost
                if cost == 0:
                    return list(state)

            steps += 1
            if (time.perf_counter() - start) > time_limit or steps >= max_steps:
                break

        schedule.step()

    # Return best found if perfect solution exists
    if best_cost == 0:
        return list(best_state)
    return None
