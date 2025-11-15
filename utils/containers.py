from typing import List, Optional, Any, Dict
from dataclasses import dataclass

@dataclass
class TLPProblem:
    """Container for Transportation LP problem data"""
    pass


@dataclass
class TLPResult:
    """Container for Transportation LP problem results"""
    status: str
    optimal_value: Optional[float] = None
    solution: Optional[Dict[str, List[float]]] = None
    error_message: Optional[str] = None


@dataclass
class BFSolution:
    """Basic Feasible Solution (BFS) representation"""
    pass