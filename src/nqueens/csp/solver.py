from __future__ import annotations
from typing import List, Optional, Set, Tuple
import time

from .heuristics import select_unassigned_mrv, order_lcv

# --------- Fallback pickers when MRV/LCV are disabled --------- #
def next_unassigned_sequential(assignment: List[Optional[int]], domains: List[Set[int]]) -> int:
    """Pick the first unassigned row (static ordering)."""
    for r, a in enumerate(assignment):
        if a is None:
            return r
    return -1  # all assigned

def order_trivial(row: int, assignment: List[Optional[int]], domains: List[Set[int]]) -> List[int]:
    """Return domain values in deterministic order (no scoring)."""
    return sorted(domains[row])


# ------------------ Core forward checking with trail ------------------ #
def _forward_assign(row: int, col: int,
                    assignment: List[Optional[int]],
                    domains: List[Set[int]],
                    trail: List[Tuple[int, int]]) -> bool:
    """
    Assign 'row -> col' and apply forward checking on neighbors.
    Record all domain removals onto the trail so they can be undone.
    Return False if any neighbor domain becomes empty (domain wipeout).
    """
    assignment[row] = col

    # 1) Shrink this row's domain to {col}
    for v in list(domains[row]):
        if v != col:
            domains[row].remove(v)
            trail.append((row, v))

    # 2) Remove conflicts from other rows' domains
    n = len(domains)
    for r2 in range(n):
        if r2 == row or assignment[r2] is not None:
            continue
        d = r2 - row
        c_same = col          # same column
        c_d1 = col + d        # main diagonal
        c_d2 = col - d        # anti-diagonal
        removed = False
        for v in list(domains[r2]):
            if v == c_same or v == c_d1 or v == c_d2:
                domains[r2].remove(v)
                trail.append((r2, v))
                removed = True
        if not domains[r2]:
            # domain wipeout
            return False
    return True


def _undo_to(trail: List[Tuple[int, int]], domains: List[Set[int]], assignment: List[Optional[int]], mark: int) -> None:
    """Restore all domain removals back to the length 'mark' on the trail."""
    while len(trail) > mark:
        r, v = trail.pop()
        # Only restore if row is currently unassigned; otherwise its domain is {assigned_col}
        if assignment[r] is None:
            domains[r].add(v)


# ------------------ Unified CSP solver with flags ------------------ #
def solve(n: int,
          time_limit: float = 5.0,
          use_mrv: bool = True,
          use_lcv: bool = True) -> Optional[List[int]]:
    """
    Backtracking + Forward Checking CSP solver for N-Queens.
    Optional dynamic ordering:
      - use_mrv=True  -> Most Constrained Variable (MRV) for variable ordering
      - use_lcv=True  -> Least Constraining Value (LCV) for value ordering
    Returns a list 'assignment' where assignment[row] = column (0..n-1),
    or None if time limit is exceeded or no solution is found within the search.
    """
    start = time.perf_counter()

    # domains[row] = set of allowed columns for that row
    domains: List[Set[int]] = [set(range(n)) for _ in range(n)]
    # assignment[row] = chosen column or None if unassigned
    assignment: List[Optional[int]] = [None] * n
    # trail stores (row, value) removed from domains (for undo)
    trail: List[Tuple[int, int]] = []

    # Pickers according to flags
    pick_var = select_unassigned_mrv if use_mrv else next_unassigned_sequential
    order_vals = order_lcv if use_lcv else order_trivial

    def backtrack() -> Optional[List[int]]:
        # Time guard
        if time.perf_counter() - start > time_limit:
            return None

        # Goal test
        if all(a is not None for a in assignment):
            return [int(x) for x in assignment]  # type: ignore

        # Variable selection
        row = pick_var(assignment, domains)
        if row == -1:
            return [int(x) for x in assignment]  # safety

        # Early dead-end check
        if not domains[row]:
            return None

        # Value ordering and recursion
        for val in order_vals(row, assignment, domains):
            mark = len(trail)
            if _forward_assign(row, val, assignment, domains, trail):
                res = backtrack()
                if res is not None:
                    return res
            # undo and unassign
            assignment[row] = None
            _undo_to(trail, domains, assignment, mark)
        return None

    return backtrack()


# ------------------ Convenience wrappers (for experiments) ------------------ #
def solve_basic(n: int, time_limit: float = 5.0, seed: Optional[int] = None) -> Optional[List[int]]:
    """CSP-basic: Backtracking + Forward Checking (no MRV/LCV)."""
    return solve(n, time_limit=time_limit, use_mrv=False, use_lcv=False)


def solve_dynamic(n: int, time_limit: float = 5.0, seed: Optional[int] = None) -> Optional[List[int]]:
    """CSP-dynamic: Backtracking + Forward Checking + MRV + LCV."""
    return solve(n, time_limit=time_limit, use_mrv=True, use_lcv=True)
