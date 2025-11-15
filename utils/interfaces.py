from abc import ABC, abstractmethod
from utils.containers import TLPProblem, BFSolution, TLPResult


class IBFSFinder(ABC):
    """Class-interface for finding initial basic feasible solutions (BFS) for transportation problems."""
    @abstractmethod
    def find_initial_bfs(self, problem: TLPProblem) -> BFSolution:
        """
        Computes an initial basic feasible solution for transportation problems.
        Args:
            problem (TLPProblem): The transportation problem
        Returns:
            BFSolution: Basic feasible solution
        """
        pass


class ITransportationAlgorithm(ABC):
    """
    Class-interface for transportation algorithms that's 
    used for solving transportation problem
    """
    @abstractmethod
    def solve_from_bfs(self, problem: TLPProblem, initial_solution: BFSolution) -> TLPResult:
        """
        Solve transportation problem starting from initial basic feasible solution.
        Args:
            problem (TLPProblem): The transportation problem in to solve
            initial_solution (BFSolution): Initial basic feasible solution containing
        Returns:
            TLPResult: The solution containing optimal value and solution
        """
        pass