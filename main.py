"""Root entrypoint for Parcial V Dynamic Programming project.

Execution:
    python3 main.py         -> Inicia la interfaz gráfica de escritorio (PyQt6)
    python3 main.py --cli   -> Ejecuta el modo consola y genera reporte_problema.txt
"""
import sys
import os

# Ensure project root is in Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    if "--cli" in sys.argv:
        from src.presentation.cli.cli_runner import run_cli
        run_cli("reporte_problema.txt")
    else:
        from src.presentation.gui.main_window import run_gui
        run_gui()


if __name__ == "__main__":
    main()
