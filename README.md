# EvoLab: Evolutionary Algorithms & PSO Suite 🧬

**EvoLab** is a comprehensive, highly modular Desktop Application built with Python and CustomTkinter. It serves as an interactive laboratory for exploring, parameter-tuning, and visualizing **Genetic Algorithms (GA)** and **Particle Swarm Optimization (PSO)**. 

Designed with a strict Object-Oriented Architecture, the application completely decouples the mathematical optimization engine from the graphical interface, allowing users to modify hyperparameters dynamically and observe solution convergence in real time.

---

## 🚀 Key Features

- **Modern Desktop UI:** Built using `CustomTkinter` for a sleek, responsive, dark/light theme user experience.
- **Decoupled Architecture:** Clean separation of concerns between the UI views (`src/gui/`) and the algorithmic solvers (`src/optimizers/`).
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
├── src/                    # Main source code directory
│   ├── main.py             # Application entry point
│   ├── optimizers/         # Core Optimization Engine (Phase 1)
│   │   ├── __init__.py
│   │   ├── base.py         # Abstract Base Classes (BaseOptimizer, BaseGA, BasePSO)
│   │   ├── function_opt.py # Mathematical Function Optimization
│   │   ├── knapsack.py     # 0/1 Knapsack Problem
│   │   ├── tsp.py          # Traveling Salesperson Problem
│   │   ├── vrp.py          # Vehicle Routing Problem
│   │   ├── nqueens.py      # N-Queens Constraint Problem
│   │   ├── nsp.py          # Nurse Scheduling Problem
│   │   ├── graph_coloring.py # Graph Coloring Problem
│   │   └── feature_selection.py # ML Feature Selection (Classification & Regression)
│   │
│   └── gui/                # User Interface Module (Phase 2)
│       ├── __init__.py
│       ├── app.py          # Main application window framework
│       └── components.py   # UI widgets, sidebars, and plot frames
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
    def solve(self, callback=None):
        raise NotImplementedError

class BaseGeneticAlgorithm(BaseOptimizer):
    def initialize_population(self): pass
    def evaluate_fitness(self): pass
    def selection(self): pass
    def crossover(self): pass
    def mutation(self): pass

class KnapsackGA(BaseGeneticAlgorithm):
    # Overrides fitness evaluation specifically for the Knapsack problem
    def evaluate_fitness(self, chromosome): pass

```

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
