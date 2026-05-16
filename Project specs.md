### 1. Title
Develop a Comprehensive Evolutionary Algorithms Desktop Application (GA & PSO Suite)
### 2. Objective
**Business & Academic Need:**
Build an interactive Graphical User Interface (GUI) that consolidates the core logic of 8 distinct problems solved using Genetic Algorithms (GA) and Particle Swarm Optimization (PSO).
**Technical Goal:**
Implement a clean, Object-Oriented Architecture separating the algorithm logic from the user interface, allowing dynamic parameter tuning and real-time visualization of solution convergence.
### 3. Background / Context
- **Current State:** The algorithm implementations currently exist as isolated, scattered Jupyter Notebooks (Scripts) for each specific problem.
- **The Problem:** There is no unified system to run, test, or compare these algorithms. Parameters are hardcoded, making it difficult to demonstrate the algorithms dynamically during academic discussions.
- **The Solution:** A unified desktop application that acts as a wrapper for all implemented models.
### 4. Scope
**In Scope**
- Implement Core Optimizer Engine (Abstract base classes for GA & PSO).
- Implement 8 specific problem modules (Function Optimization, Knapsack, TSP, VRP, N-Queens, NSP, Graph Coloring, Feature Selection).
- Develop an interactive Desktop GUI.
- Integrate real-time plotting (Fitness vs. Generations).
- Allow dynamic parameter tuning (Population size, Mutation rate, etc.) directly from the UI.
**Out of Scope**
- Web or Mobile App deployment.
- Integrating entirely new algorithms outside the course syllabus.
- Authentication, user management, or security layers (Focus is strictly on the core algorithm and business logic).
### 5. Technical Requirements
**Stack / Tools**
- **Python 3.10+** (Core programming language).
- **CustomTkinter / PyQt6** (For building the modern Desktop GUI).
- **Matplotlib / Seaborn** (For embedding graphs into the GUI).
- **NumPy & Scikit-learn** (For matrix operations and Feature Selection datasets).
**Functional Requirements**
- Accept user selection for Problem Type and Algorithm.
- Accept hyperparameter inputs (Pop Size, Generations, Crossover Rate, Mutation Rate, etc.).
- Run the algorithm without freezing the UI.
- Return the best solution (Phenotype) and optimal fitness score.
- Plot the convergence curve dynamically within the app.
**Non-Functional Requirements**
- **Modularity:** Strict separation between GUI logic and Algorithm logic (OOP approach).
- **Responsiveness:** UI must not crash or freeze during execution.
- **Extensibility:** Adding a new problem in the future should require minimal code changes.
### 6. Input / Output
**Input (Example for Knapsack GA via UI State)**
```json
{
  "problem": "Knapsack",
  "algorithm": "Genetic Algorithm",
  "parameters": {
    "population_size": 100,
    "generations": 50,
    "crossover_prob": 0.8,
    "mutation_prob": 0.1
  }
}
```
**Output (Displayed on UI)**
```json
{
  "status": "Execution Completed",
  "best_fitness": 110.0,
  "best_solution_phenotype": "Items Selected: A, C, D",
  "execution_time_sec": 1.2,
  "graph_artifact": "[Matplotlib Figure object showing fitness history]"
}
```
### 7. Architecture / Flow
**Execution Flow:**
`User (GUI)` → `Selects Problem & Params` → `GUI Controller` → `Optimizer Engine (GA/PSO)` → `Fitness Evaluator` → `Returns Results & History` → `GUI (Updates Text & Plots Graph)`
### 8. Implementation Plan
1. **Refactoring Core Logic:** Convert the Jupyter Notebook scripts into OOP Classes (`BaseOptimizer`, and problem subclasses).
2. **GUI Wireframing:** Design the layout (Sidebar for inputs, Main Area for results/plots).
3. **UI Development:** Program the interface using `CustomTkinter`.
4. **Integration (Phase 1):** Connect a simple problem (e.g., Knapsack) to ensure data flows correctly.
5. **Multithreading Setup:** Offload algorithm execution to a separate worker thread.
6. **Graph Embedding:** Integrate the Matplotlib canvas into the Tkinter window.
7. **Integration (Phase 2):** Connect the remaining complex problems (VRP, NSP, Feature Selection, etc.).
8. **Testing & Bug Fixing:** Ensure smooth execution and accurate graph rendering.
### 9. Acceptance Criteria
- All 8 problems can be solved successfully via the GUI.
- The code architecture is strictly Object-Oriented and clean.
- The UI allows full control over relevant algorithm parameters.
- The fitness curve is successfully generated and displayed natively inside the app.
- The UI remains responsive (no freezing) while the algorithm computes.
### 10. Risks / Challenges
- **UI Freezing:** Heavy computational loops blocking the main event thread (Mitigation: Use `threading` library).
- **Graph Integration:** Binding Matplotlib to Tkinter can cause memory leaks if old plots aren't cleared properly.
- **Computational Overhead:** Problems like VRP or Feature Selection may take significant time; default parameters in the UI should be kept small for quick demonstrations.
### 11. Dependencies
- Final validation of the mathematical logic for all 8 Jupyter notebooks.
- Pre-loading of datasets for the Feature Selection problem (Iris/Friedman) to ensure instant availability within the class.
### 12. Deliverables
- `main.py` (Application entry point).
- `optimizers/` directory (Contains all GA/PSO modular logic).
- `gui/` directory (Contains UI views and controllers).
- `README.md` (Setup and execution instructions).
- Clean, well-documented source code ready for academic defense.
### 13. Phased Approach
**Execution Strategy:**
To ensure stability and a clean architecture, the project will be executed in two strict, sequential phases. **Phase 2 cannot begin until all Acceptance Criteria for Phase 1 are fully met and signed off.**
#### Phase 1: Core Logic & Algorithm Implementation
**Objective:** Refactor all Jupyter Notebook scripts into a robust, Object-Oriented Python backend. Focus entirely on mathematical accuracy and code structure without any graphical interface.
**Phase 1 Acceptance Criteria (Gate to Phase 2):**
- **100% Logic Validation:** All 8 problems (Function Opt, Knapsack, TSP, VRP, N-Queens, NSP, Graph Coloring, Feature Selection) run successfully via the command line/terminal.
- **Output Accuracy:** The generated outputs (fitness scores and phenotypes) match or exceed the baseline results from the original Jupyter Notebooks.
- **OOP Compliance:** `BaseOptimizer` and individual problem subclasses are fully implemented.
- **UI Independence:** The backend code is 100% decoupled from any GUI libraries (no `tkinter` or `PyQt` imports in the logic modules).
#### Phase 2: GUI Development & Integration
**Objective:** Build the interactive Desktop Application and plug in the validated core logic from Phase 1.
**Phase 2 Acceptance Criteria (Project Completion):**
- **Seamless Integration:** The GUI successfully passes user-defined parameters to the Phase 1 backend and retrieves the results.
- **Dynamic Visualization:** Matplotlib convergence curves are generated and embedded natively within the application window.
- **Responsiveness:** Algorithm execution is offloaded to a separate thread, ensuring the UI remains clickable and does not freeze during heavy computations (e.g., VRP or Feature Selection).
- **Full Accessibility:** All 8 implemented problems are selectable and fully functional from the application's main menu.
***
