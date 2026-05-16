from __future__ import annotations

import os
import sys


def main() -> None:
    root_dir = os.path.dirname(__file__)
    src_path = os.path.join(root_dir, "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    from core.cli import main as run_cli

    run_cli()


if __name__ == "__main__":
    main()
