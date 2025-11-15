from typing import List, Optional
from utils.constants import SolutionStatus
from dataclasses import dataclass


@dataclass
class TLPProblem:
    """Container for Transportation LP problem data"""
    supply: List[float]         # supply at each supplier (A_i)
    demand: List[float]         # demand at each consumer (B_j)
    costs: List[List[float]]    # cost matrix C[i][j] - cost from supplier i to consumer j
    
    @property
    def num_suppliers(self) -> int:
        """Number of suppliers (m)"""
        return len(self.supply)
    
    @property
    def num_consumers(self) -> int:
        """Number of consumers (n)"""
        return len(self.demand)
    
    @property
    def total_supply(self) -> float:
        """Total available supply"""
        return sum(self.supply)
    
    @property
    def total_demand(self) -> float:
        """Total required demand"""
        return sum(self.demand)
    
    def is_balanced(self) -> bool:
        """Check if problem is balanced (supply == demand)"""
        return abs(self.total_supply - self.total_demand) < 1e-6


@dataclass
class TLPResult:
    """Container for Transportation LP problem results"""
    status: SolutionStatus
    optimal_value: Optional[float] = None
    solution: Optional[List[List[float]]] = None  # allocation matrix X[i][j]
    error_message: Optional[str] = None
    
    @property
    def is_optimal(self) -> bool:
        """Check if optimal solution was found"""
        return SolutionStatus.OPTIMAL


@dataclass
class BFSolution:
    """Basic Feasible Solution (BFS) representation"""
    allocation: List[List[float]]   # current allocation matrix
    basis: List[tuple]              # list of basic variables (i, j)
    cost: float                     # total cost of current solution