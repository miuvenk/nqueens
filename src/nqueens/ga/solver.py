# src/nqueens/ga/solver.py
from __future__ import annotations
from typing import Optional, List, Tuple
import time
import numpy as np

from nqueens.ga.operators import (
    init_population,
    evaluate_fitness,
    fitness_of,
    tournament_select_index,
    crossover_ox,
    mutate_swap,
    best_individual,
    pair_count,
)

__all__ = ["solve"]


def solve(
    n: int,
    time_limit: float = 5.0,
    seed: Optional[int] = None,
    # Genetic Algorithm hyper-parameters (tune from the experiment runner)
    pop_size: int = 150,
    cx_prob: float = 0.9,
    mut_prob: float = 0.1,
    tournament_size: int = 3,
    elitism: int = 2,
    max_generations: int = 5000,
    stagnation_limit: int = 300,
) -> Optional[List[int]]:
    """
    Genetic Algorithm solver for the N-Queens problem (permutation representation).
    Returns a zero-conflict assignment as a Python list [col_0, col_1, ..., col_{n-1}]
    or None if no perfect individual is found within the time/iteration budget.

    Representation
    -------------
    - Individual is a permutation of [0..n-1]; row index is implicit, value = column.
      This enforces unique columns by construction; only diagonal conflicts remain.

    Fitness
    -------
    - fitness = C(n, 2) - conflicts(individual), so higher is better.
      Perfect solution has fitness == C(n, 2).

    GA operators
    ------------
    - Selection: tournament selection.
    - Crossover: Order Crossover (OX) for permutations.
    - Mutation : swap-mutation with probability `mut_prob`.
    - Replacement: generational, with `elitism` top individuals copied to next population.

    Parameters
    ----------
    n : int
        Board size / number of queens.
    time_limit : float
        Wall-clock time budget in seconds.
    seed : int | None
        RNG seed for reproducibility.
    pop_size : int
        Population size.
    cx_prob : float
        Probability of applying crossover when producing an offspring (else clone).
    mut_prob : float
        Swap-mutation probability per offspring.
    tournament_size : int
        Tournament size for parent selection.
    elitism : int
        Number of best individuals preserved each generation.
    max_generations : int
        Upper bound on the number of generations.
    stagnation_limit : int
        Early-stop if best fitness does not improve for this many generations.
    """
    rng = np.random.default_rng(seed)
    start = time.perf_counter()

    # Guardrails
    pop_size = max(4, int(pop_size))
    elitism = max(0, min(int(elitism), pop_size - 1))
    tournament_size = max(2, int(tournament_size))
    max_fit = pair_count(n)

    # Initial population
    population = init_population(n, pop_size, rng)              # shape: (pop_size, n)
    fitnesses = evaluate_fitness(population)                    # shape: (pop_size,)
    best_idx, best_ind, best_fit = best_individual(population, fitnesses)

    if best_fit == max_fit:
        return list(best_ind)

    gen = 0
    no_improve = 0

    while gen < max_generations and (time.perf_counter() - start) < time_limit:
        gen += 1

        # --- Elitism: copy top-k to the next generation
        # argsort descending
        elite_idx = np.argsort(fitnesses)[::-1][:elitism]
        next_pop = [population[i].copy() for i in elite_idx]

        # --- Produce the rest via selection -> crossover -> mutation
        while len(next_pop) < pop_size:
            i1 = tournament_select_index(fitnesses, tournament_size, rng)
            i2 = tournament_select_index(fitnesses, tournament_size, rng)
            p1 = population[i1]
            p2 = population[i2]

            if rng.random() < cx_prob:
                child = crossover_ox(p1, p2, rng)
            else:
                # Clone a parent (diversity will come from mutation)
                child = p1.copy() if fitnesses[i1] >= fitnesses[i2] else p2.copy()

            mutate_swap(child, rng, mut_prob)
            next_pop.append(child)

        population = np.asarray(next_pop, dtype=int)
        fitnesses = evaluate_fitness(population)

        # Track best-so-far
        cur_idx, cur_ind, cur_fit = best_individual(population, fitnesses)
        if cur_fit > best_fit:
            best_idx, best_ind, best_fit = cur_idx, cur_ind, cur_fit
            no_improve = 0
        else:
            no_improve += 1

        # Perfect solution found
        if best_fit == max_fit:
            return list(best_ind)

        # Early stopping by stagnation (no improvement for many generations)
        if no_improve >= stagnation_limit:
            break

        # Time check (also guarded in while condition)
        if (time.perf_counter() - start) >= time_limit:
            break

    # Return perfect solution only; otherwise None (keeps interface consistent with CSP/SA)
    if best_fit == max_fit:
        return list(best_ind)
    return None