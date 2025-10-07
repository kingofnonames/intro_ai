import tkinter as tk
import random

CELL_SIZE = 25

class MazeApp:
    def __init__(self, root):
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

        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(padx=10, pady=10)
        self.rev_dir = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def generate_maze(self):
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
        except ValueError:
            print("Số cột, số hàng phải là số nguyên")
            return
        
        self.canvas.delete("all")
        self.maze = [[{'N': True, 'S': True, 'E': True, 'W': True} for _ in range(cols)] for _ in range(rows)]
        self.visited = [[False for _ in range(cols)] for _ in range(rows)]
        self.rows, self.cols = rows, cols
        
        self.dfs(0, 0)
        self.draw_maze()

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

    def draw_maze(self):
        w = self.cols * CELL_SIZE
        h = self.rows * CELL_SIZE
        self.canvas.config(width=w+2, height=h+2)
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * CELL_SIZE 
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE 
                y2 = y1 + CELL_SIZE
                cell = self.maze[r][c]
                if cell['N']:
                    self.canvas.create_line(x1, y1, x2, y1, fill='black') 
                if cell['S']:
                    self.canvas.create_line(x1, y2, x2, y2, fill='black') 
                if cell['W']:
                    self.canvas.create_line(x1, y1, x1, y2, fill='black') 
                if cell['E']:
                    self.canvas.create_line(x2, y1, x2, y2, fill='black')
        self.canvas.create_rectangle(3, 3, CELL_SIZE - 3, CELL_SIZE - 3, fill="green")
        self.canvas.create_rectangle(
            self.cols * CELL_SIZE - CELL_SIZE + 3,
            self.rows * CELL_SIZE - CELL_SIZE + 3,
            self.cols * CELL_SIZE - 3,
            self.rows * CELL_SIZE - 3,
            fill='red'
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()