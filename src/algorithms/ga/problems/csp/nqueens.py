from __future__ import annotations

from typing import List, Optional, Sequence, Tuple

from core.base import BaseGA
from operators.crossover import order_crossover
from operators.mutation import swap_mutation
from operators.selection import tournament_select


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
		selected = tournament_select(
			population,
			fitness_scores,
			self.selection_k,
			maximize=self.maximize,
			rnd=self.random,
		)
		return list(selected)

	def crossover(self, parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
		return order_crossover(parent1, parent2, rnd=self.random)

	def mutate(self, individual: List[int]) -> List[int]:
		return swap_mutation(individual, rnd=self.random)

	def should_stop(
		self,
		generation: int,
		best_solution: List[int],
		best_fitness: float,
		population: Sequence[List[int]],
		fitness_scores: Sequence[float],
	) -> bool:
		return best_fitness == 0.0
