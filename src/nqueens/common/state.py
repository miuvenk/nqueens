from __future__ import annotations
from typing import List, Sequence, Optional, Union
import numpy as np

ArrayLike = Union[Sequence[int], np.ndarray]

def conflicts(state: ArrayLike) -> int:
    """
    Return the total number of attacking queen pairs (same column or diagonal).
    state[r] = column index (0..n-1) of the queen in row r.
    Note: a valid solution has 0 conflicts.
    """
    s = np.asarray(state, dtype=int)
    n = int(s.shape[0])

    rows = np.arange(n, dtype=int)
    col = s
    d1 = rows - col          # main diagonal index
    d2 = rows + col          # anti-diagonal index

    def count_pairs(v: np.ndarray) -> int:
        # number of pairs with identical value: sum over k of C(count_k, 2)
        _, cnt = np.unique(v, return_counts=True)
        return int(np.sum(cnt * (cnt - 1) // 2))

    return count_pairs(col) + count_pairs(d1) + count_pairs(d2)


def is_solution(state: ArrayLike) -> bool:
    """
    Return True if the given state is a valid n-Queens solution.
    """
    s = np.asarray(state, dtype=int)
    n = int(s.shape[0])
    if n == 0:
        return False
    if np.any(s < 0) or np.any(s >= n):
        return False
    return conflicts(s) == 0


def random_state(n: int, rng: Optional[np.random.Generator] = None) -> np.ndarray:
    """
    Generate a random placement: each row gets a random column in [0, n-1].
    """
    rng = rng or np.random.default_rng()
    return rng.integers(low=0, high=n, size=n, dtype=int)


def pretty_board(state: ArrayLike) -> str:
    """
    Return an ASCII board representation (for debugging/printing).
    Q = queen, . = empty cell.
    """
    s = np.asarray(state, dtype=int)
    n = int(s.shape[0])
    lines: List[str] = []
    for r in range(n):
        row = ["." for _ in range(n)]
        c = int(s[r])
        if 0 <= c < n:
            row[c] = "Q"
        lines.append(" ".join(row))
    return "\n".join(lines)