from utils.interfaces import IBFSFinder

class VogelsMethod(IBFSFinder):
    def find_initial_bfs(self, problem):
        return super().find_initial_bfs(problem)