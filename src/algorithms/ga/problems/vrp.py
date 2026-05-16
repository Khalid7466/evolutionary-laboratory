from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple
import math

from core.base import BaseGA


class VRPGA(BaseGA):
	def __init__(
		self,
		*,
		customers: Dict[int, Tuple[float, float]],
		depot: Tuple[float, float] = (0.0, 0.0),
		num_vehicles: int = 2,
		population_size: int = 20,
		generations: int = 100,
		crossover_prob: float = 0.9,
		mutation_prob: float = 0.1,
		elitism: int = 0,
		seed: Optional[int] = None,
	) -> None:
		if not customers:
			raise ValueError("customers must not be empty.")
		if num_vehicles <= 0:
			raise ValueError("num_vehicles must be positive.")
		super().__init__(
			population_size=population_size,
			generations=generations,
			crossover_prob=crossover_prob,
			mutation_prob=mutation_prob,
			elitism=elitism,
			seed=seed,
			maximize=True,
		)
		self.customers = dict(customers)
		self.customer_ids = list(customers.keys())
		self.depot = depot
		self.num_vehicles = num_vehicles

	@staticmethod
	def _distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
		return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

	def decode_routes(self, chromosome: Sequence[int]) -> List[List[int]]:
		routes = [[] for _ in range(self.num_vehicles)]
		for i, customer in enumerate(chromosome):
			routes[i % self.num_vehicles].append(customer)
		return routes

	def initialize_population(self) -> List[List[int]]:
		population: List[List[int]] = []
		for _ in range(self.population_size):
			individual = list(self.customer_ids)
			self.random.shuffle(individual)
			population.append(individual)
		return population

	def total_distance(self, chromosome: Sequence[int]) -> float:
		routes = self.decode_routes(chromosome)
		total = 0.0
		for route in routes:
			if not route:
				continue
			prev = self.depot
			for customer in route:
				point = self.customers[customer]
				total += self._distance(prev, point)
				prev = point
			total += self._distance(prev, self.depot)
		return total

	def evaluate_fitness(self, individual: List[int]) -> float:
		distance = self.total_distance(individual)
		return 1.0 / (distance + 1e-9)

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
