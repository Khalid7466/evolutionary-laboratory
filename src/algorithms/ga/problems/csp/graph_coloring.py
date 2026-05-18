from __future__ import annotations

from typing import List, Optional, Sequence, Tuple

from core.base import BaseGA
from operators.crossover import one_point_crossover
from operators.mutation import random_reset_mutation
from operators.selection import tournament_select


class GraphColoringGA(BaseGA):
	def __init__(
		self,
		*,
		edges: Sequence[Tuple[int, int]],
		num_nodes: int,
		num_colors: int = 3,
		population_size: int = 20,
		generations: int = 50,
		mutation_prob: float = 0.3,
		elitism: int = 0,
		selection_k: int = 3,
		seed: Optional[int] = None,
	) -> None:
		if num_nodes <= 0:
			raise ValueError("num_nodes must be positive.")
		if num_colors <= 0:
			raise ValueError("num_colors must be positive.")
		super().__init__(
			population_size=population_size,
			generations=generations,
			crossover_prob=1.0,
			mutation_prob=mutation_prob,
			elitism=elitism,
			seed=seed,
			maximize=True,
		)
		self.edges = list(edges)
		self.num_nodes = num_nodes
		self.num_colors = num_colors
		self.selection_k = max(2, selection_k)

	def initialize_population(self) -> List[List[int]]:
		return [
			[self.random.randint(0, self.num_colors - 1) for _ in range(self.num_nodes)]
			for _ in range(self.population_size)
		]

	def evaluate_fitness(self, individual: List[int]) -> float:
		conflicts = 0
		for u, v in self.edges:
			if individual[u] == individual[v]:
				conflicts += 1
		return float(-conflicts)

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
		return one_point_crossover(parent1, parent2, rnd=self.random)

	def mutate(self, individual: List[int]) -> List[int]:
		return random_reset_mutation(
			individual,
			rnd=self.random,
			upper_exclusive=self.num_colors,
		)
