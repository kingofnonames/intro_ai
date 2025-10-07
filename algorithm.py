from collections import deque
class Algorithms:
    def __init__(self, maze, rows, cols):
        self.rows = rows
        self.cols = cols
        self.maze = maze
        self.DIRECTIONS = [('N', (-1, 0)), ('S', (1, 0)), ('E', (0, 1)), ('W', (0, -1))]

    def bfs(self):
        start = (0, 0)
        goal = (self.rows - 1, self.cols - 1)
        queue = deque([start])
        visited = {start: None}
        path = []
        while queue:
            r, c = queue.popleft()
            if (r, c) == goal:
                break
            for dir, (dr, dc) in self.DIRECTIONS:
                if not self.maze[r][c][dir]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols and (nr, nc) not in visited:
                        visited[(nr, nc)] = (r, c)
                        path.append((nr, nc))
                        queue.append((nr, nc))
        return path, visited
    
    def dfs(self):
        pass

    def ucb(self):
        pass

    def dls(self):
        pass

    def ids(sels):
        pass
            
