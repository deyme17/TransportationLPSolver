import numpy as np
from typing import List, Tuple, Set, Optional
from utils.interfaces import ITransportationAlgorithm
from utils import TLPProblem, TLPResult, BFSolution, SolutionStatus


class PotentialMethod(ITransportationAlgorithm):
    """Method of Potentials or MODI (Modified Distribution) Method using NumPy"""
    def __init__(self, max_iterations: int = 1000):
        self.max_iterations = max_iterations
        self.EPSILON = 1e-10
    
    def solve_from_bfs(self, problem: TLPProblem, initial_solution: BFSolution) -> TLPResult:
        """
        Solve transportation problem starting from initial basic feasible solution.
        Args:
            problem: The transportation problem to solve
            initial_solution: Initial basic feasible solution
        Returns:
            TLPResult: The result containing optimal value and solution
        """
        try:
            allocation = np.array(initial_solution.allocation, dtype=float)
            basis = set(initial_solution.basis)
            costs = np.array(problem.costs, dtype=float)
            m, n = allocation.shape

            for _ in range(self.max_iterations):
                # calc potentials
                u, v = self._calculate_potentials(costs, basis, m, n)
                # calc reduced costs
                deltas = costs - u[:, None] - v[None, :]
                
                non_basic_mask = np.array([
                    [(i, j) not in basis for j in range(n)] 
                    for i in range(m)
                ])
                deltas_masked = np.where(non_basic_mask, deltas, np.inf)
                
                # optimal condition
                min_delta = np.min(deltas_masked)
                if min_delta >= -self.EPSILON:
                    total_cost = float(np.sum(allocation * costs))
                    return TLPResult(
                        status=SolutionStatus.OPTIMAL.value,
                        optimal_value=total_cost,
                        solution=allocation.tolist()
                    )
                
                entering_cell = tuple(np.unravel_index(
                    np.argmin(deltas_masked), 
                    deltas_masked.shape
                ))
                # cycle
                cycle = self._find_cycle(entering_cell, basis, m, n)
                if not cycle:
                    return TLPResult(
                        status=SolutionStatus.ERROR.value,
                        error_message="Could not find cycle for improvement"
                    )
                # update solution
                allocation, basis = self._update_solution(allocation, basis, cycle)

            # max iterations reached
            return TLPResult(
                status=SolutionStatus.ERROR.value,
                error_message=f"Max iterations ({self.max_iterations}) reached"
            )
        except Exception as e:
            return TLPResult(
                status=SolutionStatus.ERROR.value,
                error_message=f"Error in MODI method: {str(e)}"
            )

    def _calculate_potentials(self, costs: np.ndarray, basis: Set[Tuple[int, int]], 
                              m: int, n: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate potentials u_i and v_j for basic variables.
        For basic cells: u_i + v_j = c_ij
        Args:
            costs: Cost matrix of shape (m, n)
            basis: Set of basic variables (i, j)
            m: Number of suppliers
            n: Number of consumers
        Returns:
            Tuple of (u, v) where u[i] and v[j] are potentials
        """
        u = np.full(m, np.nan, dtype=float)
        v = np.full(n, np.nan, dtype=float)

        u[0] = 0.0 # basis solution

        updated = True
        max_iter = m + n
        iter_count = 0
        
        while updated and iter_count < max_iter:
            updated = False
            iter_count += 1
            
            for i, j in basis:
                if np.isnan(u[i]) and not np.isnan(v[j]):
                    u[i] = costs[i, j] - v[j]
                    updated = True
                elif np.isnan(v[j]) and not np.isnan(u[i]):
                    v[j] = costs[i, j] - u[i]
                    updated = True

        return u, v

    def _find_cycle(self, entering_cell: Tuple[int, int], basis: Set[Tuple[int, int]], 
                    m: int, n: int) -> Optional[List[Tuple[int, int]]]:
        """
        Find closed cycle starting and ending at entering cell.
        Cycle alternates between horizontal and vertical moves.
        Args:
            entering_cell: Cell to enter basis (i, j)
            basis: Current basic variables
            m: Number of suppliers
            n: Number of consumers
        Returns:
            List of cells in cycle, or None if not found
        """
        def dfs(curr: Tuple[int, int], target: Tuple[int, int], path: List[Tuple[int, int]], 
            visited: Set[Tuple[int, int]], is_row: bool) -> Optional[List[Tuple[int, int]]]:
            """DFS to find cycle"""
            if len(path) >= 4:
                i, j = curr
                if is_row:
                    if i == target[0] and target[1] in rows_cells.get(i, []):
                        return path
                else:
                    if j == target[1] and target[0] in cols_cells.get(j, []):
                        return path
            
            if curr in visited:
                return None
            if len(path) > 2 * (m + n):
                return None

            visited.add(curr)
            i, j = curr
            
            if is_row:
                for next_j in rows_cells.get(i, []):
                    if next_j == j:
                        continue
                    next_cell = (i, next_j)
                    new_path = path + [next_cell]
                    result = dfs(next_cell, target, new_path, visited.copy(), False)
                    if result:
                        return result
            else:
                for next_i in cols_cells.get(j, []):
                    if next_i == i:
                        continue
                    next_cell = (next_i, j)
                    new_path = path + [next_cell]
                    result = dfs(next_cell, target, new_path, visited.copy(), True)
                    if result:
                        return result
            
            return None

        i0, j0 = entering_cell
        
        # adj lists
        rows_cells = {i: [] for i in range(m)}
        cols_cells = {j: [] for j in range(n)}

        for i, j in basis:
            rows_cells[i].append(j)
            cols_cells[j].append(i)

        rows_cells[i0].append(j0)
        cols_cells[j0].append(i0)

        cycle = dfs(entering_cell, entering_cell, [entering_cell], set(), True)
        if cycle: # close a cycle
            cycle.append(entering_cell)
        
        return cycle

    def _update_solution(self, allocation: np.ndarray, basis: Set[Tuple[int, int]], 
                         cycle: List[Tuple[int, int]]) -> Tuple[np.ndarray, Set[Tuple[int, int]]]:
        """
        Update allocation along the cycle.
        Add to '+' cells (even positions), subtract from '-' cells (odd positions).
        Args:
            allocation: Current allocation matrix
            basis: Current basic variables
            cycle: Cycle of cells (starting with entering cell)
        Returns:
            Updated (allocation, basis)
        """
        if len(cycle) > 1 and cycle[0] == cycle[-1]:
            cycle = cycle[:-1]
        
        # add indicies of '-'
        minus_positions = cycle[1::2]

        # min allocation at '-' cells
        theta = min(allocation[i, j] for i, j in minus_positions)
        if theta < self.EPSILON:
            positive_values = [allocation[i, j] for i, j in minus_positions 
                             if allocation[i, j] > self.EPSILON]
            theta = min(positive_values) if positive_values else self.EPSILON

        for idx, (i, j) in enumerate(cycle):
            if idx % 2 == 0:    # '+' cells
                allocation[i, j] += theta
            else:               # '-' cells
                allocation[i, j] -= theta

        # leaving cell
        leaving_cell = None
        for i, j in minus_positions:
            if allocation[i, j] < self.EPSILON:
                leaving_cell = (i, j)
                allocation[i, j] = 0
                break

        # update basis
        new_basis = basis.copy()
        if leaving_cell:
            new_basis.remove(leaving_cell)
        new_basis.add(cycle[0])  # entering cell

        return allocation, new_basis