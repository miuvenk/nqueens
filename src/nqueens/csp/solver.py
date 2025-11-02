from __future__ import annotations
from typing import List, Optional, Set, Tuple
import time

from .heuristics import select_unassigned_mrv, order_lcv

def solve(n: int, time_limit: float = 5.0) -> Optional[list[int]]:
    """
    Backtracking + Forward Checking + MRV + LCV CSP solver for n-Queens.
    Returns a list 'assignment' where assignment[row] = column (0..n-1),
    or None if time limit is exceeded or no solution is found within the search.
    """
    start = time.perf_counter()

    # domains[row] = set of allowed columns for that row
    domains: List[Set[int]] = [set(range(n)) for _ in range(n)]
    # assignment[row] = chosen column or None if unassigned
    assignment: List[Optional[int]] = [None] * n
    # trail stores all (row, value) removed from domains, so we can restore on backtrack
    trail: List[Tuple[int, int]] = []

    def forward_assign(row: int, col: int) -> bool:
        """
        Assign 'row -> col' and apply forward checking on neighbors.
        Return False if any neighbor domain becomes empty, True otherwise.
        """
        # Set the assignment first
        assignment[row] = col

        # 1) shrink this row's domain to {col}, record removals onto the trail
        for v in list(domains[row]):
            if v != col:
                domains[row].remove(v)
                trail.append((row, v))

        # 2) remove conflicting values from other rows' domains
        for r2 in range(n):
            if r2 == row or assignment[r2] is not None:
                continue
            d = r2 - row
            c_same = col            # same column
            c_d1   = col + d        # main diagonal conflict
            c_d2   = col - d        # anti-diagonal conflict
            removed_any = False
            for v in list(domains[r2]):
                if v == c_same or v == c_d1 or v == c_d2:
                    domains[r2].remove(v)
                    trail.append((r2, v))
                    removed_any = True
            if not domains[r2]:
                # domain wipeout
                return False
        return True

    def undo(to_len: int) -> None:
        """
        Restore all domain removals back to length 'to_len' on the trail.
        Only restore to rows that are currently unassigned.
        """
        while len(trail) > to_len:
            r, v = trail.pop()
            if assignment[r] is None:
                domains[r].add(v)

    def backtrack() -> Optional[list[int]]:
        # time guard
        if time.perf_counter() - start > time_limit:
            return None

        # goal test
        if all(a is not None for a in assignment):
            return [int(x) for x in assignment]  # type: ignore

        # MRV: pick the row with the smallest domain
        row = select_unassigned_mrv(assignment, domains)
        if not domains[row]:
            return None

        # LCV: try values that constrain neighbors the least first
        for val in order_lcv(row, assignment, domains):
            mark = len(trail)
            if forward_assign(row, val):
                res = backtrack()
                if res is not None:
                    return res
            # undo and unassign
            assignment[row] = None
            undo(mark)
        return None

    return backtrack()
