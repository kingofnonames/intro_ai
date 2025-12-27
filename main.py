import customtkinter as ctk
import tkinter as tk
import time
import os
from gen_maze import GenMaze
from algorithms import Algorithms

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DELAY = 50


class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Pathfinding Visualizer")
        self.root.geometry("1400x800")
        self.root.configure(fg_color="#F9FAFB")
        self.running = False
        self.paused = False
        self.gen_maze = GenMaze()
        self.algorithms = None
        self.maze = None
        self.goal = None
        self.build_ui()
    def build_ui(self):
        self.build_header()
        self.build_info()
        self.build_canvas()
    def build_header(self):
        header = ctk.CTkFrame(self.root, corner_radius=15)
        header.pack(padx=17, pady=15, fill="x")
        header.grid_columnconfigure(tuple(range(12)), weight=1)
        ctk.CTkLabel(header, text="Rows").grid(row=0, column=0)
        self.rows_entry = ctk.CTkEntry(header, width=60)
        self.rows_entry.insert(0, "15")
        self.rows_entry.grid(row=0, column=1)
        ctk.CTkLabel(header, text="Cols").grid(row=0, column=2)
        self.cols_entry = ctk.CTkEntry(header, width=60)
        self.cols_entry.insert(0, "20")
        self.cols_entry.grid(row=0, column=3)
        ctk.CTkLabel(header, text="Thuật sinh maze", font=("Arial", 13, "bold")).grid(
            row=0, column=4, padx=(17, 5)
        )
        self.maze_algo = tk.StringVar(value="DFS")
        self.maze_combo = ctk.CTkComboBox(
            header,
            values=["DFS", "Prim", "Kruskal"],
            variable=self.maze_algo,
            width=140,
            state="readonly",
        )
        self.maze_combo.grid(row=0, column=5)
        ctk.CTkLabel(header, text="Thuật tìm đường", font=("Arial", 13, "bold")).grid(
            row=0, column=7, padx=(17, 5)
        )
        self.path_algo = tk.StringVar(value="BFS")
        self.path_combo = ctk.CTkComboBox(
            header,
            values=["BFS", "DFS", "IDS", "DLS", "UCB", "AStar", "GBFS"],
            variable=self.path_algo,
            width=140,
            state="readonly",
        )
        self.path_combo.grid(row=0, column=8)
        self.btn_generate = ctk.CTkButton(
            header,
            text="Generate",
            compound="left",
            fg_color="#7C3AED",
            hover_color="#6D28D9",
            command=self.generate_maze,
        )
        self.btn_generate.grid(row=0, column=6, padx=8)
        self.btn_solve = ctk.CTkButton(
            header,
            text="Solve",
            compound="left",
            fg_color="#059669",
            hover_color="#047857",
            state="disabled",
            command=self.solve_maze,
        )
        self.btn_solve.grid(row=0, column=9, padx=8)

        self.btn_pause = ctk.CTkButton(
            header,
            text="Pause",
            fg_color="#F59E0B",
            hover_color="#D97706",
            state="disabled",
            command=self.pause,
        )
        self.btn_pause.grid(row=0, column=10, padx=8)

        self.btn_resume = ctk.CTkButton(
            header,
            text="Resume",
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            state="disabled",
            command=self.resume,
        )
        self.btn_resume.grid(row=0, column=11)

    def build_info(self):
        info = ctk.CTkFrame(self.root, fg_color="transparent")
        info.pack(pady=5)

        self.nodes_label = ctk.CTkLabel(info, text="Node lưu trữ: 0")
        self.nodes_label.pack(side="left", padx=10)

        self.depth_label = ctk.CTkLabel(info, text="Độ sâu: 0")
        self.depth_label.pack(side="left", padx=10)

        self.total_nodes_label = ctk.CTkLabel(info, text="Tổng node duyệt: 0")
        self.total_nodes_label.pack(side="left", padx=10)

        self.nodes_label_max = ctk.CTkLabel(info, text="Node max: 0")
        self.nodes_label_max.pack(side="left", padx=10)

        self.depth_label_max = ctk.CTkLabel(info, text="Độ sâu max: 0")
        self.depth_label_max.pack(side="left", padx=10)

    def build_canvas(self):
        frame = ctk.CTkFrame(self.root)
        frame.pack(expand=True, fill="both", padx=17, pady=10)

        self.canvas_maze = tk.Canvas(frame, bg="white")
        self.canvas_path = tk.Canvas(frame, bg="white")

        self.canvas_maze.pack(side="left", expand=True, padx=10)
        self.canvas_path.pack(side="right", expand=True, padx=10)

    def reset_info(self):
        self.nodes_label.configure(text="Node lưu trữ: 0")
        self.depth_label.configure(text="Độ sâu: 0")
        self.total_nodes_label.configure(text="Tổng node duyệt: 0")
        self.nodes_label_max.configure(text="Node max: 0")
        self.depth_label_max.configure(text="Độ sâu max: 0")

    def compute_cell_size(self):
        return max(6, min(600 // self.cols, 600 // self.rows))

    def generate_maze(self):
        self.running = False
        self.paused = False

        self.btn_pause.configure(state="disabled")
        self.btn_resume.configure(state="disabled")

        self.reset_info()

        try:
            self.rows = int(self.rows_entry.get())
            self.cols = int(self.cols_entry.get())
        except ValueError:
            return

        algo = self.maze_algo.get().lower()
        getattr(
            self.gen_maze, f"generate_{algo}", self.gen_maze.generate_dfs
        )(self.rows, self.cols)

        self.maze = self.gen_maze.maze
        self.goal = (self.rows - 1, self.cols - 1)
        self.algorithms = Algorithms(self.maze, self.rows, self.cols)

        self.canvas_maze.delete("all")
        self.canvas_path.delete("all")

        self.draw_maze(self.canvas_maze)
        self.draw_maze(self.canvas_path)

        self.btn_solve.configure(state="normal")

    def draw_maze(self, canvas):
        self.cell_size = self.compute_cell_size()
        canvas.config(
            width=self.cols * self.cell_size + 2,
            height=self.rows * self.cell_size + 2,
        )
        canvas.delete("all")

        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.maze[r][c]
                x, y = c * self.cell_size, r * self.cell_size

                if cell["N"]:
                    canvas.create_line(x, y, x + self.cell_size, y)
                if cell["S"]:
                    canvas.create_line(
                        x, y + self.cell_size, x + self.cell_size, y + self.cell_size
                    )
                if cell["W"]:
                    canvas.create_line(x, y, x, y + self.cell_size)
                if cell["E"]:
                    canvas.create_line(
                        x + self.cell_size, y, x + self.cell_size, y + self.cell_size
                    )

        canvas.create_rectangle(
            4, 4, self.cell_size - 4, self.cell_size - 4, fill="green"
        )
        canvas.create_rectangle(
            (self.cols - 1) * self.cell_size + 4,
            (self.rows - 1) * self.cell_size + 4,
            self.cols * self.cell_size - 4,
            self.rows * self.cell_size - 4,
            fill="red",
        )

    def solve_maze(self):
        if not self.algorithms:
            return

        self.running = False
        self.paused = False

        self.canvas_path.delete("all")
        self.reset_info()
        self.draw_maze(self.canvas_path)

        self.running = True
        self.btn_pause.configure(state="normal")
        self.btn_resume.configure(state="disabled")

        algo = self.path_algo.get().lower()
        found, order, parent, depth, frontier = getattr(self.algorithms, algo)()

        r_node = max(2, self.cell_size // 8)

        for i, (r, c) in enumerate(order):
            if not self.running:
                return

            while self.paused:
                self.root.update()
                time.sleep(0.05)

            cx = c * self.cell_size + self.cell_size // 2
            cy = r * self.cell_size + self.cell_size // 2

            self.canvas_path.create_oval(
                cx - r_node,
                cy - r_node,
                cx + r_node,
                cy + r_node,
                fill="#BFDBFE",
                outline="",
            )

            self.nodes_label.configure(text=f"Node lưu trữ: {frontier[i]}")
            self.depth_label.configure(text=f"Độ sâu: {depth.get((r, c), 0)}")
            self.total_nodes_label.configure(text=f"Tổng node duyệt: {i + 1}")

            self.root.update()
            time.sleep(DELAY / 1700)

        self.nodes_label_max.configure(text=f"Node lưu trữ max: {max(frontier)}")
        self.depth_label_max.configure(text=f"Độ sâu max: {max(depth.values())}")

        if found:
            self.draw_path(parent)

        self.running = False
        self.btn_pause.configure(state="disabled")
        self.btn_resume.configure(state="disabled")

    def draw_path(self, parent):
        cur = self.goal
        path = []

        while cur is not None:
            path.append(cur)
            cur = parent.get(cur)

        path.reverse()

        for (r1, c1), (r2, c2) in zip(path, path[1:]):
            if not self.running:
                return

            while self.paused:
                self.root.update()
                time.sleep(0.05)

            x1 = c1 * self.cell_size + self.cell_size // 2
            y1 = r1 * self.cell_size + self.cell_size // 2
            x2 = c2 * self.cell_size + self.cell_size // 2
            y2 = r2 * self.cell_size + self.cell_size // 2

            self.canvas_path.create_line(x1, y1, x2, y2, fill="red", width=3)
            self.root.update()
            time.sleep(DELAY / 1000)

    def pause(self):
        if self.running:
            self.paused = True
            self.btn_pause.configure(state="disabled")
            self.btn_resume.configure(state="normal")

    def resume(self):
        if self.running:
            self.paused = False
            self.btn_pause.configure(state="normal")
            self.btn_resume.configure(state="disabled")


if __name__ == "__main__":
    root = ctk.CTk()
    MazeApp(root)
    root.mainloop()
