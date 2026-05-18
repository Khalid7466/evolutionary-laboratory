from __future__ import annotations

from typing import List, Optional, Sequence, Tuple
import numpy as np

from core.base import BaseGA
from operators.crossover import order_crossover
from operators.mutation import swap_mutation
from operators.selection import tournament_select


class TSPGA(BaseGA):
	def __init__(
		self,
		*,
		coordinates: Sequence[Sequence[float]],
		labels: Optional[Sequence[str]] = None,
		population_size: int = 30,
		generations: int = 40,
		crossover_prob: float = 0.9,
		mutation_prob: float = 0.25,
		elitism: int = 1,
		selection_k: int = 3,
		fix_start: bool = True,
		seed: Optional[int] = None,
	) -> None:
		coords = np.array(coordinates, dtype=float)
		if coords.ndim != 2 or coords.shape[0] < 2:
			raise ValueError("coordinates must be a 2D array with at least 2 cities.")
		if labels is not None and len(labels) != coords.shape[0]:
			raise ValueError("labels length must match number of cities.")
		super().__init__(
			population_size=population_size,
			generations=generations,
			crossover_prob=crossover_prob,
			mutation_prob=mutation_prob,
			elitism=elitism,
			seed=seed,
			maximize=True,
		)
		self.coords = coords
		self.labels = list(labels) if labels is not None else None
		self.n_cities = coords.shape[0]
		self.selection_k = max(2, selection_k)
		self.fix_start = fix_start
		self.dist_matrix = self._build_distance_matrix(coords)

	@staticmethod
	def _build_distance_matrix(coords: np.ndarray) -> np.ndarray:
		return np.linalg.norm(coords[:, None, :] - coords[None, :, :], axis=2)

	def _normalize(self, chrom: List[int]) -> List[int]:
		if not self.fix_start:
			return chrom
		if 0 not in chrom:
			return chrom
		idx = chrom.index(0)
		return chrom[idx:] + chrom[:idx]

	def initialize_population(self) -> List[List[int]]:
		population: List[List[int]] = []
		for _ in range(self.population_size):
			chrom = list(range(self.n_cities))
			self.random.shuffle(chrom)
			population.append(self._normalize(chrom))
		return population

	def tour_cost(self, chrom: List[int]) -> float:
		cost = 0.0
		for i in range(self.n_cities):
			cost += self.dist_matrix[chrom[i], chrom[(i + 1) % self.n_cities]]
		return float(cost)

	def evaluate_fitness(self, individual: List[int]) -> float:
		cost = self.tour_cost(individual)
		return 1.0 / (cost + 1e-9)

	def select_parent(
		self, population: Sequence[List[int]], fitness_scores: Sequence[float]
	) -> List[int]:
		selected = tournament_select(
			population,
			fitness_scores,
			self.selection_k,
			maximize=self.maximize,
			rnd=self.random,
		)
		return list(selected)

	def crossover(self, parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
		child1, child2 = order_crossover(parent1, parent2, rnd=self.random)
		return self._normalize(child1), self._normalize(child2)

	def mutate(self, individual: List[int]) -> List[int]:
		mutated = swap_mutation(individual, rnd=self.random)
		return self._normalize(mutated)

	def decode(self, chrom: List[int]) -> List[str] | List[int]:
		if self.labels is None:
			return list(chrom) + [chrom[0]]
		return [self.labels[i] for i in chrom] + [self.labels[chrom[0]]]
