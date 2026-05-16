from __future__ import annotations

from typing import Iterable, List, Optional, Sequence, Tuple

from core.base import BaseGA


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
		indices = self.random.sample(range(len(population)), self.selection_k)
		best_idx = max(
			indices,
			key=lambda i: fitness_scores[i] if self.maximize else -fitness_scores[i],
		)
		return list(population[best_idx])

	def crossover(self, parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
		point = self.random.randint(1, self.num_nodes - 1)
		child1 = parent1[:point] + parent2[point:]
		child2 = parent2[:point] + parent1[point:]
		return list(child1), list(child2)

	def mutate(self, individual: List[int]) -> List[int]:
		mutated = list(individual)
		idx = self.random.randint(0, self.num_nodes - 1)
		mutated[idx] = self.random.randint(0, self.num_colors - 1)
		return mutated
