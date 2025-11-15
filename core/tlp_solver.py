from utils.interfaces import IBFSFinder, ITransportationAlgorithm

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