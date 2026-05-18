from __future__ import annotations

from typing import List, Sequence, Tuple, TypeVar
import random

import numpy as np


T = TypeVar("T")


def arithmetic_crossover(
	parent1: float,
	parent2: float,
	*,
	rng: np.random.Generator,
) -> Tuple[float, float]:
	alpha = float(rng.random())
	c1 = alpha * parent1 + (1.0 - alpha) * parent2
	c2 = alpha * parent2 + (1.0 - alpha) * parent1
	return float(c1), float(c2)


def one_point_crossover(
	parent1: Sequence[T],
	parent2: Sequence[T],
	*,
	rnd: random.Random,
) -> Tuple[List[T], List[T]]:
	size = len(parent1)
	if size < 2:
		return list(parent1), list(parent2)
	point = rnd.randint(1, size - 1)
	child1 = list(parent1[:point]) + list(parent2[point:])
	child2 = list(parent2[:point]) + list(parent1[point:])
	return child1, child2


def order_crossover(
	parent1: Sequence[T],
	parent2: Sequence[T],
	*,
	rnd: random.Random,
) -> Tuple[List[T], List[T]]:
	size = len(parent1)
	if size < 2:
		return list(parent1), list(parent2)
	start, end = sorted(rnd.sample(range(size), 2))

	def build_child(p1: Sequence[T], p2: Sequence[T]) -> List[T]:
		child: List[T | None] = [None] * size
		child[start:end] = list(p1[start:end])
		idx = end % size
		for gene in p2:
			if gene not in child:
				while child[idx] is not None:
					idx = (idx + 1) % size
				child[idx] = gene
				idx = (idx + 1) % size
		return [gene for gene in child if gene is not None]

	return build_child(parent1, parent2), build_child(parent2, parent1)


def column_crossover(
	parent1: np.ndarray,
	parent2: np.ndarray,
	*,
	rnd: random.Random,
) -> Tuple[np.ndarray, np.ndarray]:
	if parent1.shape[1] < 2:
		return parent1.copy(), parent2.copy()
	point = rnd.randint(1, parent1.shape[1] - 1)
	child1 = np.hstack((parent1[:, :point], parent2[:, point:]))
	child2 = np.hstack((parent2[:, :point], parent1[:, point:]))
	return child1, child2
