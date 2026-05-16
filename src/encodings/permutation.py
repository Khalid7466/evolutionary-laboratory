from __future__ import annotations

from typing import List, Sequence, TypeVar
import random

T = TypeVar("T")


def swap_mutation(chromosome: Sequence[T], rng: random.Random | None = None) -> List[T]:
    if len(chromosome) < 2:
        return list(chromosome)
    rand = rng or random
    i, j = rand.sample(range(len(chromosome)), 2)
    mutated = list(chromosome)
    mutated[i], mutated[j] = mutated[j], mutated[i]
    return mutated
