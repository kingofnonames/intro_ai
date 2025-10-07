import tkinter as tk
from tkinter import ttk
import random
import time
from algorithm import Algorithms
from gen_maze import GenMaze
CELL_SIZE = 25
DELAY = 50

class MazeApp:
    def __init__(self, root):
        # Thêm tên hàm tìm kiếm, đúng tên thàm trong algorithm
        ALGORITHMS = ['BFS', 'DFS']
        self.gen_maze = GenMaze()

        self.root = root
        self.root.title("Maze Generator")
        
        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)

        tk.Label(control_frame, text="Số hàng:").grid(row=0, column=0)
        tk.Label(control_frame, text="Số cột:").grid(row=0, column=2)

        self.rows_entry = tk.Entry(control_frame, width=5)
        self.cols_entry = tk.Entry(control_frame, width=5)
        self.rows_entry.grid(row=0, column=1)
        self.cols_entry.grid(row=0, column=3)
        self.rows_entry.insert(0, "15")
        self.cols_entry.insert(0, "20")

        self.generate_button = tk.Button(control_frame, text="Tạo", command=self.generate_maze)
        self.generate_button.grid(row=0, column=4, padx=10)
        
        self.solve_button = tk.Button(control_frame, text="Tìm đường", command=self.solve_maze, state="disabled")
        self.solve_button.grid(row=0, column=5, padx=10)

        self.selected_option = tk.StringVar()
        tk.Label(control_frame, text="Thuật toán").grid(row=0, column=6, padx=10)
        self.algorithms_dropdown = ttk.Combobox(
            control_frame,
            textvariable=self.selected_option,
            values=ALGORITHMS,
            state='readonly'
        )
        self.algorithms_dropdown.grid(row=0, column=7, padx=10)
        self.algorithms_dropdown.current(0)
        canvas_frame = tk.Frame(root)
        canvas_frame.pack()

        self.canvas_maze = tk.Canvas(canvas_frame, bg="white")
        self.canvas_path = tk.Canvas(canvas_frame, bg="white")
        self.canvas_maze.pack(side="left", padx=10, pady=10)
        self.canvas_path.pack(side="right", padx=10, pady=10)
        # self.rev_dir = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
        # self.DIRECTIONS = [('N', (-1, 0)), ('S', (1, 0)), ('E', (0, 1)), ('W', (0, -1))]
        self.algorithms = None
        self.goal = None
    def generate_maze(self):
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
        except ValueError:
            print("Số cột, số hàng phải là số nguyên")
            return
        
        self.canvas_maze.delete("all")
        self.gen_maze.generate_maze(rows, cols)
        # self.maze = [[{'N': True, 'S': True, 'E': True, 'W': True} for _ in range(cols)] for _ in range(rows)]
        # self.visited = [[False for _ in range(cols)] for _ in range(rows)]
        self.maze = self.gen_maze.maze
        self.visited = self.gen_maze.visited
        self.rows, self.cols = rows, cols
        self.goal = (self.rows - 1, self.cols - 1)
        
        self.draw_maze(self.canvas_maze)
        self.draw_maze(self.canvas_path)
        self.solve_button.config(state='normal')
        self.algorithms = Algorithms(self.maze, self.rows, self.cols)


    def draw_maze(self, canvas):
        w = self.cols * CELL_SIZE
        h = self.rows * CELL_SIZE
        canvas.config(width=w+2, height=h+2)
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * CELL_SIZE 
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE 
                y2 = y1 + CELL_SIZE
                cell = self.maze[r][c]
                if cell['N']:
                    canvas.create_line(x1, y1, x2, y1, fill='black') 
                if cell['S']:
                    canvas.create_line(x1, y2, x2, y2, fill='black') 
                if cell['W']:
                    canvas.create_line(x1, y1, x1, y2, fill='black') 
                if cell['E']:
                    canvas.create_line(x2, y1, x2, y2, fill='black')
        canvas.create_rectangle(3, 3, CELL_SIZE - 3, CELL_SIZE - 3, fill="green")
        canvas.create_rectangle(
            self.cols * CELL_SIZE - CELL_SIZE + 3,
            self.rows * CELL_SIZE - CELL_SIZE + 3,
            self.cols * CELL_SIZE - 3,
            self.rows * CELL_SIZE - 3,
            fill='red'
        )

    def solve_maze(self):
        self.canvas_path.delete("all")
        self.draw_maze(self.canvas_path)
        path, visited = self.algorithms.__getattribute__(f'{self.selected_option.get().lower()}')()
        for (r, c) in path:
            x1 = c * CELL_SIZE + 3
            y1 = r * CELL_SIZE + 3
            x2 = x1 + CELL_SIZE - 6
            y2 = y1 + CELL_SIZE - 6
            self.canvas_path.create_rectangle(x1, y1, x2, y2, fill="yellow")
            self.root.update()
            time.sleep(DELAY / 1000)
        self.draw_path(visited)

    def draw_path(self, visited):
        current = self.goal
        path = []
        while current is not None:
            (r, c) = current
            path.append((r, c))
            current = visited[current]
        path = path[::-1]
        for (r, c) in path:
            x1 = c * CELL_SIZE + 5
            y1 = r * CELL_SIZE + 5
            x2 = x1 + CELL_SIZE - 10
            y2 = y1 + CELL_SIZE - 10
            self.canvas_path.create_rectangle(x1, y1, x2, y2, fill="blue")
            self.root.update()
            time.sleep(DELAY / 1000)
if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()