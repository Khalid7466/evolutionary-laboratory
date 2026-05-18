from __future__ import annotations

from typing import List, Optional, Sequence, Tuple
import numpy as np

from core.base import BaseGA
from operators.crossover import column_crossover
from operators.mutation import random_reset_matrix
from operators.selection import tournament_select


class NurseSchedulingGA(BaseGA):
	def __init__(
		self,
		*,
		num_nurses: int = 4,
		days: int = 5,
		shifts: Sequence[int] = (0, 1, 2, 3),
		max_shifts: int = 4,
		population_size: int = 20,
		generations: int = 50,
		mutation_prob: float = 0.3,
		elitism: int = 0,
		selection_k: int = 3,
		seed: Optional[int] = None,
	) -> None:
		if num_nurses <= 0 or days <= 0:
			raise ValueError("num_nurses and days must be positive.")
		super().__init__(
			population_size=population_size,
			generations=generations,
			crossover_prob=1.0,
			mutation_prob=mutation_prob,
			elitism=elitism,
			seed=seed,
			maximize=True,
		)
		self.num_nurses = num_nurses
		self.days = days
		self.shifts = list(shifts)
		self.max_shifts = max_shifts
		self.selection_k = max(2, selection_k)

	def initialize_population(self) -> List[np.ndarray]:
		return [
			self.rng.choice(self.shifts, size=(self.num_nurses, self.days))
			for _ in range(self.population_size)
		]

	def evaluate_fitness(self, individual: np.ndarray) -> float:
		penalty = 0.0
		for nurse in individual:
			work_days = int(np.count_nonzero(nurse))
			if work_days > self.max_shifts:
				penalty += (work_days - self.max_shifts) * 2
		for day in range(self.days):
			if np.all(individual[:, day] == 0):
				penalty += 5
		return float(-penalty)

	def select_parent(
		self, population: Sequence[np.ndarray], fitness_scores: Sequence[float]
	) -> np.ndarray:
		selected = tournament_select(
			population,
			fitness_scores,
			self.selection_k,
			maximize=self.maximize,
			rnd=self.random,
		)
		return selected.copy()

	def crossover(self, parent1: np.ndarray, parent2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
		return column_crossover(parent1, parent2, rnd=self.random)

	def mutate(self, individual: np.ndarray) -> np.ndarray:
		return random_reset_matrix(individual, rnd=self.random, choices=self.shifts)
