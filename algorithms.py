from collections import deque
import math
import heapq
class Algorithms:
    def __init__(self, maze, rows, cols):
        self.maze = maze
        self.rows = rows
        self.cols = cols
        self.DIRECTIONS = [('N', (-1, 0)), ('S', (1, 0)),
                           ('E', (0, 1)), ('W', (0, -1))]

    def bfs(self):
        start = (0, 0)
        goal = (self.rows - 1, self.cols - 1)

        queue = deque([start])
        parent = {start: None}
        depth = {start: 0}
        order = []
        frontier_sizes = []
        found = False
        while queue:
            frontier_sizes.append(len(queue))
            r, c = queue.popleft()
            order.append((r, c))

            if (r, c) == goal:
                found = True
                break

            for d, (dr, dc) in self.DIRECTIONS:
                if not self.maze[r][c][d]:
                    nr, nc = r + dr, c + dc
                    if (nr, nc) not in parent:
                        parent[(nr, nc)] = (r, c)
                        depth[(nr, nc)] = depth[(r, c)] + 1
                        queue.append((nr, nc))

        return found, order, parent, depth, frontier_sizes

    def dfs(self):
        start = (0, 0)
        goal = (self.rows - 1, self.cols - 1)

        stack = [start]
        parent = {start: None}
        depth = {start: 0}
        order = []
        frontier_sizes = []
        found = False
        while stack:
            frontier_sizes.append(len(stack))
            r, c = stack.pop()
            order.append((r, c))

            if (r, c) == goal:
                found = True
                break

            for d, (dr, dc) in reversed(self.DIRECTIONS):
                if not self.maze[r][c][d]:
                    nr, nc = r + dr, c + dc
                    if (nr, nc) not in parent:
                        parent[(nr, nc)] = (r, c)
                        depth[(nr, nc)] = depth[(r, c)] + 1
                        stack.append((nr, nc))

        return found, order, parent, depth, frontier_sizes

    def dls(self, limit=10):
        start = (0, 0)
        goal = (self.rows - 1, self.cols - 1)
        found = False
        stack = [(start, 0)]
        parent = {start: None}
        depth = {start: 0}
        order = []
        frontier_sizes = []

        while stack:
            frontier_sizes.append(len(stack))
            (r, c), d = stack.pop()
            order.append((r, c))

            if (r, c) == goal:
                found = True
                break

            if d < limit:
                for dir, (dr, dc) in reversed(self.DIRECTIONS):
                    if not self.maze[r][c][dir]:
                        nr, nc = r + dr, c + dc
                        if (nr, nc) not in parent:
                            parent[(nr, nc)] = (r, c)
                            depth[(nr, nc)] = d + 1
                            stack.append(((nr, nc), d + 1))
        
        return found, order, parent, depth, frontier_sizes

    def ids(self):
        goal = (self.rows - 1, self.cols - 1)

        total_order = []
        total_frontier = []

        for limit in range(1, self.rows * self.cols):
            found, order, parent, depth, frontier = self.dls(limit)

            total_order.extend(order)
            total_frontier.extend(frontier)

            if found:
                return True, total_order, parent, depth, total_frontier

        return False, total_order, {}, {}, total_frontier


    def ucb(self):
        return self.bfs()
    
    def heuristic(self, node, goal):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])
    
    def astar(self):
        start = (0, 0)
        goal = (self.rows - 1, self.cols - 1)

        pq = []
        heapq.heappush(pq, (0, start))

        parent = {start: None}
        g_score = {start: 0}
        order = []
        frontier_sizes = []
        found = False

        while pq:
            frontier_sizes.append(len(pq))
            f, (r, c) = heapq.heappop(pq)

            if (r, c) in order:
                continue

            order.append((r, c))

            if (r, c) == goal:
                found = True
                break

            for d, (dr, dc) in self.DIRECTIONS:
                if not self.maze[r][c][d]:
                    nr, nc = r + dr, c + dc
                    tentative_g = g_score[(r, c)] + 1

                    if (nr, nc) not in g_score or tentative_g < g_score[(nr, nc)]:
                        g_score[(nr, nc)] = tentative_g
                        parent[(nr, nc)] = (r, c)
                        f_score = tentative_g + self.heuristic((nr, nc), goal)
                        heapq.heappush(pq, (f_score, (nr, nc)))

        depth = g_score
        return found, order, parent, depth, frontier_sizes


    def gbfs(self):
        start = (0, 0)
        goal = (self.rows - 1, self.cols - 1)

        pq = []
        heapq.heappush(pq, (self.heuristic(start, goal), start))

        parent = {start: None}
        depth = {start: 0}
        order = []
        frontier_sizes = []
        visited = set()
        found = False

        while pq:
            frontier_sizes.append(len(pq))
            _, (r, c) = heapq.heappop(pq)

            if (r, c) in visited:
                continue
            visited.add((r, c))
            order.append((r, c))

            if (r, c) == goal:
                found = True
                break

            for d, (dr, dc) in self.DIRECTIONS:
                if not self.maze[r][c][d]:
                    nr, nc = r + dr, c + dc
                    if (nr, nc) not in visited:
                        parent[(nr, nc)] = (r, c)
                        depth[(nr, nc)] = depth[(r, c)] + 1
                        heapq.heappush(pq, (self.heuristic((nr, nc), goal), (nr, nc)))

        return found, order, parent, depth, frontier_sizes
