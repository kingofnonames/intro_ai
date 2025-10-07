import random

class GenMaze:
    def __init__(self):
        self.maze = None
        self.visited = None
        self.rev_dir = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
    def generate_maze(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.maze = [[{'N': True, 'S': True, 'E': True, 'W': True} for _ in range(cols)] for _ in range(rows)]
        self.visited = [[False for _ in range(cols)] for _ in range(rows)]
        self.dfs(0, 0)

    def dfs(self, r, c):
        self.visited[r][c] = True
        directions = [('N', (-1, 0)), ('S', (1, 0)), ('E', (0, 1)), ('W', (0, -1))]
        random.shuffle(directions)

        for dir, (dr, dc) in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and not self.visited[nr][nc]:
                try:
                    self.maze[r][c][dir] = False
                    self.maze[nr][nc][self.rev_dir[dir]] = False
                except IndexError:
                    print(r, c)
                self.dfs(nr, nc)