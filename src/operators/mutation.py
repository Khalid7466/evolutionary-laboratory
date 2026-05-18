from __future__ import annotations

from typing import List, Sequence, TypeVar
import random

import numpy as np


T = TypeVar("T")


def gaussian_mutation(
	value: float,
	*,
	rng: np.random.Generator,
	std: float,
	min_val: float,
	max_val: float,
) -> float:
	mutated = value + float(rng.normal(0.0, std))
	return float(np.clip(mutated, min_val, max_val))


def bit_flip_mutation(
	individual: Sequence[int],
	*,
	rnd: random.Random,
	prob: float,
) -> List[int]:
	mutated = list(individual)
	for i in range(len(mutated)):
		if rnd.random() < prob:
			mutated[i] = 1 - mutated[i]
	return mutated


def single_bit_flip(
	individual: Sequence[int],
	*,
	rnd: random.Random,
) -> List[int]:
	mutated = list(individual)
	if not mutated:
		return mutated
	idx = rnd.randint(0, len(mutated) - 1)
	mutated[idx] = 1 - mutated[idx]
	return mutated


def swap_mutation(
	individual: Sequence[T],
	*,
	rnd: random.Random,
) -> List[T]:
	mutated = list(individual)
	if len(mutated) >= 2:
		i, j = rnd.sample(range(len(mutated)), 2)
		mutated[i], mutated[j] = mutated[j], mutated[i]
	return mutated


def random_reset_mutation(
	individual: Sequence[int],
	*,
	rnd: random.Random,
	upper_exclusive: int,
) -> List[int]:
	mutated = list(individual)
	if not mutated:
		return mutated
	idx = rnd.randint(0, len(mutated) - 1)
	mutated[idx] = rnd.randint(0, upper_exclusive - 1)
	return mutated


def random_reset_matrix(
	individual: np.ndarray,
	*,
	rnd: random.Random,
	choices: Sequence[int],
) -> np.ndarray:
	mutated = individual.copy()
	if mutated.size == 0:
		return mutated
	nurse = rnd.randint(0, mutated.shape[0] - 1)
	day = rnd.randint(0, mutated.shape[1] - 1)
	mutated[nurse][day] = rnd.choice(list(choices))
	return mutated
