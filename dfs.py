def dfs(self):
    start = (0,0)
    goal = (self.rows - 1, self.cols - 1)
    stack = [start]
    visited = {start: None}
    path = []
    while stack:
        r,c = stack.pop()
        if(r,c) == goal:
            break
        for dir, (dr, dc) in self.DIRECTIONS:
            if not self.maze[r][c][dir]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < self.rows and 0 <= nc <self.cols and (nr, nc) not in visited:
                    visited[(nr, nc)] = (r,c)
                    path.append((nr, nc))
                    stack.append((nr,nc))
    return path, visited
