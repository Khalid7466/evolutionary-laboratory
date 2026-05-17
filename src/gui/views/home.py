import customtkinter as ctk
from gui import theme

class HomeView(ctk.CTkFrame):
	def __init__(self, parent, app, **kwargs):
		super().__init__(parent, fg_color=theme.BG_MAIN, **kwargs)
		self.app = app

		# Main Title
		title_lbl = ctk.CTkLabel(
			self,
			text="EvoLab",
			font=theme.F_TITLE,
			text_color=theme.TEXT_MAIN
		)
		title_lbl.pack(pady=(120, 10))

		# Subtitle
		sub_lbl = ctk.CTkLabel(
			self,
			text="اختر نوع الخوارزمية للبدء / Select Algorithm to Begin",
			font=theme.F_BODY,
			text_color=theme.TEXT_SUB
		)
		sub_lbl.pack(pady=(0, 50))

		# Button container
		btn_frame = ctk.CTkFrame(self, fg_color="transparent")
		btn_frame.pack()

		# GA Button
		ga_btn = ctk.CTkButton(
			btn_frame,
			text="Genetic Algorithm (GA)",
			font=theme.F_HEAD,
			fg_color=theme.BTN_GA,
			hover_color="#144d6e",
			width=300,
			height=60,
			command=self._on_ga_click
		)
		ga_btn.pack(pady=15)

		# PSO Button
		pso_btn = ctk.CTkButton(
			btn_frame,
			text="Particle Swarm Optimization (PSO)",
			font=theme.F_HEAD,
			fg_color=theme.BTN_PSO,
			hover_color="#1d4533",
			width=300,
			height=60,
			command=self._on_pso_click
		)
		pso_btn.pack(pady=15)

	def _on_ga_click(self):
		from gui.views.ga_view import GAView
		self.app.show_frame(GAView)

	def _on_pso_click(self):
		from gui.views.pso_view import PSOView
		self.app.show_frame(PSOView)
