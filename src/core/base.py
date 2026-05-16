from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Sequence, Tuple
import copy
import random

import numpy as np


Callback = Optional[Callable[..., None]]


class BaseOptimizer(ABC):
	def __init__(self, *, seed: Optional[int] = None, maximize: bool = True) -> None:
		self.seed = seed
		self.maximize = maximize
		self.random = random.Random(seed)
		self.rng = np.random.default_rng(seed)
		if seed is not None:
			np.random.seed(seed)
		self.fitness_history: List[float] = []

	def _is_better(self, candidate: float, best: Optional[float]) -> bool:
		if best is None:
			return True
		return candidate > best if self.maximize else candidate < best

	def copy_individual(self, individual: Any) -> Any:
		return copy.deepcopy(individual)

	@abstractmethod
	def run(self, callback: Callback = None) -> Tuple[Any, float, List[float]]:
		raise NotImplementedError


class BaseGA(BaseOptimizer):
	def __init__(
		self,
		*,
		population_size: int,
		generations: int,
		crossover_prob: float = 0.8,
		mutation_prob: float = 0.1,
		elitism: int = 1,
		seed: Optional[int] = None,
		maximize: bool = True,
	) -> None:
		super().__init__(seed=seed, maximize=maximize)
		self.population_size = population_size
		self.generations = generations
		self.crossover_prob = crossover_prob
		self.mutation_prob = mutation_prob
		self.elitism = max(0, elitism)

	@abstractmethod
	def initialize_population(self) -> List[Any]:
		raise NotImplementedError

	@abstractmethod
	def evaluate_fitness(self, individual: Any) -> float:
		raise NotImplementedError

	@abstractmethod
	def select_parent(self, population: Sequence[Any], fitness_scores: Sequence[float]) -> Any:
		raise NotImplementedError

	@abstractmethod
	def crossover(self, parent1: Any, parent2: Any) -> Tuple[Any, Any]:
		raise NotImplementedError

	@abstractmethod
	def mutate(self, individual: Any) -> Any:
		raise NotImplementedError

	def should_stop(
		self,
		generation: int,
		best_solution: Any,
		best_fitness: float,
		population: Sequence[Any],
		fitness_scores: Sequence[float],
	) -> bool:
		return False

	def evaluate_population(self, population: Sequence[Any]) -> List[float]:
		return [self.evaluate_fitness(individual) for individual in population]

	def _select_elites(
		self, population: Sequence[Any], fitness_scores: Sequence[float]
	) -> List[Any]:
		if self.elitism <= 0:
			return []
		indices = list(range(len(population)))
		indices.sort(key=lambda i: fitness_scores[i], reverse=self.maximize)
		return [self.copy_individual(population[i]) for i in indices[: self.elitism]]

	def run(self, callback: Callback = None) -> Tuple[Any, float, List[float]]:
		population = self.initialize_population()
		best_solution: Any = None
		best_fitness: Optional[float] = None
		self.fitness_history = []

		for gen in range(self.generations):
			fitness_scores = self.evaluate_population(population)
			best_idx = max(
				range(len(fitness_scores)),
				key=lambda i: fitness_scores[i] if self.maximize else -fitness_scores[i],
			)
			current_best_fitness = fitness_scores[best_idx]
			if self._is_better(current_best_fitness, best_fitness):
				best_fitness = current_best_fitness
				best_solution = self.copy_individual(population[best_idx])

			self.fitness_history.append(best_fitness if best_fitness is not None else 0.0)

			if callback is not None:
				callback(gen, best_solution, best_fitness, population, fitness_scores)

			if best_solution is not None and best_fitness is not None:
				if self.should_stop(gen, best_solution, best_fitness, population, fitness_scores):
					break

			new_population: List[Any] = []
			new_population.extend(self._select_elites(population, fitness_scores))

			while len(new_population) < self.population_size:
				p1 = self.select_parent(population, fitness_scores)
				p2 = self.select_parent(population, fitness_scores)

				if self.random.random() < self.crossover_prob:
					c1, c2 = self.crossover(p1, p2)
				else:
					c1, c2 = self.copy_individual(p1), self.copy_individual(p2)

				if self.random.random() < self.mutation_prob:
					c1 = self.mutate(c1)
				if len(new_population) < self.population_size:
					new_population.append(c1)

				if len(new_population) < self.population_size:
					if self.random.random() < self.mutation_prob:
						c2 = self.mutate(c2)
					new_population.append(c2)

			population = new_population

		return best_solution, float(best_fitness) if best_fitness is not None else 0.0, self.fitness_history


@dataclass
class Particle:
	position: np.ndarray
	velocity: np.ndarray
	best_position: np.ndarray
	best_fitness: float
	fitness: float


class BasePSO(BaseOptimizer):
	def __init__(
		self,
		*,
		swarm_size: int,
		iterations: int,
		inertia: float = 0.7,
		cognitive: float = 1.5,
		social: float = 1.5,
		seed: Optional[int] = None,
		maximize: bool = True,
	) -> None:
		super().__init__(seed=seed, maximize=maximize)
		self.swarm_size = swarm_size
		self.iterations = iterations
		self.inertia = inertia
		self.cognitive = cognitive
		self.social = social

	@abstractmethod
	def initialize_swarm(self) -> List[Particle]:
		raise NotImplementedError

	@abstractmethod
	def evaluate_fitness(self, position: np.ndarray) -> float:
		raise NotImplementedError

	@abstractmethod
	def update_velocity(self, particle: Particle, gbest_position: np.ndarray) -> None:
		raise NotImplementedError

	@abstractmethod
	def update_position(self, particle: Particle) -> None:
		raise NotImplementedError

	def should_stop(
		self,
		iteration: int,
		best_position: np.ndarray,
		best_fitness: float,
		swarm: Sequence[Particle],
	) -> bool:
		return False

	def run(self, callback: Callback = None) -> Tuple[np.ndarray, float, List[float]]:
		swarm = self.initialize_swarm()
		if not swarm:
			raise ValueError("Swarm must contain at least one particle.")

		gbest_position: Optional[np.ndarray] = None
		gbest_fitness: Optional[float] = None
		for particle in swarm:
			particle.fitness = self.evaluate_fitness(particle.position)
			particle.best_position = particle.position.copy()
			particle.best_fitness = particle.fitness
			if self._is_better(particle.fitness, gbest_fitness):
				gbest_fitness = particle.fitness
				gbest_position = particle.position.copy()

		if gbest_position is None or gbest_fitness is None:
			raise ValueError("Failed to initialize global best from swarm.")

		self.fitness_history = []
		for iteration in range(self.iterations):
			for particle in swarm:
				self.update_velocity(particle, gbest_position)
				self.update_position(particle)

				particle.fitness = self.evaluate_fitness(particle.position)
				if self._is_better(particle.fitness, particle.best_fitness):
					particle.best_fitness = particle.fitness
					particle.best_position = particle.position.copy()

				if self._is_better(particle.fitness, gbest_fitness):
					gbest_fitness = particle.fitness
					gbest_position = particle.position.copy()

			self.fitness_history.append(gbest_fitness)
			if callback is not None:
				callback(iteration, gbest_position, gbest_fitness, swarm)

			if self.should_stop(iteration, gbest_position, gbest_fitness, swarm):
				break

		return gbest_position, float(gbest_fitness), self.fitness_history
