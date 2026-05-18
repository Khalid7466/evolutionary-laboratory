import customtkinter as ctk
import threading
import random
from gui import theme
from core import registry

PROBLEM_DISPLAY = {
	"ga_function_opt": "Function Optimization",
	"ga_knapsack": "0/1 Knapsack",
	"ga_tsp": "Traveling Salesperson (TSP)",
	"ga_vrp": "Vehicle Routing (VRP)",
	"ga_nqueens": "N-Queens",
	"ga_nsp": "Nurse Scheduling (NSP)",
	"ga_graph_coloring": "Graph Coloring",
	"ga_feature_selection": "Feature Selection",
}

CATEGORY_GROUPS = [
	("combinatorial", "Combinatorial & Function Optimization", ["ga_function_opt", "ga_knapsack"]),
	("routing", "Routing & Logistics", ["ga_tsp", "ga_vrp"]),
	("csp", "Constraint Satisfaction (CSP)", ["ga_nqueens", "ga_nsp", "ga_graph_coloring"]),
	("ml", "Machine Learning Applications", ["ga_feature_selection"]),
]

PROBLEM_PARAMS = {
	"ga_function_opt": [
		{"label": "Population Size",   "key": "pop_size",    "type": "int",   "default": "100"},
		{"label": "Generations",       "key": "generations", "type": "int",   "default": "200"},
		{"label": "Crossover Rate",    "key": "cx_rate",     "type": "float", "default": "0.85"},
		{"label": "Mutation Rate",     "key": "mut_rate",    "type": "float", "default": "0.12"},
		{"label": "Function", "key": "function", "type": "choice",
		 "options": ["Rastrigin", "Rosenbrock", "Sphere", "Ackley"], "default": "Rastrigin"},
		{"label": "Dimensions",        "key": "dimensions",  "type": "int",   "default": "10"},
		{"label": "Lower Bound",       "key": "lb",          "type": "float", "default": "-5.12"},
		{"label": "Upper Bound",       "key": "ub",          "type": "float", "default": "5.12"},
		{"label": "Seed",              "key": "seed",        "type": "int",   "default": "42"},
	],
	"ga_knapsack": [
		{"label": "Population Size",   "key": "pop_size",    "type": "int",   "default": "100"},
		{"label": "Generations",       "key": "generations", "type": "int",   "default": "150"},
		{"label": "Crossover Rate",    "key": "cx_rate",     "type": "float", "default": "0.80"},
		{"label": "Mutation Rate",     "key": "mut_rate",    "type": "float", "default": "0.05"},
		{"label": "Num Items",         "key": "num_items",   "type": "int",   "default": "20"},
		{"label": "Capacity (0=Auto)", "key": "capacity",    "type": "int",   "default": "50"},
		{"label": "Seed",              "key": "seed",        "type": "int",   "default": "42"},
	],
	"ga_tsp": [
		{"label": "Population Size",   "key": "pop_size",    "type": "int",   "default": "100"},
		{"label": "Generations",       "key": "generations", "type": "int",   "default": "300"},
		{"label": "Crossover Rate",    "key": "cx_rate",     "type": "float", "default": "0.90"},
		{"label": "Mutation Rate",     "key": "mut_rate",    "type": "float", "default": "0.02"},
		{"label": "Num Cities",        "key": "num_cities",  "type": "int",   "default": "20"},
		{"label": "Seed",              "key": "seed",        "type": "int",   "default": "42"},
	],
	"ga_vrp": [
		{"label": "Population Size",   "key": "pop_size",    "type": "int",   "default": "100"},
		{"label": "Generations",       "key": "generations", "type": "int",   "default": "300"},
		{"label": "Crossover Rate",    "key": "cx_rate",     "type": "float", "default": "0.90"},
		{"label": "Mutation Rate",     "key": "mut_rate",    "type": "float", "default": "0.02"},
		{"label": "Num Cities",        "key": "num_cities",  "type": "int",   "default": "15"},
		{"label": "Num Vehicles",      "key": "num_vehicles","type": "int",   "default": "3"},
		{"label": "Vehicle Capacity",  "key": "capacity",    "type": "int",   "default": "30"},
		{"label": "Seed",              "key": "seed",        "type": "int",   "default": "42"},
	],
	"ga_nqueens": [
		{"label": "Population Size",   "key": "pop_size",    "type": "int",   "default": "100"},
		{"label": "Generations",       "key": "generations", "type": "int",   "default": "200"},
		{"label": "Crossover Rate",    "key": "cx_rate",     "type": "float", "default": "0.85"},
		{"label": "Mutation Rate",     "key": "mut_rate",    "type": "float", "default": "0.10"},
		{"label": "N (Board Size)",    "key": "n",           "type": "int",   "default": "8"},
		{"label": "Seed",              "key": "seed",        "type": "int",   "default": "42"},
	],
	"ga_nsp": [
		{"label": "Population Size",   "key": "pop_size",    "type": "int",   "default": "80"},
		{"label": "Generations",       "key": "generations", "type": "int",   "default": "200"},
		{"label": "Crossover Rate",    "key": "cx_rate",     "type": "float", "default": "0.85"},
		{"label": "Mutation Rate",     "key": "mut_rate",    "type": "float", "default": "0.10"},
		{"label": "Num Nurses",        "key": "num_nurses",  "type": "int",   "default": "6"},
		{"label": "Num Days",          "key": "num_days",    "type": "int",   "default": "14"},
		{"label": "Seed",              "key": "seed",        "type": "int",   "default": "42"},
	],
	"ga_graph_coloring": [
		{"label": "Population Size",   "key": "pop_size",    "type": "int",   "default": "100"},
		{"label": "Generations",       "key": "generations", "type": "int",   "default": "200"},
		{"label": "Crossover Rate",    "key": "cx_rate",     "type": "float", "default": "0.85"},
		{"label": "Mutation Rate",     "key": "mut_rate",    "type": "float", "default": "0.10"},
		{"label": "Max Colors",        "key": "num_colors",  "type": "int",   "default": "5"},
		{"label": "Num Nodes",         "key": "num_nodes",   "type": "int",   "default": "10"},
		{"label": "Graph Type", "key": "graph_type", "type": "choice",
		 "options": ["Petersen", "Cycle", "Complete", "Random"], "default": "Petersen"},
		{"label": "Seed",              "key": "seed",        "type": "int",   "default": "42"},
	],
	"ga_feature_selection": [
		{"label": "Population Size",   "key": "pop_size",    "type": "int",   "default": "30"},
		{"label": "Generations",       "key": "generations", "type": "int",   "default": "60"},
		{"label": "Crossover Rate",    "key": "cx_rate",     "type": "float", "default": "0.80"},
		{"label": "Mutation Rate",     "key": "mut_rate",    "type": "float", "default": "0.05"},
		{"label": "Dataset", "key": "dataset", "type": "choice",
		 "options": ["Friedman (Regression)", "Iris (Classification)"], "default": "Friedman (Regression)"},
		{"label": "Model", "key": "model", "type": "choice",
		 "options": ["Logistic", "Random Forest"], "default": "Logistic"},
		{"label": "Seed",              "key": "seed",        "type": "int",   "default": "42"},
	],
}

class GAView(ctk.CTkFrame):
	def __init__(self, parent, app, **kwargs):
		super().__init__(parent, fg_color=theme.BG_MAIN, **kwargs)
		self.app = app
		self._selected_problem = "ga_function_opt"
		self._selected_category = CATEGORY_GROUPS[0][0]
		self._entries = {}

		# Header
		header = ctk.CTkFrame(self, fg_color="transparent", height=50)
		header.pack(fill="x", padx=15, pady=10)

		back_btn = ctk.CTkButton(
			header,
			text="← Back",
			font=theme.F_BODY,
			fg_color=theme.BTN_BACK,
			hover_color="#363650",
			width=80,
			command=self._on_back
		)
		back_btn.pack(side="left", padx=(0, 15))

		title_lbl = ctk.CTkLabel(
			header,
			text="Genetic Algorithm (GA) Workspace",
			font=theme.F_TITLE,
			text_color=theme.TEXT_MAIN
		)
		title_lbl.pack(side="left")

		# Body Frame (Split Left/Right)
		body_frame = ctk.CTkFrame(self, fg_color="transparent")
		body_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))

		# Left Panel - Problems container frame
		left_panel = ctk.CTkFrame(body_frame, fg_color=theme.BG_CARD, width=220)
		left_panel.pack(side="left", fill="both", expand=False, padx=(0, 10))

		# Category cards
		categories_lbl = ctk.CTkLabel(
			left_panel,
			text="Problem Categories",
			font=theme.F_HEAD,
			text_color=theme.TEXT_MAIN,
			anchor="w",
		)
		categories_lbl.pack(fill="x", padx=15, pady=(15, 8))

		self.category_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
		self.category_frame.pack(fill="x", padx=12)
		self._category_buttons = {}

		for key, label, _ in CATEGORY_GROUPS:
			btn = ctk.CTkButton(
				self.category_frame,
				text=label,
				font=theme.F_BODY,
				fg_color=theme.BG_INPUT,
				text_color=theme.TEXT_MAIN,
				hover_color="#1d273a",
				height=46,
				command=lambda k=key: self._select_category(k),
			)
			btn.pack(fill="x", pady=6)
			self._category_buttons[key] = btn

		problems_lbl = ctk.CTkLabel(
			left_panel,
			text="Problems",
			font=theme.F_HEAD,
			text_color=theme.TEXT_MAIN,
			anchor="w",
		)
		problems_lbl.pack(fill="x", padx=15, pady=(12, 6))

		self.problems_frame = ctk.CTkScrollableFrame(left_panel, fg_color="transparent")
		self.problems_frame.pack(fill="both", expand=True, padx=5, pady=(0, 10))
		self._problem_buttons = {}
		self._render_problem_list(self._selected_category)

		# Right Panel - Dynamic parameters inputs
		self.inputs_container = ctk.CTkFrame(body_frame, fg_color=theme.BG_CARD, width=540)
		self.inputs_container.pack(side="right", fill="both", expand=True)

		self.inputs_scroll = ctk.CTkScrollableFrame(self.inputs_container, fg_color="transparent")
		self.inputs_scroll.pack(fill="both", expand=True, padx=15, pady=(10, 5))

		# Run Button inside inputs container
		self.run_btn = ctk.CTkButton(
			self.inputs_container,
			text="Run Simulation",
			font=theme.F_HEAD,
			fg_color=theme.ACCENT,
			hover_color="#b53347",
			height=40,
			command=self._on_run
		)
		self.run_btn.pack(fill="x", padx=15, pady=10)

		# Bottom Row - Results
		self.result_container = ctk.CTkFrame(self, fg_color=theme.BG_CARD, height=170)
		self.result_container.pack(fill="x", padx=15, pady=(0, 15))

		self.status_lbl = ctk.CTkLabel(
			self.result_container,
			text="اختر مشكلة وابدأ التشغيل / Choose a problem and click Run",
			font=theme.F_HEAD,
			text_color=theme.TEXT_SUB
		)
		self.status_lbl.pack(anchor="w", padx=15, pady=(10, 5))

		self.result_box = ctk.CTkTextbox(
			self.result_container,
			font=theme.F_BODY,
			fg_color=theme.BG_MAIN,
			text_color=theme.TEXT_OK,
			height=110,
			state="disabled"
		)
		self.result_box.pack(fill="both", expand=True, padx=15, pady=(0, 10))

		# Render default view
		self._select_category(self._selected_category)

	def _on_back(self):
		from gui.views.home import HomeView
		self.app.show_frame(HomeView)

	def _select_problem_view(self, problem_key):
		self._selected_problem = problem_key

		# Clear previous active colors, set selected button to ACCENT
		for key, btn in self._problem_buttons.items():
			if key == problem_key:
				btn.configure(fg_color=theme.ACCENT, text_color=theme.TEXT_MAIN)
			else:
				btn.configure(fg_color="transparent", text_color=theme.TEXT_SUB)

		# Rebuild inputs
		self._build_inputs(problem_key)

		# Reset status
		self._show_result("اختر مشكلة وابدأ التشغيل / Choose a problem and click Run")

	def _select_category(self, category_key: str) -> None:
		self._selected_category = category_key
		for key, btn in self._category_buttons.items():
			if key == category_key:
				btn.configure(fg_color=theme.ACCENT, text_color=theme.TEXT_MAIN)
			else:
				btn.configure(fg_color=theme.BG_INPUT, text_color=theme.TEXT_MAIN)
		self._render_problem_list(category_key)

		problems = self._get_category_problems(category_key)
		if problems:
			self._select_problem_view(problems[0])

	def _render_problem_list(self, category_key: str) -> None:
		for w in self.problems_frame.winfo_children():
			w.destroy()
		self._problem_buttons = {}
		for key in self._get_category_problems(category_key):
			display_name = PROBLEM_DISPLAY.get(key, key)
			btn = ctk.CTkButton(
				self.problems_frame,
				text=display_name,
				font=theme.F_BODY,
				anchor="w",
				fg_color="transparent",
				text_color=theme.TEXT_SUB,
				hover_color="#1d273a",
				command=lambda k=key: self._select_problem_view(k),
			)
			btn.pack(fill="x", pady=2, padx=4)
			self._problem_buttons[key] = btn

	def _get_category_problems(self, category_key: str) -> list[str]:
		for key, _label, keys in CATEGORY_GROUPS:
			if key == category_key:
				return list(keys)
		return []

	def _build_inputs(self, problem_key):
		# Clear inputs scroll area
		for w in self.inputs_scroll.winfo_children():
			w.destroy()
		self._entries = {}

		# Problem Header
		p_title = ctk.CTkLabel(
			self.inputs_scroll,
			text=PROBLEM_DISPLAY[problem_key],
			font=theme.F_HEAD,
			text_color=theme.TEXT_MAIN
		)
		p_title.pack(anchor="w", pady=(0, 5), padx=5)

		params_def = PROBLEM_PARAMS[problem_key]
		for p in params_def:
			row = ctk.CTkFrame(self.inputs_scroll, fg_color="transparent")
			row.pack(fill="x", pady=1.5, padx=5)

			lbl = ctk.CTkLabel(row, text=p["label"], font=theme.F_BODY, text_color=theme.TEXT_SUB, width=160, anchor="w")
			lbl.pack(side="left")

			if p["type"] == "choice":
				widget = ctk.CTkOptionMenu(
					row,
					values=p["options"],
					font=theme.F_BODY,
					fg_color=theme.BG_INPUT,
					button_color=theme.BG_INPUT,
					button_hover_color="#124883",
					dropdown_fg_color=theme.BG_CARD,
					dropdown_hover_color="#1d273a",
					dropdown_text_color=theme.TEXT_MAIN,
					width=200
				)
				widget.set(p["default"])
			else:
				widget = ctk.CTkEntry(
					row,
					font=theme.F_BODY,
					fg_color=theme.BG_INPUT,
					border_color="#213a5c",
					text_color=theme.TEXT_MAIN,
					width=200
				)
				widget.insert(0, p["default"])

			widget.pack(side="left", padx=10)
			self._entries[p["key"]] = (widget, p["type"])

	def _show_result(self, text, error=False, status_msg="Ready"):
		self.status_lbl.configure(
			text=status_msg,
			text_color=theme.TEXT_ERR if error else (theme.TEXT_OK if status_msg == "Completed" else theme.TEXT_SUB)
		)
		self.result_box.configure(state="normal")
		self.result_box.delete("1.0", "end")
		self.result_box.insert("1.0", text)
		self.result_box.configure(
			state="disabled",
			text_color=theme.TEXT_ERR if error else theme.TEXT_OK
		)

	def _collect_params(self) -> dict:
		params = {}
		params_def = PROBLEM_PARAMS[self._selected_problem]

		for p in params_def:
			widget, p_type = self._entries[p["key"]]
			raw_val = widget.get().strip()

			if not raw_val:
				raise ValueError(f"المعيار '{p['label']}' لا يمكن تركه فارغاً.")

			if p_type == "int":
				try:
					params[p["key"]] = int(raw_val)
				except ValueError:
					raise ValueError(f"المعيار '{p['label']}' يجب أن يكون رقماً صحيحاً (Integer).")
			elif p_type == "float":
				try:
					params[p["key"]] = float(raw_val)
				except ValueError:
					raise ValueError(f"المعيار '{p['label']}' يجب أن يكون رقماً عشرياً (Float).")
			else:
				params[p["key"]] = raw_val
		return params

	def _on_run(self):
		try:
			params = self._collect_params()
		except ValueError as e:
			self._show_result(str(e), error=True, status_msg="خطأ في المدخلات / Input Error")
			return

		# Lock run button
		self.run_btn.configure(state="disabled", text="Running...")
		self._show_result("Executing algorithm, please wait...", status_msg="Running...")

		# Run in daemon background thread
		thread = threading.Thread(target=self._run_worker, args=(params,), daemon=True)
		thread.start()

	def _run_worker(self, params):
		try:
			# 1. Parse and extract common GA parameters
			pop_size = params.pop("pop_size", 100)
			generations = params.pop("generations", 200)
			cx_rate = params.pop("cx_rate", 0.8)
			mut_rate = params.pop("mut_rate", 0.1)

			# 2. Seed parsing with safety checks
			seed = params.pop("seed", 42)
			rng_tool = random.Random(seed)

			# 3. Construct specific parameters expected by backend solver
			solver_params = {
				"population_size": pop_size,
				"generations": generations,
				"seed": seed,
			}

			if self._selected_problem == "ga_function_opt":
				solver_params.update({
					"x_min": params["lb"],
					"x_max": params["ub"],
					"crossover_prob": cx_rate,
					"mutation_prob": mut_rate,
				})
			elif self._selected_problem == "ga_knapsack":
				num_items = params["num_items"]
				weights = [rng_tool.randint(5, 30) for _ in range(num_items)]
				values = [rng_tool.randint(10, 100) for _ in range(num_items)]
				capacity = float(params["capacity"])
				if capacity <= 0:
					capacity = float(sum(weights)) * 0.3

				solver_params.update({
					"values": values,
					"weights": weights,
					"capacity": capacity,
					"crossover_prob": cx_rate,
					"mutation_prob": mut_rate,
				})
			elif self._selected_problem == "ga_tsp":
				num_cities = params["num_cities"]
				coords = [(rng_tool.uniform(0.0, 100.0), rng_tool.uniform(0.0, 100.0)) for _ in range(num_cities)]
				solver_params.update({
					"coordinates": coords,
					"crossover_prob": cx_rate,
					"mutation_prob": mut_rate,
				})
			elif self._selected_problem == "ga_vrp":
				num_cities = params["num_cities"]
				num_vehicles = params["num_vehicles"]
				customers = {i + 1: (rng_tool.uniform(0.0, 100.0), rng_tool.uniform(0.0, 100.0)) for i in range(num_cities)}
				solver_params.update({
					"customers": customers,
					"depot": (50.0, 50.0),
					"num_vehicles": num_vehicles,
					"crossover_prob": cx_rate,
					"mutation_prob": mut_rate,
				})
			elif self._selected_problem == "ga_nqueens":
				solver_params.update({
					"n": params["n"],
					"mutation_prob": mut_rate,
				})
			elif self._selected_problem == "ga_nsp":
				# NurseSchedulingGA doesn't accept crossover_prob in its constructor
				solver_params.update({
					"num_nurses": params["num_nurses"],
					"days": params["num_days"],
					"mutation_prob": mut_rate,
				})
			elif self._selected_problem == "ga_graph_coloring":
				num_nodes = params["num_nodes"]
				num_colors = params["num_colors"]
				graph_type = params["graph_type"]

				# Programmatic graph edge generator
				if graph_type == "Cycle":
					edges = [(i, (i + 1) % num_nodes) for i in range(num_nodes)]
				elif graph_type == "Complete":
					edges = [(i, j) for i in range(num_nodes) for j in range(i + 1, num_nodes)]
				elif graph_type == "Petersen":
					num_nodes = 10
					edges = [
						(0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
						(5, 7), (7, 9), (9, 6), (6, 8), (8, 5),
						(0, 5), (1, 6), (2, 7), (3, 8), (4, 9)
					]
				else:  # Random
					edges = []
					for i in range(num_nodes):
						for j in range(i + 1, num_nodes):
							if rng_tool.random() < 0.25:
								edges.append((i, j))

				# GraphColoringGA doesn't take crossover_prob in constructor
				solver_params.update({
					"edges": edges,
					"num_nodes": num_nodes,
					"num_colors": num_colors,
					"mutation_prob": mut_rate,
				})
			elif self._selected_problem == "ga_feature_selection":
				task_type = "classification" if "Iris" in params["dataset"] else "regression"
				solver_params.update({
					"task": task_type,
					"model": params.get("model", "Logistic"),
					"mutation_prob": mut_rate,
				})

			# Map to the correct key expected by PROBLEM_ALIASES in registry.py
			prob_map = {
				"ga_function_opt": "function",
				"ga_knapsack": "knapsack",
				"ga_tsp": "tsp",
				"ga_vrp": "vrp",
				"ga_nqueens": "nqueens",
				"ga_nsp": "nsp",
				"ga_graph_coloring": "graph coloring",
				"ga_feature_selection": "feature selection",
			}
			spec = {
				"problem": prob_map.get(self._selected_problem, self._selected_problem),
				"algorithm": "GA",
				"parameters": solver_params
			}

			result = registry.run_from_spec(spec)
			self.after(0, self._on_done, result)
		except Exception as e:
			self.after(0, self._on_error, str(e))

	def _on_done(self, result):
		self.run_btn.configure(state="normal", text="Run Simulation")
		formatted = self._format_result(result)
		self._show_result(formatted, error=False, status_msg="Completed")

	def _on_error(self, err_msg):
		self.run_btn.configure(state="normal", text="Run Simulation")
		self._show_result(f"خطأ أثناء التشغيل / Runtime Error:\n{err_msg}", error=True, status_msg="Runtime Error")

	def _format_result(self, result) -> str:
		lines = []
		lines.append(f"Status                  : {result.status}")
		lines.append(f"Best Fitness Value      : {result.best_fitness:.6f}")
		lines.append(f"Execution Duration (sec): {result.execution_time_sec:.4f} seconds")

		sol = result.best_solution_phenotype
		if isinstance(sol, (list, tuple)):
			if len(sol) <= 20:
				lines.append(f"Best Solution Phenotype : {sol}")
			else:
				lines.append(f"Best Solution Phenotype : {sol[:15]} ... (+ {len(sol) - 15} more)")
		elif isinstance(sol, dict):
			lines.append(f"Best Solution Phenotype : {dict(list(sol.items())[:15])} ... (+ {len(sol) - 15} items)")
		else:
			lines.append(f"Best Solution Phenotype : {sol}")
		return "\n".join(lines)
