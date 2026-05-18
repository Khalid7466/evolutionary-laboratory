# EvoLab: Evolutionary Algorithms & PSO Suite 🧬

**EvoLab** is a comprehensive, highly modular Desktop Application built with Python and CustomTkinter. It serves as an interactive laboratory for exploring, parameter-tuning, and visualizing **Genetic Algorithms (GA)** and **Particle Swarm Optimization (PSO)**. 

Designed with a strict Object-Oriented Architecture, the application completely decouples the mathematical optimization engine from the graphical interface, allowing users to modify hyperparameters dynamically and observe solution convergence in real time.

---

## 🚀 Key Features

- **Modern Desktop UI:** Built using `CustomTkinter` for a sleek, responsive, dark/light theme user experience.
- **Decoupled Architecture:** Clean separation of concerns between the UI views (`src/gui/`) and the core engine (`src/core/`, `src/algorithms/`).
- **Multithreaded Execution:** Optimization loops run on separate worker threads to keep the GUI fully responsive and prevent freezing during heavy calculations.
- **Real-Time Visualization:** Embedded `Matplotlib` canvas displays dynamic convergence curves (Fitness vs. Generations/Iterations) for immediate analysis.
- **Comprehensive Problem Suite:** Solves 8 complex computational problems across 4 foundational domains using natural encodings (Binary, Real-Coded, and Permutation).

---

## 📂 Project Structure

The repository is structured following software engineering best practices for modularity and scalability:

```text
EvoLab/
├── pyproject.toml          # Project configuration and dependency management
├── uv.lock                 # Strict dependency lock file for reproducibility
├── README.md               # Comprehensive documentation
├── .gitignore              # Files and directories to be ignored by Git
├── main.py                 # Root entry point (launches GUI)
├── org-notebooks/          # Original notebooks (reference only)
├── src/                    # Main source code directory
│   ├── main.py             # Application entry point (Phase 2)
│   ├── core/               # Core engine contracts and shared logic
│   │   ├── __init__.py
│   │   ├── base.py          # BaseOptimizer, BaseGA, BasePSO
│   │   ├── registry.py      # Unified entry point for GUI
│   │   └── validation.py    # Input validation and bounds checks
│   ├── encodings/          # Genotype/phenotype conversions
│   │   ├── __init__.py
│   │   ├── binary.py
│   │   ├── gray.py
│   │   ├── real.py
│   │   └── permutation.py
│   ├── operators/          # Selection, crossover, and mutation operators
│   │   └── __init__.py
│   ├── algorithms/         # Problem implementations
│   │   ├── __init__.py
│   │   ├── ga/
│   │   │   ├── __init__.py
│   │   │   └── problems/
│   │   │       ├── __init__.py
│   │   │       ├── combinatorial/
│   │   │       │   ├── __init__.py
│   │   │       │   ├── function_opt.py
│   │   │       │   └── knapsack.py
│   │   │       ├── routing/
│   │   │       │   ├── __init__.py
│   │   │       │   ├── tsp.py
│   │   │       │   └── vrp.py
│   │   │       ├── csp/
│   │   │       │   ├── __init__.py
│   │   │       │   ├── nqueens.py
│   │   │       │   ├── nsp.py
│   │   │       │   └── graph_coloring.py
│   │   │       └── ml/
│   │   │           ├── __init__.py
│   │   │           └── feature_selection.py
│   │   └── pso/
│   │       ├── __init__.py
│   │       └── problems/
│   │           ├── __init__.py
│   │           └── function_opt.py
│   └── gui/                # User Interface Module (Phase 2)
│       ├── __init__.py
│       ├── app.py           # Main application window framework
│       ├── theme.py         # GUI theme tokens
│       └── views/           # Screens and view logic
│           ├── home.py
│           ├── ga_view.py
│           └── pso_view.py
│
└── tests/                  # Backend Testing Suite
    └── test_optimizers.py  # Unit tests for core algorithm validation

```

---

## 🛠️ Implemented Domains & Problems

### 1. Combinatorial & Function Optimization

* **Function Optimization:** Maximizing or minimizing complex non-linear mathematical equations using real-coded arithmetic operators and Gaussian mutations.
* **0/1 Knapsack Problem:** Selecting an optimal subset of items to maximize value under strict weight capacity constraints using binary chromosome representations.

### 2. Routing & Logistics

* **Traveling Salesperson Problem (TSP):** Finding the absolute shortest closed-loop route to visit a set of cities exactly once using permutation encoding and Order Crossover (OX) to preserve sequence validity.
* **Vehicle Routing Problem (VRP):** An advanced extension of TSP optimizing a fleet of multiple vehicles originating from a central depot to distribute goods efficiently.

### 3. Constraint Satisfaction Problems (CSP)

* **N-Queens Problem:** Placing $N$ chess queens on an $N \times N$ board such that no two queens threaten each other, utilizing conflict-minimizing fitness functions.
* **Nurse Scheduling Problem (NSP):** Generating shift schedules that satisfy complex institutional constraints (maximum weekly hours, consecutive shift bans, and required shift coverage).
* **Graph Coloring Problem (GCP):** Coloring all vertices of a graph such that adjacent nodes do not share the same color, aiming to minimize the total number of colors used via `networkx`.

### 4. Machine Learning Applications

* **Feature Selection:** Using binary Genetic Algorithms as a wrapper to filter features and maximize prediction metrics ($R^2$ for Linear Regression via the Friedman dataset and Accuracy for Random Forest via the Iris dataset).

---

## ⚙️ Core Optimization Architecture

The core solver engine relies on robust Object-Oriented Principles. Adding a new problem or metaheuristic requires zero modifications to the interface.

```python
# Conceptual architecture of the backend engine
class BaseOptimizer:
    def run(self, callback=None):
        raise NotImplementedError

class BaseGA(BaseOptimizer):
    def initialize_population(self): pass
    def evaluate_fitness(self): pass
    def select_parent(self): pass
    def crossover(self): pass
    def mutate(self): pass

class KnapsackGA(BaseGA):
    # Overrides fitness evaluation specifically for the Knapsack problem
    def evaluate_fitness(self, chromosome): pass

```

---

## 🧭 Folder Guide

**Top-level**

- **src/**: All production source code.
- **tests/**: Phase 1 validation tests for all solvers.
- **org-notebooks/**: Original reference notebooks only (no production code).
- **main.py**: Lightweight CLI entry (temporary until GUI is complete).

**Inside `src/`**

- **core/**: Base classes, shared engine contracts, registry, and validation logic.
- **encodings/**: Binary, gray, real, and permutation encoding utilities.
- **operators/**: Reusable GA operators (selection, crossover, mutation).
- **algorithms/ga/**: GA problem implementations grouped by domain (combinatorial, routing, CSP, ML).
- **algorithms/pso/**: PSO problem implementations.
- **gui/**: UI layer and screens (must not import from GUI inside core/algorithms).

---

## 🚀 Installation & Setup

This project uses `uv`, an ultra-fast Python package installer and resolver.

### 1. Clone the Repository

```bash
git clone [https://github.com/USERNAME/EvoLab.git](https://github.com/USERNAME/EvoLab.git)
cd EvoLab

```

### 2. Initialize and Install Dependencies

Ensure you have `uv` installed, then run the following command to automatically create a virtual environment and sync all required packages:

```bash
uv sync

```

*Dependencies installed include: `numpy`, `matplotlib`, `scikit-learn`, `customtkinter`, `networkx`, and `pytest` (dev).*

### 3. Run the Application

Execute the application directly within the isolated environment:

```bash
uv run src/main.py

```

### 4. Run Tests (Phase 1 Validation)

To ensure the mathematical engine is functioning perfectly before launching the GUI, execute the test suite:

```bash
uv run pytest

```

---

## 📅 Development Strategy (Phased Approach)

To ensure maximum software reliability, development is strictly split into two gated phases:

1. **Phase 1 (Core Logic):** Complete refactoring of all standalone scripts into the OOP structure. Passing 100% of the unit tests is a hard requirement to proceed.
2. **Phase 2 (GUI & Integration):** Assembling the `CustomTkinter` dashboard, implementing multithreading worker pipelines, and embedding the `Matplotlib` live graphs.

---

## 📄 License

This project is developed for academic purposes as part of the **Genetic Algorithms** course curriculum. All core implementations reflect modular, production-ready AI application design.

```
