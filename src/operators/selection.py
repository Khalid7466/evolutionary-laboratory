from __future__ import annotations

from typing import Sequence, TypeVar
import random

import numpy as np


T = TypeVar("T")


def tournament_select(
	population: Sequence[T],
	fitness_scores: Sequence[float],
	k: int,
	*,
	maximize: bool,
	rnd: random.Random,
) -> T:
	indices = rnd.sample(range(len(population)), k)
	best_idx = max(
		indices,
		key=lambda i: fitness_scores[i] if maximize else -fitness_scores[i],
	)
	return population[best_idx]


def tournament_select_np(
	population: Sequence[T],
	fitness_scores: Sequence[float],
	k: int,
	*,
	maximize: bool,
	rng: np.random.Generator,
) -> T:
	indices = rng.choice(len(population), size=k, replace=False)
	best_idx = max(
		indices,
		key=lambda i: fitness_scores[i] if maximize else -fitness_scores[i],
	)
	return population[int(best_idx)]


def roulette_select(
	population: Sequence[T],
	fitness_scores: Sequence[float],
	rnd: random.Random,
) -> T:
	total = float(sum(fitness_scores))
	if total <= 0.0:
		return rnd.choice(list(population))
	return rnd.choices(list(population), weights=fitness_scores, k=1)[0]
