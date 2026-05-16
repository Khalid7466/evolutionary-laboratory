from __future__ import annotations

from typing import List, Optional, Sequence, Tuple
import numpy as np

from sklearn.datasets import load_iris, make_friedman1
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, r2_score

from core.base import BaseGA


class FeatureSelectionGA(BaseGA):
	def __init__(
		self,
		*,
		x_train: np.ndarray,
		x_test: np.ndarray,
		y_train: np.ndarray,
		y_test: np.ndarray,
		task: str = "regression",
		population_size: int = 20,
		generations: int = 30,
		mutation_prob: float = 0.3,
		elitism: int = 0,
		selection_k: int = 3,
		seed: Optional[int] = None,
	) -> None:
		super().__init__(
			population_size=population_size,
			generations=generations,
			crossover_prob=1.0,
			mutation_prob=mutation_prob,
			elitism=elitism,
			seed=seed,
			maximize=True,
		)
		self.x_train = x_train
		self.x_test = x_test
		self.y_train = y_train
		self.y_test = y_test
		self.num_features = x_train.shape[1]
		self.task = task
		self.selection_k = max(2, selection_k)
		if task not in {"regression", "classification"}:
			raise ValueError("task must be 'regression' or 'classification'.")

	def initialize_population(self) -> List[List[int]]:
		return [
			[self.random.randint(0, 1) for _ in range(self.num_features)]
			for _ in range(self.population_size)
		]

	def evaluate_fitness(self, individual: List[int]) -> float:
		if sum(individual) == 0:
			return -1.0 if self.task == "regression" else 0.0
		selected = [i for i in range(self.num_features) if individual[i] == 1]
		x_train = self.x_train[:, selected]
		x_test = self.x_test[:, selected]

		if self.task == "regression":
			model = LinearRegression()
			model.fit(x_train, self.y_train)
			preds = model.predict(x_test)
			return float(r2_score(self.y_test, preds))

		model = RandomForestClassifier()
		model.fit(x_train, self.y_train)
		preds = model.predict(x_test)
		return float(accuracy_score(self.y_test, preds))

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
		point = self.random.randint(1, self.num_features - 1)
		child1 = parent1[:point] + parent2[point:]
		child2 = parent2[:point] + parent1[point:]
		return list(child1), list(child2)

	def mutate(self, individual: List[int]) -> List[int]:
		mutated = list(individual)
		idx = self.random.randint(0, self.num_features - 1)
		mutated[idx] = 1 - mutated[idx]
		return mutated


def load_regression_data(
	*,
	n_samples: int = 200,
	n_features: int = 10,
	noise: float = 0.1,
	test_size: float = 0.3,
	seed: Optional[int] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
	X, y = make_friedman1(n_samples=n_samples, n_features=n_features, noise=noise, random_state=seed)
	return train_test_split(X, y, test_size=test_size, random_state=seed)


def load_classification_data(
	*,
	test_size: float = 0.3,
	seed: Optional[int] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
	data = load_iris()
	X = data.data
	y = data.target
	return train_test_split(X, y, test_size=test_size, random_state=seed)
