from __future__ import annotations

from typing import Callable, List, Optional, Tuple
import math
import numpy as np

from core.base import BasePSO, Particle


CostFunction = Callable[[np.ndarray], float]


def ackley_cost(x: np.ndarray) -> float:
	a = 20.0
	b = 0.2
	c = 2.0 * math.pi
	d = len(x)
	term1 = -a * np.exp(-b * np.sqrt(np.sum(x ** 2) / d))
	term2 = -np.exp(np.sum(np.cos(c * x)) / d)
	return float(term1 + term2 + a + math.e)


class FunctionOptimizationPSO(BasePSO):
	def __init__(
		self,
		*,
		dimensions: int = 2,
		swarm_size: int = 30,
		iterations: int = 100,
		bounds: Tuple[float, float] = (-5.0, 5.0),
		inertia: float = 0.7,
		cognitive: float = 1.5,
		social: float = 1.5,
		v_max: float = 0.5,
		cost_fn: Optional[CostFunction] = None,
		seed: Optional[int] = None,
	) -> None:
		super().__init__(
			swarm_size=swarm_size,
			iterations=iterations,
			inertia=inertia,
			cognitive=cognitive,
			social=social,
			seed=seed,
			maximize=False,
		)
		self.dimensions = dimensions
		self.min_bound, self.max_bound = bounds
		self.v_max = v_max
		self.cost_fn = cost_fn or ackley_cost

	def initialize_swarm(self) -> List[Particle]:
		swarm: List[Particle] = []
		for _ in range(self.swarm_size):
			position = self.rng.uniform(self.min_bound, self.max_bound, size=self.dimensions)
			velocity = self.rng.uniform(-self.v_max, self.v_max, size=self.dimensions)
			fitness = self.evaluate_fitness(position)
			swarm.append(
				Particle(
					position=position,
					velocity=velocity,
					best_position=position.copy(),
					best_fitness=fitness,
					fitness=fitness,
				)
			)
		return swarm

	def evaluate_fitness(self, position: np.ndarray) -> float:
		return float(self.cost_fn(position))

	def update_velocity(self, particle: Particle, gbest_position: np.ndarray) -> None:
		r1 = self.rng.random(self.dimensions)
		r2 = self.rng.random(self.dimensions)
		particle.velocity = (
			self.inertia * particle.velocity
			+ self.cognitive * r1 * (particle.best_position - particle.position)
			+ self.social * r2 * (gbest_position - particle.position)
		)
		particle.velocity = np.clip(particle.velocity, -self.v_max, self.v_max)

	def update_position(self, particle: Particle) -> None:
		particle.position = particle.position + particle.velocity
		particle.position = np.clip(particle.position, self.min_bound, self.max_bound)
