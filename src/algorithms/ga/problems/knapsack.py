from __future__ import annotations

from typing import List, Optional, Sequence, Tuple

from core.base import BaseGA


class KnapsackGA(BaseGA):
	def __init__(
		self,
		*,
		values: Sequence[float],
		weights: Sequence[float],
		capacity: float,
		population_size: int = 6,
		generations: int = 30,
		crossover_prob: float = 0.9,
		mutation_prob: float = 0.1,
		elitism: int = 0,
		seed: Optional[int] = None,
	) -> None:
		if len(values) != len(weights):
			raise ValueError("values and weights must have the same length.")
		if len(values) == 0:
			raise ValueError("values and weights must not be empty.")
		super().__init__(
			population_size=population_size,
			generations=generations,
			crossover_prob=crossover_prob,
			mutation_prob=1.0,
			elitism=elitism,
			seed=seed,
			maximize=True,
		)
		self.values = list(values)
		self.weights = list(weights)
		self.capacity = capacity
		self.num_items = len(values)
		self.bit_mutation_prob = mutation_prob

	def initialize_population(self) -> List[List[int]]:
		return [
			[self.random.randint(0, 1) for _ in range(self.num_items)]
			for _ in range(self.population_size)
		]

	def evaluate_fitness(self, individual: List[int]) -> float:
		total_value = 0.0
		total_weight = 0.0
		for i in range(self.num_items):
			if individual[i] == 1:
				total_value += self.values[i]
				total_weight += self.weights[i]
		if total_weight > self.capacity:
			return 0.0
		return float(total_value)

	def select_parent(
		self, population: Sequence[List[int]], fitness_scores: Sequence[float]
	) -> List[int]:
		total_fitness = float(sum(fitness_scores))
		if total_fitness == 0.0:
			return list(self.random.choice(population))
		probabilities = [score / total_fitness for score in fitness_scores]
		selected = self.random.choices(population, probabilities, k=1)[0]
		return list(selected)

	def crossover(self, parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
		if self.num_items < 2:
			return list(parent1), list(parent2)
		point = self.random.randint(1, self.num_items - 1)
		child1 = parent1[:point] + parent2[point:]
		child2 = parent2[:point] + parent1[point:]
		return child1, child2

	def mutate(self, individual: List[int]) -> List[int]:
		mutated = list(individual)
		for i in range(self.num_items):
			if self.random.random() < self.bit_mutation_prob:
				mutated[i] = 1 - mutated[i]
		return mutated
