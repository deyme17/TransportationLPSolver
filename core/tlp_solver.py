from utils.interfaces import IBFSFinder, ITransportationAlgorithm
from utils import (
    TLPProblem, TLPResult, SolutionStatus
)

class TLPSolver:
    """A tamplate for solving transportation LP problems."""
    def __init__(self, bfs_finder: IBFSFinder, algorithm: ITransportationAlgorithm) -> None:
        """
        Args:
            bfs_finder: Component for finding basic feasible solutions
            algorithm: Transportation algorithm implementation for optimization
        """
        self.bfs_finder = bfs_finder
        self.algorithm = algorithm

    def solve(self, problem: TLPProblem) -> TLPResult:
        """
        Solve a transportation linear programming problem.
        Args:
            problem (TLPProblem): The transportation LP problem to solve
        Returns:
            TLPResult: The solution containing optimal value and cost matrix
        """
        try:
            if not problem.is_balanced():
                problem = self._balance_problem(problem)
            # initial basic feasible solution
            initial_solution = self.bfs_finder.find_initial_bfs(problem)
            if not initial_solution:
                return TLPResult(
                    status=SolutionStatus.INFEASIBLE.value,
                    error_message="No initial BFS found"
                )
            # optimize
            final_result = self.algorithm.solve_from_bfs(problem, initial_solution)
            return final_result
        except Exception as e:
            return TLPResult(
                status=SolutionStatus.ERROR.value,
                error_message=f"Solver error: {str(e)}"
            )
        
    def _balance_problem(self, problem: TLPProblem) -> TLPProblem:
        """
        Balance transportation LP problem
        Args:
            problem (TLPProblem): The transportation LP problem
        Returns:
            TLPProblem: Balanced transportation LP problem
        """
        total_supply = problem.total_supply
        total_demand = problem.total_demand
        
        if total_supply > total_demand:
            # dummy consumer
            deficit = total_supply - total_demand
            new_demand = problem.demand + [deficit]
            new_costs = [row + [0.0] for row in problem.costs]
            return TLPProblem(
                supply=problem.supply.copy(),
                demand=new_demand,
                costs=new_costs
            )
        else:
            # dummy supplier
            deficit = total_demand - total_supply
            new_supply = problem.supply + [deficit]
            new_costs = problem.costs + [[0.0] * problem.num_consumers]
            return TLPProblem(
                supply=new_supply,
                demand=problem.demand.copy(),
                costs=new_costs
            )