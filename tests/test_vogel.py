import pytest
import numpy as np
from utils import TLPProblem, BFSolution
from core import VogelsMethod

# fixtures
@pytest.fixture
def vogels_method():
    return VogelsMethod()

@pytest.fixture
def simple_balanced_problem():
    supply = [10.0, 20.0]
    demand = [15.0, 5.0, 10.0]
    costs = [[2.0, 3.0, 1.0], 
             [4.0, 1.0, 5.0]]
    return TLPProblem(supply=supply, demand=demand, costs=costs)

@pytest.fixture
def standard_balanced_problem():
    supply = [30.0, 50.0, 20.0]
    demand = [20.0, 40.0, 30.0, 10.0]
    costs = [[10.0, 5.0, 8.0, 9.0], 
             [7.0, 9.0, 10.0, 4.0], 
             [3.0, 6.0, 5.0, 2.0]]
    return TLPProblem(supply=supply, demand=demand, costs=costs)

@pytest.fixture
def degenerate_problem():
    supply = [10.0, 10.0]
    demand = [10.0, 10.0]
    costs = [[1.0, 2.0], 
             [3.0, 4.0]]
    return TLPProblem(supply=supply, demand=demand, costs=costs)



class TestVogelsPenalties:

    def setup_method(self, method):
        self.costs = np.array([[2.0, 3.0, 1.0], 
                               [4.0, 1.0, 5.0]])
        self.active_rows = {0, 1}
        self.active_cols = {0, 1, 2}
        self.vm = VogelsMethod()

    def test_calculate_row_penalties_full(self):
        penalties = self.vm._calculate_row_penalties(self.costs, self.active_rows, self.active_cols)
        assert penalties == {0: 1.0, 1: 3.0}

    def test_calculate_col_penalties_full(self):
        penalties = self.vm._calculate_col_penalties(self.costs, self.active_rows, self.active_cols)
        assert penalties == {0: 2.0, 1: 2.0, 2: 4.0}

    def test_calculate_row_penalties_partial(self):
        active_cols_partial = {0}
        penalties = self.vm._calculate_row_penalties(self.costs, self.active_rows, active_cols_partial)
        assert penalties == {0: 2.0, 1: 4.0}



class TestVogelsMethodFindInitialBFS:

    def test_simple_balanced_problem(self, vogels_method: VogelsMethod, simple_balanced_problem: TLPProblem):
        solution = vogels_method.find_initial_bfs(simple_balanced_problem)
        
        expected_allocation = [[0.0, 0.0, 10.0], 
                               [15.0, 5.0, 0.0]]
        expected_cost = (10.0 * 1.0) + (15.0 * 4.0) + (5.0 * 1.0) # 75.0
        expected_basis = [(1, 1), (1, 0), (0, 2)] 
        
        assert isinstance(solution, BFSolution)
        assert np.allclose(solution.allocation, expected_allocation)
        assert solution.cost == pytest.approx(expected_cost)
        assert set(solution.basis) == set(expected_basis) 
        
    def test_standard_balanced_problem_cost(self, vogels_method: VogelsMethod, standard_balanced_problem: TLPProblem):
        solution = vogels_method.find_initial_bfs(standard_balanced_problem)
        
        # Expected VAM steps (R-Row Penalty, C-Col Penalty, [i,j] allocation, D-Degenerate)
        # 1. Max Penalty C0=4. Allocate (2,0): min(20, 20)=20. R2 out, D0 out. Cost: 20*3=60
        # 2. Max Penalty C3=5. Allocate (1,3): min(50, 10)=10. D3 out. Cost: 10*4=40
        # 3. Max Penalty C1=4. Allocate (0,1): min(30, 40)=30. R0 out. Cost: 30*5=150
        # 4. Max Penalty R1=3. Allocate (1,2): min(40, 30)=30. D2 out. Cost: 30*10=300
        # 5. Max Penalty R1=9. Allocate (1,1): min(10, 10)=10. R1 out, D1 out (D). Cost: 10*9=90
        # Total Cost: 60 + 40 + 150 + 300 + 90 = 640.0
        
        expected_cost = 640.0
        assert isinstance(solution, BFSolution)
        assert solution.cost == pytest.approx(expected_cost)
        assert len(solution.basis) >= standard_balanced_problem.num_suppliers + standard_balanced_problem.num_consumers - 1 - 1 # VAM might be degenerate
        
    def test_degenerate_problem(self, vogels_method: VogelsMethod, degenerate_problem: TLPProblem):
        solution = vogels_method.find_initial_bfs(degenerate_problem)
        
        expected_allocation = [[10.0, 0.0], [0.0, 10.0]]
        expected_cost = 10.0 * 1.0 + 10.0 * 4.0 # 50.0
        expected_basis = [(0, 0), (1, 1)] 

        assert isinstance(solution, BFSolution)
        assert np.allclose(solution.allocation, expected_allocation)
        assert solution.cost == pytest.approx(expected_cost)
        assert set(solution.basis) == set(expected_basis)
        assert len(solution.basis) == 2 # expected degeneracy (m + n - 1 = 3)