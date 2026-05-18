import customtkinter as ctk
from gui import theme
from gui.views.home import HomeView

class EvoLabApp(ctk.CTk):
	def __init__(self) -> None:
		super().__init__()
		
		# High-DPI Windows Scaling Safety Net
		try:
			self.tk.call('tk', 'scaling', 1.0)
		except Exception:
			pass

		self.title("EvoLab")
		screen_w = self.winfo_screenwidth()
		screen_h = self.winfo_screenheight()
		win_w = int(screen_w * 0.95)
		win_h = int(screen_h * 0.92)
		self.geometry(f"{win_w}x{win_h}")
		self.resizable(True, True)
		self.configure(fg_color=theme.BG_MAIN)

		self._current_frame = None
		self.show_frame(HomeView)

	def show_frame(self, FrameClass, **kwargs) -> None:
		# Destroy the active frame entirely to prevent memory leaks and maintain absolute stability
		if self._current_frame is not None:
			self._current_frame.destroy()

		self._current_frame = FrameClass(self, app=self, **kwargs)
		self._current_frame.pack(fill="both", expand=True)
