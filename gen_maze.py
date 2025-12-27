
import random

class GenMaze:
    def __init__(self):
        self.maze = None
        self.visited = None
        self.rev_dir = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
        self.DIRECTIONS = [('N', (-1, 0)), ('S', (1, 0)), ('E', (0, 1)), ('W', (0, -1))]

    def _find(self, parent, x):
        if parent[x] != x:
            parent[x] = self._find(parent, parent[x])
        return parent[x]


    def _union(self, parent, rank, x, y):
        rx = self._find(parent, x)
        ry = self._find(parent, y)
        if rx == ry:
            return False

        if rank[rx] < rank[ry]:
            parent[rx] = ry
        elif rank[rx] > rank[ry]:
            parent[ry] = rx
        else:
            parent[ry] = rx
            rank[rx] += 1
        return True
    
    def generate_kruskal(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.maze = [[{'N': True, 'S': True, 'E': True, 'W': True}
                    for _ in range(cols)] for _ in range(rows)]
        parent = {}
        rank = {}

        def idx(r, c):
            return r * cols + c

        for r in range(rows):
            for c in range(cols):
                i = idx(r, c)
                parent[i] = i
                rank[i] = 0
        edges = []
        for r in range(rows):
            for c in range(cols):
                if r + 1 < rows:
                    edges.append((r, c, 'S', r + 1, c))
                if c + 1 < cols:
                    edges.append((r, c, 'E', r, c + 1))

        random.shuffle(edges)

        for r1, c1, d, r2, c2 in edges:
            a = idx(r1, c1)
            b = idx(r2, c2)

            if self._union(parent, rank, a, b):
                self.maze[r1][c1][d] = False
                self.maze[r2][c2][self.rev_dir[d]] = False

    def generate_prim(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.maze = [[{'N': True, 'S': True, 'E': True, 'W': True}
                    for _ in range(cols)] for _ in range(rows)]

        visited = [[False] * cols for _ in range(rows)]

        def add_frontiers(r, c, frontiers):
            for d, (dr, dc) in self.DIRECTIONS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                    frontiers.append((r, c, d, nr, nc))

        visited[0][0] = True
        frontiers = []
        add_frontiers(0, 0, frontiers)

        while frontiers:
            idx = random.randrange(len(frontiers))
            r1, c1, d, r2, c2 = frontiers.pop(idx)

            if visited[r2][c2]:
                continue

            self.maze[r1][c1][d] = False
            self.maze[r2][c2][self.rev_dir[d]] = False

            visited[r2][c2] = True
            add_frontiers(r2, c2, frontiers)


    def generate_dfs(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.maze = [[{'N': True, 'S': True, 'E': True, 'W': True}
                      for _ in range(cols)] for _ in range(rows)]
        self.visited = [[False] * cols for _ in range(rows)]

        stack = [(0, 0)]
        self.visited[0][0] = True

        while stack:
            r, c = stack[-1]
            neighbors = []

            for d, (dr, dc) in self.DIRECTIONS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and not self.visited[nr][nc]:
                    neighbors.append((d, nr, nc))

            if neighbors:
                d, nr, nc = random.choice(neighbors)
                self.maze[r][c][d] = False
                self.maze[nr][nc][self.rev_dir[d]] = False
                self.visited[nr][nc] = True
                stack.append((nr, nc))
            else:
                stack.pop()
