from __future__ import annotations

import os
import sys

def main() -> None:
	# If arguments are passed, run the CLI. Otherwise, start the GUI!
	if len(sys.argv) > 1:
		from core.cli import main as run_cli
		run_cli()
	else:
		from gui.app import EvoLabApp
		app = EvoLabApp()
		app.mainloop()

if __name__ == "__main__":
	main()
