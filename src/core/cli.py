from __future__ import annotations

import argparse
from typing import List, Tuple

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


PROBLEMS = (
	"ga_function",
	"pso_function",
	"knapsack",
	"tsp",
	"vrp",
	"nqueens",
	"nsp",
	"graph_coloring",
	"feature_selection",
)


def _print_result(best_solution, best_fitness, history) -> None:
	print("Best fitness:", best_fitness)
	print("Generations:", len(history))
	print("Best solution:", best_solution)


def run_ga_function(seed: int) -> None:
	solver = FunctionOptimizationGA(seed=seed)
	best_solution, best_fitness, history = solver.run()
	_print_result(best_solution, best_fitness, history)


def run_pso_function(seed: int) -> None:
	solver = FunctionOptimizationPSO(seed=seed)
	best_solution, best_fitness, history = solver.run()
	_print_result(best_solution, best_fitness, history)


def run_knapsack(seed: int) -> None:
	values = [50, 30, 20, 30, 50]
	weights = [30, 50, 40, 20, 60]
	capacity = 110
	solver = KnapsackGA(values=values, weights=weights, capacity=capacity, seed=seed)
	best_solution, best_fitness, history = solver.run()
	_print_result(best_solution, best_fitness, history)


def run_tsp(seed: int) -> None:
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
	solver = TSPGA(coordinates=coords, labels=labels, seed=seed)
	best_solution, best_fitness, history = solver.run()
	print("Best tour:", solver.decode(best_solution))
	print("Best cost:", solver.tour_cost(best_solution))
	_print_result(best_solution, best_fitness, history)


def run_vrp(seed: int) -> None:
	customers = {
		1: (2.0, 3.0),
		2: (5.0, 4.0),
		3: (1.0, 7.0),
		4: (6.0, 8.0),
		5: (3.0, 6.0),
	}
	solver = VRPGA(customers=customers, depot=(0.0, 0.0), num_vehicles=2, seed=seed)
	best_solution, best_fitness, history = solver.run()
	routes = solver.decode_routes(best_solution)
	print("Routes:", routes)
	print("Total distance:", solver.total_distance(best_solution))
	_print_result(best_solution, best_fitness, history)


def run_nqueens(seed: int) -> None:
	solver = NQueensGA(n=8, seed=seed)
	best_solution, best_fitness, history = solver.run()
	conflicts = int(-best_fitness)
	print("Conflicts:", conflicts)
	_print_result(best_solution, best_fitness, history)


def run_nsp(seed: int) -> None:
	solver = NurseSchedulingGA(seed=seed)
	best_solution, best_fitness, history = solver.run()
	print("Schedule:\n", best_solution)
	_print_result(best_solution, best_fitness, history)


def run_graph_coloring(seed: int) -> None:
	edges = [
		(0, 1),
		(0, 2),
		(1, 2),
		(1, 3),
		(2, 3),
		(3, 4),
		(4, 5),
		(5, 0),
	]
	solver = GraphColoringGA(edges=edges, num_nodes=6, num_colors=3, seed=seed)
	best_solution, best_fitness, history = solver.run()
	conflicts = int(-best_fitness)
	print("Conflicts:", conflicts)
	_print_result(best_solution, best_fitness, history)


def run_feature_selection(seed: int, task: str) -> None:
	if task == "classification":
		x_train, x_test, y_train, y_test = load_classification_data(seed=seed)
	else:
		x_train, x_test, y_train, y_test = load_regression_data(seed=seed)
	solver = FeatureSelectionGA(
		x_train=x_train,
		x_test=x_test,
		y_train=y_train,
		y_test=y_test,
		task=task,
		seed=seed,
	)
	best_solution, best_fitness, history = solver.run()
	selected = [i for i, bit in enumerate(best_solution) if bit == 1]
	print("Selected features:", selected)
	_print_result(best_solution, best_fitness, history)


def build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(description="EvoLab Phase 1 CLI")
	parser.add_argument("problem", nargs="?", default="list", choices=("list",) + PROBLEMS)
	parser.add_argument("--task", choices=("regression", "classification"), default="regression")
	parser.add_argument("--seed", type=int, default=42)
	return parser


def main(argv: List[str] | None = None) -> None:
	parser = build_parser()
	args = parser.parse_args(argv)
	if args.problem == "list":
		print("Available problems:")
		for name in PROBLEMS:
			print("-", name)
		return

	if args.problem == "ga_function":
		run_ga_function(args.seed)
	elif args.problem == "pso_function":
		run_pso_function(args.seed)
	elif args.problem == "knapsack":
		run_knapsack(args.seed)
	elif args.problem == "tsp":
		run_tsp(args.seed)
	elif args.problem == "vrp":
		run_vrp(args.seed)
	elif args.problem == "nqueens":
		run_nqueens(args.seed)
	elif args.problem == "nsp":
		run_nsp(args.seed)
	elif args.problem == "graph_coloring":
		run_graph_coloring(args.seed)
	elif args.problem == "feature_selection":
		run_feature_selection(args.seed, args.task)


if __name__ == "__main__":
	main()
