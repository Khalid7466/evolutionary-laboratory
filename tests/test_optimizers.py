from __future__ import annotations

import os
import sys
import time
from typing import Any, Dict, Tuple

import numpy as np

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if SRC_DIR not in sys.path:
	sys.path.insert(0, SRC_DIR)

from algorithms.ga.problems.feature_selection import (  # noqa: E402
	FeatureSelectionGA,
	load_classification_data,
	load_regression_data,
)
from algorithms.ga.problems.function_opt import FunctionOptimizationGA  # noqa: E402
from algorithms.ga.problems.graph_coloring import GraphColoringGA  # noqa: E402
from algorithms.ga.problems.knapsack import KnapsackGA  # noqa: E402
from algorithms.ga.problems.nqueens import NQueensGA  # noqa: E402
from algorithms.ga.problems.nsp import NurseSchedulingGA  # noqa: E402
from algorithms.ga.problems.tsp import TSPGA  # noqa: E402
from algorithms.ga.problems.vrp import VRPGA  # noqa: E402
from algorithms.pso.problems.function_opt import FunctionOptimizationPSO  # noqa: E402
from core.registry import run_from_spec  # noqa: E402


def run_and_log(name: str, runner) -> Tuple[Any, float, float, int]:
	start = time.perf_counter()
	best_solution, best_fitness, history = runner()
	duration = time.perf_counter() - start
	print(f"{name}: best_fitness={best_fitness}, time={duration:.4f}s")
	print(f"{name}: best_solution={best_solution}")
	assert history is not None
	assert len(history) > 0
	return best_solution, best_fitness, duration, len(history)


def test_ga_function_opt_runs() -> None:
	solver = FunctionOptimizationGA(population_size=20, generations=10, seed=42)
	run_and_log("ga_function", solver.run)


def test_pso_function_opt_runs() -> None:
	solver = FunctionOptimizationPSO(swarm_size=10, iterations=10, seed=42)
	run_and_log("pso_function", solver.run)


def test_knapsack_runs() -> None:
	values = [50, 30, 20, 30, 50]
	weights = [30, 50, 40, 20, 60]
	capacity = 110
	solver = KnapsackGA(
		values=values,
		weights=weights,
		capacity=capacity,
		population_size=10,
		generations=20,
		seed=42,
	)
	run_and_log("knapsack", solver.run)


def test_tsp_runs() -> None:
	coords = np.array(
		[
			[0.0, 0.0],
			[1.0, 3.0],
			[4.0, 2.0],
			[3.0, 0.0],
			[1.0, 4.0],
		]
	)
	labels = ["A", "B", "C", "D", "E"]
	solver = TSPGA(
		coordinates=coords,
		labels=labels,
		population_size=20,
		generations=20,
		seed=42,
	)
	run_and_log("tsp", solver.run)


def test_vrp_runs() -> None:
	customers = {
		1: (2.0, 3.0),
		2: (5.0, 4.0),
		3: (1.0, 7.0),
		4: (6.0, 8.0),
		5: (3.0, 6.0),
	}
	solver = VRPGA(
		customers=customers,
		depot=(0.0, 0.0),
		num_vehicles=2,
		population_size=20,
		generations=20,
		seed=42,
	)
	run_and_log("vrp", solver.run)


def test_nqueens_runs() -> None:
	solver = NQueensGA(n=8, population_size=50, generations=50, seed=42)
	run_and_log("nqueens", solver.run)


def test_nsp_runs() -> None:
	solver = NurseSchedulingGA(population_size=20, generations=20, seed=42)
	run_and_log("nsp", solver.run)


def test_graph_coloring_runs() -> None:
	edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (5, 0)]
	solver = GraphColoringGA(
		edges=edges,
		num_nodes=6,
		num_colors=3,
		population_size=20,
		generations=20,
		seed=42,
	)
	run_and_log("graph_coloring", solver.run)


def test_feature_selection_runs() -> None:
	x_train, x_test, y_train, y_test = load_regression_data(
		n_samples=80,
		n_features=8,
		noise=0.1,
		seed=42,
	)
	solver = FeatureSelectionGA(
		x_train=x_train,
		x_test=x_test,
		y_train=y_train,
		y_test=y_test,
		task="regression",
		population_size=10,
		generations=10,
		seed=42,
	)
	run_and_log("feature_selection", solver.run)


def build_solver_from_spec(spec: Dict[str, Any]):
	problem = spec["problem"]
	algorithm = spec["algorithm"]
	params = spec["parameters"]
	if problem == "Function Optimization" and algorithm == "Genetic Algorithm":
		return FunctionOptimizationGA(**params)
	if problem == "Function Optimization" and algorithm == "PSO":
		return FunctionOptimizationPSO(**params)
	if problem == "Knapsack" and algorithm == "Genetic Algorithm":
		return KnapsackGA(**params)
	if problem == "TSP" and algorithm == "Genetic Algorithm":
		return TSPGA(**params)
	if problem == "VRP" and algorithm == "Genetic Algorithm":
		return VRPGA(**params)
	if problem == "N-Queens" and algorithm == "Genetic Algorithm":
		return NQueensGA(**params)
	if problem == "NSP" and algorithm == "Genetic Algorithm":
		return NurseSchedulingGA(**params)
	if problem == "Graph Coloring" and algorithm == "Genetic Algorithm":
		return GraphColoringGA(**params)
	if problem == "Feature Selection" and algorithm == "Genetic Algorithm":
		return FeatureSelectionGA(**params)
	raise ValueError("Unsupported spec")


def test_json_like_config_execution() -> None:
	coords = np.array(
		[
			[0.0, 0.0],
			[1.0, 3.0],
			[4.0, 2.0],
			[3.0, 0.0],
			[1.0, 4.0],
		]
	)
	customers = {
		1: (2.0, 3.0),
		2: (5.0, 4.0),
		3: (1.0, 7.0),
		4: (6.0, 8.0),
		5: (3.0, 6.0),
	}
	x_train, x_test, y_train, y_test = load_classification_data(seed=42)

	specs = [
		{
			"problem": "Function Optimization",
			"algorithm": "Genetic Algorithm",
			"parameters": {"population_size": 10, "generations": 5, "seed": 42},
		},
		{
			"problem": "Function Optimization",
			"algorithm": "PSO",
			"parameters": {"swarm_size": 10, "iterations": 5, "seed": 42},
		},
		{
			"problem": "Knapsack",
			"algorithm": "Genetic Algorithm",
			"parameters": {
				"values": [50, 30, 20, 30, 50],
				"weights": [30, 50, 40, 20, 60],
				"capacity": 110,
				"population_size": 6,
				"generations": 5,
				"seed": 42,
			},
		},
		{
			"problem": "TSP",
			"algorithm": "Genetic Algorithm",
			"parameters": {
				"coordinates": coords,
				"population_size": 10,
				"generations": 5,
				"seed": 42,
			},
		},
		{
			"problem": "VRP",
			"algorithm": "Genetic Algorithm",
			"parameters": {
				"customers": customers,
				"num_vehicles": 2,
				"population_size": 10,
				"generations": 5,
				"seed": 42,
			},
		},
		{
			"problem": "N-Queens",
			"algorithm": "Genetic Algorithm",
			"parameters": {"n": 8, "population_size": 20, "generations": 5, "seed": 42},
		},
		{
			"problem": "NSP",
			"algorithm": "Genetic Algorithm",
			"parameters": {"population_size": 10, "generations": 5, "seed": 42},
		},
		{
			"problem": "Graph Coloring",
			"algorithm": "Genetic Algorithm",
			"parameters": {
				"edges": [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)],
				"num_nodes": 4,
				"num_colors": 3,
				"population_size": 10,
				"generations": 5,
				"seed": 42,
			},
		},
		{
			"problem": "Feature Selection",
			"algorithm": "Genetic Algorithm",
			"parameters": {
				"x_train": x_train,
				"x_test": x_test,
				"y_train": y_train,
				"y_test": y_test,
				"task": "classification",
				"population_size": 10,
				"generations": 5,
				"seed": 42,
			},
		},
	]

	for spec in specs:
		solver = build_solver_from_spec(spec)
		best_solution, best_fitness, history = solver.run()
		assert history
		assert best_solution is not None
		assert isinstance(best_fitness, float)


def test_registry_run_from_spec() -> None:
	coords = np.array(
		[
			[0.0, 0.0],
			[1.0, 3.0],
			[4.0, 2.0],
			[3.0, 0.0],
			[1.0, 4.0],
		]
	)
	tsp_spec = {
		"problem": "Traveling Salesperson",
		"algorithm": "GA",
		"parameters": {
			"coordinates": coords,
			"population_size": 10,
			"generations": 5,
			"seed": 42,
		},
	}
	result = run_from_spec(tsp_spec)
	assert result.status == "Execution Completed"
	assert isinstance(result.best_fitness, float)
	assert result.fitness_history
	assert result.graph_artifact["fitness_history"] == result.fitness_history

	fs_spec = {
		"problem": "Feature Selection",
		"algorithm": "Genetic Algorithm",
		"parameters": {
			"task": "regression",
			"n_samples": 60,
			"n_features": 6,
			"noise": 0.1,
			"test_size": 0.3,
			"population_size": 8,
			"generations": 5,
			"seed": 42,
		},
	}
	fs_result = run_from_spec(fs_spec)
	assert fs_result.status == "Execution Completed"
	assert isinstance(fs_result.best_fitness, float)
	assert fs_result.fitness_history
