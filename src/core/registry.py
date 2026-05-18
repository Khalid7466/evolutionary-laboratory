from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple, Callable
import copy
import time

import numpy as np

from algorithms.ga.problems.ml.feature_selection import (
	FeatureSelectionGA,
	load_classification_data,
	load_regression_data,
)
from algorithms.ga.problems.combinatorial.function_opt import FunctionOptimizationGA
from algorithms.ga.problems.csp.graph_coloring import GraphColoringGA
from algorithms.ga.problems.combinatorial.knapsack import KnapsackGA
from algorithms.ga.problems.csp.nqueens import NQueensGA
from algorithms.ga.problems.csp.nsp import NurseSchedulingGA
from algorithms.ga.problems.routing.tsp import TSPGA
from algorithms.ga.problems.routing.vrp import VRPGA
from algorithms.pso.problems.function_opt import FunctionOptimizationPSO
from core.validation import SpecError, normalize_choice, require, require_keys


PROBLEM_ALIASES = {
	"function optimization": "function_opt",
	"function opt": "function_opt",
	"function": "function_opt",
	"knapsack": "knapsack",
	"tsp": "tsp",
	"traveling salesperson": "tsp",
	"traveling sales": "tsp",
	"vrp": "vrp",
	"vehicle routing": "vrp",
	"n-queens": "nqueens",
	"nqueens": "nqueens",
	"nsp": "nsp",
	"nurse scheduling": "nsp",
	"graph coloring": "graph_coloring",
	"gcp": "graph_coloring",
	"feature selection": "feature_selection",
}

ALGO_ALIASES = {
	"genetic algorithm": "ga",
	"ga": "ga",
	"pso": "pso",
	"particle swarm optimization": "pso",
}


@dataclass
class RunResult:
	status: str
	best_fitness: float
	best_solution: Any
	best_solution_phenotype: Any
	execution_time_sec: float
	fitness_history: list[float]
	graph_artifact: Dict[str, Any]


def _prepare_feature_selection_data(params: Dict[str, Any]) -> Dict[str, Any]:
	if all(key in params for key in ("x_train", "x_test", "y_train", "y_test")):
		return params
	task = params.get("task", "regression")
	seed = params.get("seed")
	data_keys = {"n_samples", "n_features", "noise", "test_size"}
	if task == "classification":
		x_train, x_test, y_train, y_test = load_classification_data(
			test_size=params.get("test_size", 0.3),
			seed=seed,
		)
		params.update(
			{
				"x_train": x_train,
				"x_test": x_test,
				"y_train": y_train,
				"y_test": y_test,
			}
		)
		return params

	x_train, x_test, y_train, y_test = load_regression_data(
		n_samples=params.get("n_samples", 200),
		n_features=params.get("n_features", 10),
		noise=params.get("noise", 0.1),
		test_size=params.get("test_size", 0.3),
		seed=seed,
	)
	params.update(
		{
			"x_train": x_train,
			"x_test": x_test,
			"y_train": y_train,
			"y_test": y_test,
		}
	)
	for key in data_keys:
		params.pop(key, None)
	for key in data_keys:
		params.pop(key, None)
	return params


def build_solver(spec: Dict[str, Any]):
	require(isinstance(spec, dict), "Spec must be a dict.")
	require_keys(spec, ("problem", "algorithm"), "spec")
	params = copy.deepcopy(spec.get("parameters", {}))
	require(isinstance(params, dict), "parameters must be a dict.")

	problem_key = normalize_choice(spec["problem"], PROBLEM_ALIASES, "problem")
	algorithm_key = normalize_choice(spec["algorithm"], ALGO_ALIASES, "algorithm")

	if problem_key == "function_opt" and algorithm_key == "ga":
		return FunctionOptimizationGA(**params), problem_key
	if problem_key == "function_opt" and algorithm_key == "pso":
		return FunctionOptimizationPSO(**params), problem_key
	if problem_key == "knapsack" and algorithm_key == "ga":
		require_keys(params, ("values", "weights", "capacity"), "parameters")
		return KnapsackGA(**params), problem_key
	if problem_key == "tsp" and algorithm_key == "ga":
		require_keys(params, ("coordinates",), "parameters")
		return TSPGA(**params), problem_key
	if problem_key == "vrp" and algorithm_key == "ga":
		require_keys(params, ("customers",), "parameters")
		return VRPGA(**params), problem_key
	if problem_key == "nqueens" and algorithm_key == "ga":
		return NQueensGA(**params), problem_key
	if problem_key == "nsp" and algorithm_key == "ga":
		return NurseSchedulingGA(**params), problem_key
	if problem_key == "graph_coloring" and algorithm_key == "ga":
		require_keys(params, ("edges", "num_nodes"), "parameters")
		return GraphColoringGA(**params), problem_key
	if problem_key == "feature_selection" and algorithm_key == "ga":
		params = _prepare_feature_selection_data(params)
		return FeatureSelectionGA(**params), problem_key

	raise SpecError("Unsupported problem/algorithm combination.")


def _phenotype_from_solution(problem_key: str, solver, best_solution: Any, params: Dict[str, Any]):
	if problem_key == "tsp":
		return solver.decode(best_solution)
	if problem_key == "vrp":
		return solver.decode_routes(best_solution)
	if problem_key == "knapsack":
		labels = params.get("item_labels") or params.get("items")
		if labels:
			return [labels[i] for i, bit in enumerate(best_solution) if bit == 1]
		return [i for i, bit in enumerate(best_solution) if bit == 1]
	if problem_key == "feature_selection":
		return [i for i, bit in enumerate(best_solution) if bit == 1]
	if problem_key == "graph_coloring":
		return {i: color for i, color in enumerate(best_solution)}
	if problem_key == "nqueens":
		return [(row, col) for row, col in enumerate(best_solution)]
	return best_solution


def run_from_spec(spec: Dict[str, Any], callback: Optional[Callable[..., None]] = None) -> RunResult:
	solver, problem_key = build_solver(spec)
	params = spec.get("parameters", {}) if isinstance(spec, dict) else {}
	start = time.perf_counter()
	best_solution, best_fitness, history = solver.run(callback=callback)
	duration = time.perf_counter() - start
	phenotype = _phenotype_from_solution(problem_key, solver, best_solution, params)
	return RunResult(
		status="Execution Completed",
		best_fitness=float(best_fitness),
		best_solution=best_solution,
		best_solution_phenotype=phenotype,
		execution_time_sec=duration,
		fitness_history=history,
		graph_artifact={"fitness_history": history},
	)
