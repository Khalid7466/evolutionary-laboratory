from __future__ import annotations

from typing import List, Optional, Sequence, Tuple

from core.base import BaseGA


class NQueensGA(BaseGA):
	def __init__(
		self,
		*,
		n: int = 8,
		population_size: int = 100,
		generations: int = 200,
		mutation_prob: float = 0.01,
		elitism: int = 1,
		selection_k: int = 3,
		seed: Optional[int] = None,
	) -> None:
		if n < 4:
			raise ValueError("n must be at least 4.")
		super().__init__(
			population_size=population_size,
			generations=generations,
			crossover_prob=1.0,
			mutation_prob=mutation_prob,
			elitism=elitism,
			seed=seed,
			maximize=True,
		)
		self.n = n
		self.selection_k = max(2, selection_k)

	def initialize_population(self) -> List[List[int]]:
		population: List[List[int]] = []
		for _ in range(self.population_size):
			individual = list(range(self.n))
			self.random.shuffle(individual)
			population.append(individual)
		return population

	def evaluate_fitness(self, individual: List[int]) -> float:
		conflicts = 0
		for i in range(self.n):
			for j in range(i + 1, self.n):
				if abs(individual[i] - individual[j]) == abs(i - j):
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
		size = len(parent1)
		start, end = sorted(self.random.sample(range(size), 2))
		child = [None] * size
		child[start:end] = parent1[start:end]
		fill = [gene for gene in parent2 if gene not in child]
		j = 0
		for i in range(size):
			if child[i] is None:
				child[i] = fill[j]
				j += 1
		child2 = [None] * size
		child2[start:end] = parent2[start:end]
		fill2 = [gene for gene in parent1 if gene not in child2]
		j = 0
		for i in range(size):
			if child2[i] is None:
				child2[i] = fill2[j]
				j += 1
		return list(child), list(child2)

	def mutate(self, individual: List[int]) -> List[int]:
		mutated = list(individual)
		if len(mutated) >= 2:
			i, j = self.random.sample(range(len(mutated)), 2)
			mutated[i], mutated[j] = mutated[j], mutated[i]
		return mutated

	def should_stop(
		self,
		generation: int,
		best_solution: List[int],
		best_fitness: float,
		population: Sequence[List[int]],
		fitness_scores: Sequence[float],
	) -> bool:
		return best_fitness == 0.0
