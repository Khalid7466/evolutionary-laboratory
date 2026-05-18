import customtkinter as ctk
import threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from gui import theme
from core import registry

PSO_PARAMS = [
	{"label": "Swarm Size",      "key": "swarm_size",  "type": "int",   "default": "50"},
	{"label": "Iterations",      "key": "iterations",  "type": "int",   "default": "200"},
	{"label": "Inertia (w)",     "key": "w",           "type": "float", "default": "0.72"},
	{"label": "Cognitive (c1)",  "key": "c1",          "type": "float", "default": "1.49"},
	{"label": "Social (c2)",     "key": "c2",          "type": "float", "default": "1.49"},
	{"label": "Function", "key": "function", "type": "choice",
	 "options": ["Ackley", "Rastrigin", "Rosenbrock", "Sphere"], "default": "Ackley"},
	{"label": "Dimensions",      "key": "dimensions",  "type": "int",   "default": "10"},
	{"label": "Lower Bound",     "key": "lb",          "type": "float", "default": "-5.12"},
	{"label": "Upper Bound",     "key": "ub",          "type": "float", "default": "5.12"},
	{"label": "Seed",            "key": "seed",        "type": "int",   "default": "42"},
]

class PSOView(ctk.CTkFrame):
	def __init__(self, parent, app, **kwargs):
		super().__init__(parent, fg_color=theme.BG_MAIN, **kwargs)
		self.app = app
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
			text="PSO — Function Optimization",
			font=theme.F_TITLE,
			text_color=theme.TEXT_MAIN
		)
		title_lbl.pack(side="left")

		# Main container
		body_frame = ctk.CTkFrame(self, fg_color="transparent")
		body_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))

		top_row = ctk.CTkFrame(body_frame, fg_color="transparent", height=300)
		top_row.pack(fill="x", pady=(0, 10))
		top_row.pack_propagate(False)

		# Parameters inputs Panel (left)
		self.inputs_container = ctk.CTkFrame(top_row, fg_color=theme.BG_CARD)
		self.inputs_container.pack(side="left", fill="both", expand=True, padx=(0, 10))

		self.inputs_scroll = ctk.CTkScrollableFrame(self.inputs_container, fg_color="transparent")
		self.inputs_scroll.pack(fill="both", expand=True, padx=15, pady=(10, 5))

		self._build_inputs()

		# Run Button at the bottom of inputs panel
		self.run_btn = ctk.CTkButton(
			self.inputs_container,
			text="Run PSO Simulation",
			font=theme.F_HEAD,
			fg_color=theme.ACCENT,
			hover_color="#b53347",
			height=40,
			command=self._on_run
		)
		self.run_btn.pack(fill="x", padx=15, pady=10)

		# Results Panel (right)
		self.result_container = ctk.CTkFrame(top_row, fg_color=theme.BG_CARD, width=320)
		self.result_container.pack(side="right", fill="both", expand=False)
		self.result_container.pack_propagate(False)

		self.status_lbl = ctk.CTkLabel(
			self.result_container,
			text="اضغط Run للتشغيل / Click Run to start PSO optimization",
			font=theme.F_HEAD,
			text_color=theme.TEXT_SUB
		)
		self.status_lbl.pack(anchor="w", padx=15, pady=(10, 5))

		self.result_box = ctk.CTkTextbox(
			self.result_container,
			font=theme.F_BODY,
			fg_color=theme.BG_MAIN,
			text_color=theme.TEXT_OK,
			state="disabled"
		)
		self.result_box.pack(fill="both", expand=True, padx=15, pady=(0, 10))

		# Fitness chart
		self.chart_container = ctk.CTkFrame(body_frame, fg_color=theme.BG_CARD)
		self.chart_container.pack(fill="both", expand=True, pady=(0, 10))
		self._init_chart()

	def _on_back(self):
		from gui.views.home import HomeView
		self.app.show_frame(HomeView)

	def _build_inputs(self):
		for p in PSO_PARAMS:
			row = ctk.CTkFrame(self.inputs_scroll, fg_color="transparent")
			row.pack(fill="x", pady=1.5, padx=5)

			lbl = ctk.CTkLabel(row, text=p["label"], font=theme.F_BODY, text_color=theme.TEXT_SUB, width=200, anchor="w")
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
					width=250
				)
				widget.set(p["default"])
			else:
				widget = ctk.CTkEntry(
					row,
					font=theme.F_BODY,
					fg_color=theme.BG_INPUT,
					border_color="#213a5c",
					text_color=theme.TEXT_MAIN,
					width=250
				)
				widget.insert(0, p["default"])

			widget.pack(side="left", padx=10)
			self._entries[p["key"]] = (widget, p["type"])

	def _collect_params(self) -> dict:
		params = {}
		for p in PSO_PARAMS:
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
		self._show_result("Executing PSO simulation, please wait...", status_msg="Running...")
		self._reset_chart()

		# Run in background daemon thread
		thread = threading.Thread(target=self._run_worker, args=(params,), daemon=True)
		thread.start()

	def _run_worker(self, params):
		try:
			# Map to solver parameter names for FunctionOptimizationPSO constructor
			solver_params = {
				"dimensions": params["dimensions"],
				"swarm_size": params["swarm_size"],
				"iterations": params["iterations"],
				"bounds": (params["lb"], params["ub"]),
				"inertia": params["w"],
				"cognitive": params["c1"],
				"social": params["c2"],
				"seed": params["seed"],
			}

			spec = {
				"problem": "function",
				"algorithm": "PSO",
				"parameters": solver_params
			}

			def callback(iteration, _best_position, best_fitness, _swarm):
				value = float(best_fitness) if best_fitness is not None else 0.0
				self.after(0, self._append_chart_point, iteration + 1, value)

			result = registry.run_from_spec(spec, callback=callback)
			self.after(0, self._on_done, result)
		except Exception as e:
			self.after(0, self._on_error, str(e))

	def _init_chart(self) -> None:
		self._chart_x = []
		self._chart_y = []
		self.chart_fig = Figure(figsize=(6.5, 3.0), dpi=100)
		self.chart_fig.patch.set_facecolor(theme.BG_CARD)
		self.chart_ax = self.chart_fig.add_subplot(111)
		self.chart_fig.subplots_adjust(left=0.08, right=0.995, top=0.92, bottom=0.18)
		self.chart_ax.set_facecolor(theme.BG_CARD)
		self.chart_ax.tick_params(colors=theme.TEXT_SUB)
		for spine in self.chart_ax.spines.values():
			spine.set_color(theme.BG_INPUT)
		self.chart_ax.set_title("Fitness vs Iteration", color=theme.TEXT_MAIN, fontsize=10)
		self.chart_ax.set_xlabel("Iteration", color=theme.TEXT_SUB)
		self.chart_ax.set_ylabel("Fitness", color=theme.TEXT_SUB)
		self.chart_ax.grid(True, alpha=0.3)
		self.chart_line, = self.chart_ax.plot([], [], color=theme.TEXT_OK, linewidth=2)
		self.chart_canvas = FigureCanvasTkAgg(self.chart_fig, master=self.chart_container)
		canvas_widget = self.chart_canvas.get_tk_widget()
		canvas_widget.configure(bg=theme.BG_CARD, highlightthickness=0)
		canvas_widget.pack(fill="both", expand=True, padx=0, pady=0)
		self.chart_container.bind("<Configure>", self._on_chart_resize)
		self.after(50, self._on_chart_resize)

	def _on_chart_resize(self, _event=None) -> None:
		self.chart_container.update_idletasks()
		width = self.chart_container.winfo_width()
		height = self.chart_container.winfo_height()
		if width <= 1 or height <= 1:
			self.after(50, self._on_chart_resize)
			return
		self.chart_canvas.get_tk_widget().configure(width=width, height=height)
		self.chart_fig.set_size_inches(
			width / self.chart_fig.dpi,
			height / self.chart_fig.dpi,
			forward=True
		)
		self.chart_canvas.draw_idle()

	def _reset_chart(self) -> None:
		self._chart_x = []
		self._chart_y = []
		self.chart_line.set_data([], [])
		self.chart_ax.set_xlim(0, 1)
		self.chart_ax.set_ylim(0, 1)
		self.chart_canvas.draw_idle()

	def _append_chart_point(self, iteration: int, fitness: float) -> None:
		self._chart_x.append(iteration)
		self._chart_y.append(fitness)
		self.chart_line.set_data(self._chart_x, self._chart_y)
		self.chart_ax.set_xlim(1, max(2, len(self._chart_x)))
		min_v = min(self._chart_y)
		max_v = max(self._chart_y)
		pad = (max_v - min_v) * 0.1 if max_v != min_v else 1.0
		self.chart_ax.set_ylim(min_v - pad, max_v + pad)
		self.chart_canvas.draw_idle()

	def _on_done(self, result):
		self.run_btn.configure(state="normal", text="Run PSO Simulation")
		formatted = self._format_result(result)
		self._show_result(formatted, error=False, status_msg="Completed")

	def _on_error(self, err_msg):
		self.run_btn.configure(state="normal", text="Run PSO Simulation")
		self._show_result(f"خطأ أثناء التشغيل / Runtime Error:\n{err_msg}", error=True, status_msg="Runtime Error")

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

	def _format_result(self, result) -> str:
		lines = []
		lines.append(f"Status                  : {result.status}")
		lines.append(f"Best Cost Value         : {result.best_fitness:.6f}")
		lines.append(f"Execution Duration (sec): {result.execution_time_sec:.4f} seconds")

		sol = result.best_solution_phenotype
		if isinstance(sol, (list, tuple)):
			lines.append("Best Particle Position  :")
			lines.append(f"{list(sol)}")
		else:
			lines.append(f"Best Particle Position  : {sol}")
		return "\n".join(lines)
