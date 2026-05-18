from __future__ import annotations

from typing import Callable, List, Optional, Tuple
import numpy as np

from core.base import BaseGA
from operators.crossover import arithmetic_crossover
from operators.mutation import gaussian_mutation
from operators.selection import tournament_select_np


FitnessFunction = Callable[[float], float]


def default_fitness(x: float) -> float:
	return x * np.sin(10 * np.pi * x) + 1.0


class FunctionOptimizationGA(BaseGA):
	def __init__(
		self,
		*,
		population_size: int = 40,
		generations: int = 100,
		x_min: float = -1.0,
		x_max: float = 2.0,
		crossover_prob: float = 0.9,
		mutation_prob: float = 0.2,
		mutation_std: float = 0.1,
		selection_k: int = 3,
		elitism: int = 0,
		fitness_fn: Optional[FitnessFunction] = None,
		seed: Optional[int] = None,
	) -> None:
		super().__init__(
			population_size=population_size,
			generations=generations,
			crossover_prob=crossover_prob,
			mutation_prob=mutation_prob,
			elitism=elitism,
			seed=seed,
			maximize=True,
		)
		self.x_min = x_min
		self.x_max = x_max
		self.mutation_std = mutation_std
		self.selection_k = max(2, selection_k)
		self.fitness_fn = fitness_fn or default_fitness

	def initialize_population(self) -> List[float]:
		return list(self.rng.uniform(self.x_min, self.x_max, size=self.population_size))

	def evaluate_fitness(self, individual: float) -> float:
		return float(self.fitness_fn(individual))

	def select_parent(self, population: List[float], fitness_scores: List[float]) -> float:
		selected = tournament_select_np(
			population,
			fitness_scores,
			self.selection_k,
			maximize=self.maximize,
			rng=self.rng,
		)
		return float(selected)

	def crossover(self, parent1: float, parent2: float) -> Tuple[float, float]:
		return arithmetic_crossover(parent1, parent2, rng=self.rng)

	def mutate(self, individual: float) -> float:
		return gaussian_mutation(
			individual,
			rng=self.rng,
			std=self.mutation_std,
			min_val=self.x_min,
			max_val=self.x_max,
		)
