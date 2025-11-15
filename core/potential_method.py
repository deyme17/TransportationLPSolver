from utils.interfaces import ITransportationAlgorithm

class PotentialMethod(ITransportationAlgorithm):
    def solve_from_bfs(self, problem, initial_solution):
        return super().solve_from_bfs(problem, initial_solution)