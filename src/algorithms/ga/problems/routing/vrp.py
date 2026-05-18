from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple
import math

from core.base import BaseGA
from operators.crossover import order_crossover
from operators.mutation import swap_mutation
from operators.selection import roulette_select


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
		selected = roulette_select(population, fitness_scores, rnd=self.random)
		return list(selected)

	def crossover(self, parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
		return order_crossover(parent1, parent2, rnd=self.random)

	def mutate(self, individual: List[int]) -> List[int]:
		return swap_mutation(individual, rnd=self.random)
