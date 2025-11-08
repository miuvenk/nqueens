# src/nqueens/ga/operators.py
from __future__ import annotations
from typing import Tuple, Iterable
import numpy as np

from nqueens.common.state import conflicts

__all__ = [
    "init_population",
    "fitness_of",
    "evaluate_fitness",
    "tournament_select_index",
    "crossover_ox",
    "mutate_swap",
    "best_individual",
    "pair_count",
]


# ---------------------------
# Representation & Fitness
# ---------------------------

def pair_count(n: int) -> int:
    """Number of unordered pairs among n queens = C(n, 2). Used to map conflicts -> fitness."""
    return n * (n - 1) // 2


def fitness_of(individual: np.ndarray) -> int:
    """
    Fitness = (max non-attacking pairs) - (pairwise conflicts).
    With permutation representation, column conflicts are impossible by design,
    so conflicts(...) effectively counts diagonal conflicts only.
    Higher fitness is better; perfect solution has fitness == pair_count(n).
    """
    n = int(individual.size)
    return pair_count(n) - int(conflicts(individual))


def evaluate_fitness(population: np.ndarray) -> np.ndarray:
    """
    Vectorized-ish fitness evaluation for a population of shape (pop_size, n).
    Returns an array of shape (pop_size,) with integer fitness values.
    """
    return np.array([fitness_of(ind) for ind in population], dtype=int)


def init_population(n: int, pop_size: int, rng: np.random.Generator) -> np.ndarray:
    """
    Initialize a population of permutations (each individual is a permutation of 0..n-1).
    Shape: (pop_size, n)
    """
    return np.array([rng.permutation(n) for _ in range(pop_size)], dtype=int)


def best_individual(population: np.ndarray, fitnesses: np.ndarray) -> Tuple[int, np.ndarray, int]:
    """Return (index, individual, fitness) of the best member in the population."""
    idx = int(np.argmax(fitnesses))
    return idx, population[idx].copy(), int(fitnesses[idx])


# ---------------------------
# Selection
# ---------------------------

def tournament_select_index(fitnesses: np.ndarray, t_size: int, rng: np.random.Generator) -> int:
    """
    Tournament selection (indices only). Sample t_size indices without replacement,
    return the index with the highest fitness among them.
    """
    pop_size = int(fitnesses.size)
    t_size = min(max(2, t_size), pop_size)
    contestants = rng.choice(pop_size, size=t_size, replace=False)
    best_local = int(contestants[np.argmax(fitnesses[contestants])])
    return best_local


# ---------------------------
# Crossover (Order Crossover - OX)
# ---------------------------

def crossover_ox(p1: np.ndarray, p2: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """
    Order Crossover (OX) for permutations.
    - Choose two cut points [a, b] with a <= b.
    - Copy p1[a:b+1] into the child at the same positions.
    - Fill remaining positions, in order, with genes from p2 skipping those already present.

    Ensures offspring is a valid permutation (no duplicates).
    """
    n = int(p1.size)
    a, b = int(rng.integers(0, n)), int(rng.integers(0, n))
    if a > b:
        a, b = b, a

    child = np.full(n, -1, dtype=int)
    # Copy middle segment from p1
    child[a:b+1] = p1[a:b+1]
    used = set(child[a:b+1].tolist())

    # Fill remaining positions from p2
    pos = 0
    for gene in p2:
        if gene in used:
            continue
        # find next empty slot
        while child[pos] != -1:
            pos += 1
        child[pos] = int(gene)

    return child


# ---------------------------
# Mutation (Swap Mutation)
# ---------------------------

def mutate_swap(individual: np.ndarray, rng: np.random.Generator, mut_prob: float = 0.1) -> None:
    """
    Swap-mutation for permutations.
    With probability mut_prob, pick two positions i != j and swap them in-place.
    """
    if rng.random() < mut_prob:
        n = int(individual.size)
        i, j = rng.choice(n, size=2, replace=False)
        individual[i], individual[j] = individual[j], individual[i]
