from __future__ import annotations

from typing import List, Optional, Sequence, Tuple
import numpy as np

from sklearn.datasets import load_iris, make_friedman1
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, r2_score

from core.base import BaseGA
from operators.crossover import one_point_crossover
from operators.mutation import single_bit_flip
from operators.selection import tournament_select


class FeatureSelectionGA(BaseGA):
	def __init__(
		self,
		*,
		x_train: np.ndarray,
		x_test: np.ndarray,
		y_train: np.ndarray,
		y_test: np.ndarray,
		task: str = "regression",
		model: str = "linear",
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
		self.model_key = model.strip().lower().replace(" ", "_")
		self._fitness_cache: dict[tuple[int, ...], float] = {}
		self.selection_k = max(2, selection_k)
		if task not in {"regression", "classification"}:
			raise ValueError("task must be 'regression' or 'classification'.")

	def initialize_population(self) -> List[List[int]]:
		return [
			[self.random.randint(0, 1) for _ in range(self.num_features)]
			for _ in range(self.population_size)
		]

	def evaluate_fitness(self, individual: List[int]) -> float:
		key = tuple(individual)
		cached = self._fitness_cache.get(key)
		if cached is not None:
			return cached
		if sum(individual) == 0:
			fitness = -1.0 if self.task == "regression" else 0.0
			self._fitness_cache[key] = fitness
			return fitness
		selected = [i for i in range(self.num_features) if individual[i] == 1]
		x_train = self.x_train[:, selected]
		x_test = self.x_test[:, selected]

		if self.task == "regression":
			regressor = self._build_regressor()
			regressor.fit(x_train, self.y_train)
			preds = regressor.predict(x_test)
			fitness = float(r2_score(self.y_test, preds))
			self._fitness_cache[key] = fitness
			return fitness

		classifier = self._build_classifier()
		classifier.fit(x_train, self.y_train)
		preds = classifier.predict(x_test)
		fitness = float(accuracy_score(self.y_test, preds))
		self._fitness_cache[key] = fitness
		return fitness

	def _build_regressor(self):
		if self.model_key in {"random_forest", "random_forest_regressor"}:
			return RandomForestRegressor(
				n_estimators=50,
				max_depth=6,
				random_state=self.seed,
			)
		return LinearRegression()

	def _build_classifier(self):
		if self.model_key in {"logistic", "logistic_regression", "linear", "linear_regression"}:
			return LogisticRegression(max_iter=300, random_state=self.seed, solver="lbfgs")
		return RandomForestClassifier(
			n_estimators=50,
			max_depth=6,
			random_state=self.seed,
		)

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
		return one_point_crossover(parent1, parent2, rnd=self.random)

	def mutate(self, individual: List[int]) -> List[int]:
		return single_bit_flip(individual, rnd=self.random)


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
