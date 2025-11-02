from __future__ import annotations
from typing import List, Set, Optional

def select_unassigned_mrv(assignment: List[Optional[int]], domains: List[Set[int]]) -> int:
    """
    Pick the unassigned row with the smallest domain size (MRV).
    """
    best_row: Optional[int] = None
    best_size = 10**9
    for r, a in enumerate(assignment):
        if a is None:
            sz = len(domains[r])
            if sz < best_size:
                best_size = sz
                best_row = r
    # By construction, there must be at least one unassigned variable when called.
    return best_row if best_row is not None else 0

def order_lcv(row: int, assignment: List[Optional[int]], domains: List[Set[int]]) -> list[int]:
    """
    Return row's values ordered by Least Constraining Value (LCV):
    values that remove fewer options from neighbors come first.
    """
    impacts = []  # (impact_score, value)
    current_values = list(domains[row])
    for v in current_values:
        impact = 0
        for r2, a in enumerate(assignment):
            if r2 == row or a is not None:
                continue
            d = r2 - row
            c_same = v
            c_d1   = v + d
            c_d2   = v - d
            # how many of r2's domain values would be removed if row=v?
            for val in domains[r2]:
                if val == c_same or val == c_d1 or val == c_d2:
                    impact += 1
        impacts.append((impact, v))
    impacts.sort(key=lambda x: x[0])  # smaller impact first
    return [v for _, v in impacts]