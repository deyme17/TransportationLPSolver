from utils.interfaces import IBFSFinder
from utils import TLPProblem, BFSolution
import numpy as np

class VogelsMethod(IBFSFinder):
    """Vogel's Approximation Method (VAM)"""
    EPSILON=1e-10
    def find_initial_bfs(self, problem: TLPProblem):
        """
        Computes an initial basic feasible solution for transportation problems
        using Vogel's Approximation Method (VAM)
        Args:
            problem (TLPProblem): The transportation problem
        Returns:
            BFSolution: Basic feasible solution
        """
        supply = problem.supply.copy()
        demand = problem.demand.copy()
        costs = np.array(problem.costs, dtype=float)
        
        m, n = costs.shape
        allocation = np.zeros((m, n), dtype=float)
        basis = []
        
        active_rows = set(range(m))
        active_cols = set(range(n))
        
        while active_rows and active_cols:
            # calc penalties
            row_penalties = self._calculate_row_penalties(costs, active_rows, active_cols)
            col_penalties = self._calculate_col_penalties(costs, active_rows, active_cols)
            
            # find maximum penalty
            max_row_penalty = max(row_penalties.values()) if row_penalties else -1
            max_col_penalty = max(col_penalties.values()) if col_penalties else -1
            
            if max_row_penalty == -1 and max_col_penalty == -1:
                break
            
            # select cell
            if max_row_penalty >= max_col_penalty:
                i = max(row_penalties.keys(), key=lambda k: row_penalties[k])
                j = min(active_cols, key=lambda j: costs[i, j])
            else:
                j = max(col_penalties.keys(), key=lambda k: col_penalties[k])
                i = min(active_rows, key=lambda i: costs[i, j])
            
            # allocate
            amount = min(supply[i], demand[j])
            allocation[i, j] = amount
            basis.append((i, j))
            
            # update supply and demand
            supply[i] -= amount
            demand[j] -= amount
            
            # remove exhausted row or column
            if supply[i] < self.EPSILON:
                active_rows.discard(i)
            if demand[j] < self.EPSILON:
                active_cols.discard(j)
        
        total_cost = sum(
            allocation[i, j] * problem.costs[i][j]
            for i, j in basis
        )
        return BFSolution(
            allocation=allocation.tolist(),
            basis=basis,
            cost=total_cost
        )

    def _calculate_row_penalties(self, costs: np.ndarray, active_rows: set, active_cols: set):
        penalties = {}
        for i in active_rows:
            row_costs = [costs[i, j] for j in active_cols]
            if len(row_costs) >= 2:
                smallest = np.partition(row_costs, 1)[:2]
                penalties[i] = smallest[1] - smallest[0]
            elif len(row_costs) == 1:
                penalties[i] = row_costs[0]
        return penalties

    def _calculate_col_penalties(self, costs: np.ndarray, active_rows: set, active_cols: set):
        penalties = {}
        for j in active_cols:
            col_costs = [costs[i, j] for i in active_rows]
            if len(col_costs) >= 2:
                smallest = np.partition(col_costs, 1)[:2]
                penalties[j] = smallest[1] - smallest[0]
            elif len(col_costs) == 1:
                penalties[j] = col_costs[0]
        return penalties