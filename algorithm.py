from collections import deque
class Algorithms:
    def __init__(self, maze, rows, cols):
        self.rows = rows
        self.cols = cols
        self.maze = maze
        self.alpha = 0.1
        self.gamma = 0.9
        self.c = 1.0
        self.episodes = 300
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


    def ucb(self):
        import math

        Q = {}
        N_s = {}
        N_sa = {}

        def state_key(r, c):
            return f"{r},{c}"

        def reward(r, c):
            if (r, c) == (self.rows - 1, self.cols - 1):
                return 10
            return -0.1

        for ep in range(self.episodes):
            state = (0, 0)
            done = False

            while not done:
                s_key = state_key(*state)
                Q.setdefault(s_key, {d[0]: 0 for d in self.DIRECTIONS})
                N_s[s_key] = N_s.get(s_key, 0) + 1
                N_sa.setdefault(s_key, {d[0]: 0 for d in self.DIRECTIONS})

                ucb_values = {}
                for dir, (dr, dc) in self.DIRECTIONS:
                    nr, nc = state[0] + dr, state[1] + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols and not self.maze[state[0]][state[1]][dir]:
                        n_s = N_s[s_key]
                        n_sa = N_sa[s_key][dir]
                        q = Q[s_key][dir]
                        ucb = q + self.c * math.sqrt(math.log(n_s + 1) / (n_sa + 1))
                        ucb_values[dir] = ucb

                if not ucb_values:
                    break

                action = max(ucb_values, key=ucb_values.get)
                dr, dc = dict(self.DIRECTIONS)[action]
                nr, nc = state[0] + dr, state[1] + dc
                next_state = (nr, nc)

                N_sa[s_key][action] += 1
                r = reward(nr, nc)

                ns_key = state_key(*next_state)
                Q.setdefault(ns_key, {d[0]: 0 for d in self.DIRECTIONS})

                best_next = max(Q[ns_key].values())
                Q[s_key][action] += self.alpha * (r + self.gamma * best_next - Q[s_key][action])

                if next_state == (self.rows - 1, self.cols - 1):
                    done = True

                state = next_state

        state = (0, 0)
        goal = (self.rows - 1, self.cols - 1)
        path = [state]
        visited = {state: None}

        while state != goal:
            s_key = state_key(*state)
            if s_key not in Q:
                break
            action = max(Q[s_key], key=Q[s_key].get)
            dr, dc = dict(self.DIRECTIONS)[action]
            nr, nc = state[0] + dr, state[1] + dc
            if not (0 <= nr < self.rows and 0 <= nc < self.cols):
                break
            if self.maze[state[0]][state[1]][action]:
                break
            
            next_state = (nr, nc)
            visited[next_state] = state
            path.append(next_state)
            state = next_state
            
            if state == goal:
                if goal not in visited: 
                    visited[goal] = path[-2] if len(path) > 1 else None
                break
        if goal not in visited:
            visited[goal] = None

        return path, visited

        


    def dls(self):
        pass

    def ids(self):
        pass
            
