import sys
from PyQt6.QtWidgets import QApplication

from core import TLPSolver, VogelsMethod, PotentialMethod

from view.app_window import TLPSolverApp
from view import InputSection, ResultSection


def main():
    app = QApplication(sys.argv)

    solver = TLPSolver(
        bfs_finder=VogelsMethod(),
        algorithm=PotentialMethod()
    )
    window = TLPSolverApp(
        input_section=InputSection(),
        results_section=ResultSection(),
        solver=solver
    )
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()