import unittest
import numpy as np
from core.potential_method import PotentialMethod
from utils import TLPProblem, BFSolution, SolutionStatus


class TestPotentialMethod(unittest.TestCase):
    """Unit tests for PotentialMethod (MODI) algorithm"""
    def setUp(self):
        """Set up test fixtures"""
        self.method = PotentialMethod(max_iterations=1000)
    
    def test_simple_optimal_solution(self):
        """Test with simple 2x2 problem that's already optimal"""
        problem = TLPProblem(
            supply=[20, 30],
            demand=[25, 25],
            costs=[
                [2, 3],
                [4, 1]
            ]
        )
        # initial BFS (already optimal)
        initial_bfs = BFSolution(
            allocation=[
                [20.0, 0.0],
                [5.0, 25.0]
            ],
            basis=[(0, 0), (1, 0), (1, 1)],
            cost=20*2 + 5*4 + 25*1
        )
        result = self.method.solve_from_bfs(problem, initial_bfs)
        
        self.assertEqual(result.status, SolutionStatus.OPTIMAL.value)
        self.assertIsNotNone(result.optimal_value)
        self.assertIsNotNone(result.solution)
        self.assertAlmostEqual(result.optimal_value, 85.0, places=5)
    
    def test_requires_optimization(self):
        """Test problem that requires optimization iterations"""
        problem = TLPProblem(
            supply=[30, 40, 50],
            demand=[35, 28, 57],
            costs=[
                [8, 6, 10],
                [9, 12, 13],
                [14, 9, 16]
            ]
        )
        # suboptimal initial solution
        initial_bfs = BFSolution(
            allocation=[
                [30.0, 0.0, 0.0],
                [5.0, 28.0, 7.0],
                [0.0, 0.0, 50.0]
            ],
            basis=[(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)],
            cost=30*8 + 5*9 + 28*12 + 7*13 + 50*16
        )
        result = self.method.solve_from_bfs(problem, initial_bfs)
        
        self.assertEqual(result.status, SolutionStatus.OPTIMAL.value)
        self.assertIsNotNone(result.optimal_value)
        # verify solution maintains supply/demand
        solution = np.array(result.solution)
        np.testing.assert_allclose(solution.sum(axis=1), problem.supply, rtol=1e-5)
        np.testing.assert_allclose(solution.sum(axis=0), problem.demand, rtol=1e-5)
    
    def test_calculate_potentials(self):
        """Test potential calculation for basic variables"""
        costs = np.array([
            [2, 3, 4],
            [5, 1, 6]
        ])
        basis = {(0, 0), (0, 1), (1, 1)}
        m, n = 2, 3
        
        u, v = self.method._calculate_potentials(costs, basis, m, n)
        
        # check that u_i + v_j = c_ij for all basic cells
        for i, j in basis:
            self.assertAlmostEqual(u[i] + v[j], costs[i, j], places=5)
        
        # u[0] should be 0 (initial assignment)
        self.assertAlmostEqual(u[0], 0.0, places=5)
    
    def test_find_cycle_simple(self):
        """Test cycle finding with simple configuration"""
        basis = {(0, 0), (0, 2), (1, 1), (1, 2)}
        entering_cell = (0, 1)
        m, n = 2, 3
        
        cycle = self.method._find_cycle(entering_cell, basis, m, n)
        
        self.assertIsNotNone(cycle)
        self.assertGreaterEqual(len(cycle), 4)
        self.assertEqual(cycle[0], entering_cell)
        self.assertEqual(cycle[-1], entering_cell)  # should return to start
        # should alternate between row/column moves
        for i in range(len(cycle) - 1):
            curr = cycle[i]
            next_cell = cycle[i + 1]
            # either row or column should match, not both
            same_row = curr[0] == next_cell[0]
            same_col = curr[1] == next_cell[1]
            self.assertTrue(same_row != same_col)
    
    def test_find_cycle_no_cycle(self):
        """Test cycle finding when no valid cycle exists"""
        # invalid basis configuration
        basis = {(0, 0), (1, 1)}
        entering_cell = (0, 1)
        m, n = 2, 2
        
        cycle = self.method._find_cycle(entering_cell, basis, m, n)
        
        # return None or empty list
        self.assertIsNone(cycle)
    
    def test_update_solution(self):
        """Test solution update along cycle"""
        allocation = np.array([
            [10.0, 0.0, 20.0],
            [0.0, 15.0, 5.0]
        ])
        basis = {(0, 0), (0, 2), (1, 1), (1, 2)}
        cycle = [(0, 1), (0, 2), (1, 2), (1, 1)]  # cycle
        
        new_allocation, new_basis = self.method._update_solution(
            allocation, basis, cycle
        )
        # check that allocation is still valid
        self.assertTrue(np.all(new_allocation >= -self.method.EPSILON))
        # check basis size
        self.assertEqual(len(new_basis), len(basis))
        # entering cell should be in new basis
        self.assertIn(cycle[0], new_basis)
    
    def test_degenerate_case(self):
        """Test handling of degenerate solution"""
        problem = TLPProblem(
            supply=[10, 10],
            demand=[10, 10],
            costs=[
                [1, 2],
                [3, 4]
            ]
        )
        # degenerate initial solution
        initial_bfs = BFSolution(
            allocation=[
                [10.0, 0.0],
                [0.0, 10.0]
            ],
            basis=[(0, 0), (1, 1), (0, 1)],  # m+n-1 = 3
            cost=10*1 + 10*4
        )
        
        result = self.method.solve_from_bfs(problem, initial_bfs)
        
        self.assertEqual(result.status, SolutionStatus.OPTIMAL.value)
        self.assertIsNotNone(result.optimal_value)
    
    def test_max_iterations_exceeded(self):
        """Test that max iterations limit works"""
        method = PotentialMethod(max_iterations=1)  # low limit
        
        problem = TLPProblem(
            supply=[100, 100],
            demand=[100, 100],
            costs=[
                [5, 10],
                [8, 6]
            ]
        )
        
        # non-optimal initial solution
        initial_bfs = BFSolution(
            allocation=[
                [0.0, 100.0],
                [100.0, 0.0]
            ],
            basis=[(0, 1), (1, 0), (1, 1)],
            cost=100*10 + 100*8
        )
        
        result = method.solve_from_bfs(problem, initial_bfs)
        
        self.assertEqual(result.status, SolutionStatus.ERROR.value)
        self.assertIn("Max iterations", result.error_message)
    
    def test_invalid_basis(self):
        """Test handling of invalid basis"""
        problem = TLPProblem(
            supply=[20, 30],
            demand=[25, 25],
            costs=[
                [2, 3],
                [4, 1]
            ]
        )
        # invalid basis (disconnected)
        initial_bfs = BFSolution(
            allocation=[
                [20.0, 0.0],
                [5.0, 25.0]
            ],
            basis=[(0, 0), (1, 1)],  # 2 cells, need 3
            cost=20*2 + 5*4 + 25*1
        )
        result = self.method.solve_from_bfs(problem, initial_bfs)
        
        # should either handle gracefully or return error
        self.assertIn(result.status, [
            SolutionStatus.ERROR.value, 
            SolutionStatus.OPTIMAL.value
        ])
    
    def test_large_problem(self):
        """Test with larger problem size"""
        m, n = 5, 6
        problem = TLPProblem(
            supply=[50] * m,
            demand=[40, 45, 35, 50, 55, 25],
            costs=[[np.random.randint(1, 20) for _ in range(n)] for _ in range(m)]
        )
        # create valid initial BFS
        allocation = np.zeros((m, n))
        basis = []
        supply_left = problem.supply.copy()
        demand_left = problem.demand.copy()
        
        for i in range(m):
            for j in range(n):
                if supply_left[i] > 0 and demand_left[j] > 0:
                    amount = min(supply_left[i], demand_left[j])
                    allocation[i, j] = amount
                    basis.append((i, j))
                    supply_left[i] -= amount
                    demand_left[j] -= amount
        
        initial_bfs = BFSolution(
            allocation=allocation.tolist(),
            basis=basis,
            cost=float(np.sum(allocation * np.array(problem.costs)))
        )
        result = self.method.solve_from_bfs(problem, initial_bfs)
        
        self.assertEqual(result.status, SolutionStatus.OPTIMAL.value)
        self.assertIsNotNone(result.optimal_value)
    
    def test_zero_costs(self):
        """Test with some zero costs"""
        problem = TLPProblem(
            supply=[15, 25],
            demand=[20, 20],
            costs=[
                [0, 5],
                [3, 0]
            ]
        )
        initial_bfs = BFSolution(
            allocation=[
                [15.0, 0.0],
                [5.0, 20.0]
            ],
            basis=[(0, 0), (1, 0), (1, 1)],
            cost=15*0 + 5*3 + 20*0
        )
        result = self.method.solve_from_bfs(problem, initial_bfs)
        
        self.assertEqual(result.status, SolutionStatus.OPTIMAL.value)
        # optimal should be 0 or very low
        self.assertLessEqual(result.optimal_value, 20)
    
    def test_solution_maintains_constraints(self):
        """Test that final solution maintains supply/demand constraints"""
        problem = TLPProblem(
            supply=[100, 150, 200],
            demand=[120, 180, 150],
            costs=[
                [5, 8, 7],
                [6, 9, 4],
                [8, 5, 6]
            ]
        )
        # any valid initial BFS
        initial_bfs = BFSolution(
            allocation=[
                [100.0, 0.0, 0.0],
                [20.0, 130.0, 0.0],
                [0.0, 50.0, 150.0]
            ],
            basis=[(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)],
            cost=100*5 + 20*6 + 130*9 + 50*5 + 150*6
        )
        
        result = self.method.solve_from_bfs(problem, initial_bfs)
        
        self.assertEqual(result.status, SolutionStatus.OPTIMAL.value)
        
        solution = np.array(result.solution)
        # check supply constraints
        row_sums = solution.sum(axis=1)
        for i, supply in enumerate(problem.supply):
            self.assertAlmostEqual(row_sums[i], supply, places=4)
        
        # check demand constraints
        col_sums = solution.sum(axis=0)
        for j, demand in enumerate(problem.demand):
            self.assertAlmostEqual(col_sums[j], demand, places=4)


if __name__ == '__main__':
    unittest.main()