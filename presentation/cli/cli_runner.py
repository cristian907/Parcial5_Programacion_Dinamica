"""CLI entrypoint for presentation/cli/cli_runner.py."""
import os
import sys

# Ensure root directory is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.presentation.cli.cli_runner import run_cli

if __name__ == "__main__":
    export_file = sys.argv[1] if len(sys.argv) > 1 else "reporte_problema.txt"
    run_cli(export_file)
