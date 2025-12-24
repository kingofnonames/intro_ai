import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import time
from algorithm import Algorithms
from gen_maze import GenMaze

# Cấu hình giao diện CustomTkinter
ctk.set_appearance_mode("light") 
ctk.set_default_color_theme("blue")

CELL_SIZE = 25
DELAY = 50

class MazeApp:
    def __init__(self, root):
        # Giữ nguyên danh sách và logic khởi tạo
        ALGORITHMS = ['BFS', 'DFS', 'IDS', 'DLS', 'UCB']
        self.gen_maze = GenMaze()
        self.root = root
        self.root.title("Maze Generator")
        self.root.configure(fg_color="#F8F9FA") # Màu nền xám nhạt hiện đại

        # --- GIAO DIỆN ĐIỀU KHIỂN (CONTROL PANEL) ---
        # Header frame chứa các input số hàng/cột
        self.header_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.header_frame.pack(pady=(20, 0))

        ctk.CTkLabel(self.header_frame, text="Số hàng:", font=("Arial", 13)).grid(row=0, column=0, padx=5)
        self.rows_entry = ctk.CTkEntry(self.header_frame, width=60, corner_radius=8)
        self.rows_entry.grid(row=0, column=1, padx=5)
        self.rows_entry.insert(0, "15")

        ctk.CTkLabel(self.header_frame, text="Số cột:", font=("Arial", 13)).grid(row=0, column=2, padx=5)
        self.cols_entry = ctk.CTkEntry(self.header_frame, width=60, corner_radius=8)
        self.cols_entry.grid(row=0, column=3, padx=5)
        self.cols_entry.insert(0, "20")

        # Control frame chính (Giống ảnh mẫu bạn gửi)
        self.main_control = ctk.CTkFrame(self.root, fg_color="white", corner_radius=15, height=80)
        self.main_control.pack(padx=20, pady=20, fill="x")

        # Label và Dropdown Thuật toán
        ctk.CTkLabel(self.main_control, text="Algorithm", font=("Arial", 14, "bold"), text_color="#1E293B").pack(side="left", padx=(30, 10))
        
        self.selected_option = tk.StringVar()
        self.algorithms_dropdown = ctk.CTkComboBox(
            self.main_control,
            variable=self.selected_option,
            values=ALGORITHMS,
            width=220,
            height=40,
            corner_radius=10,
            state='readonly'
        )
        self.algorithms_dropdown.pack(side="left", padx=10)
        self.algorithms_dropdown.set(ALGORITHMS[0])

        # Nút Tạo (Màu Gradient Tím/Hồng từ ảnh mẫu)
        self.generate_button = ctk.CTkButton(
            self.main_control, 
            text="Generate", 
            command=self.generate_maze,
            fg_color="#A855F7", hover_color="#9333EA",
            font=("Arial", 13, "bold"),
            height=40, corner_radius=10
        )
        self.generate_button.pack(side="left", padx=10)

        # Nút Tìm đường (Màu Xanh Ngọc từ ảnh mẫu)
        self.solve_button = ctk.CTkButton(
            self.main_control, 
            text="Solve", 
            command=self.solve_maze,
            fg_color="#0D9488", hover_color="#0F766E",
            font=("Arial", 13, "bold"),
            height=40, corner_radius=10,
            state="disabled"
        )
        self.solve_button.pack(side="left", padx=10)

        # Nút Reset (Trắng có viền xám từ ảnh mẫu)
        self.reset_btn = ctk.CTkButton(
            self.main_control, 
            text="Reset", 
            command=self.reset_canvases,
            fg_color="white", border_color="#E2E8F0", border_width=1,
            text_color="#475569", hover_color="#F1F5F9",
            font=("Arial", 13, "bold"),
            height=40, corner_radius=10
        )
        self.reset_btn.pack(side="left", padx=10)

        # --- KHU VỰC VẼ (CANVAS AREA) ---
        canvas_container = ctk.CTkFrame(self.root, fg_color="transparent")
        canvas_container.pack(expand=True, fill="both", padx=20, pady=10)

        self.canvas_maze = tk.Canvas(canvas_container, bg="white", highlightthickness=0, bd=0)
        self.canvas_path = tk.Canvas(canvas_container, bg="white", highlightthickness=0, bd=0)
        
        self.canvas_maze.pack(side="left", padx=15, pady=15, expand=True)
        self.canvas_path.pack(side="right", padx=15, pady=15, expand=True)

        self.algorithms = None
        self.goal = None

    # Giữ nguyên logic xử lý của bạn
    def generate_maze(self):
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
        except ValueError:
            return
        
        self.canvas_maze.delete("all")
        self.canvas_path.delete("all")
        self.gen_maze.generate_maze(rows, cols)
        
        self.maze = self.gen_maze.maze
        self.rows, self.cols = rows, cols
        self.goal = (self.rows - 1, self.cols - 1)
        
        self.draw_maze(self.canvas_maze)
        self.draw_maze(self.canvas_path)
        self.solve_button.configure(state='normal') # Sử dụng configure thay cho config của ctk
        self.algorithms = Algorithms(self.maze, self.rows, self.cols)

    def draw_maze(self, canvas):
        w = self.cols * CELL_SIZE
        h = self.rows * CELL_SIZE
        canvas.config(width=w, height=h)
        for r in range(self.rows):
            for c in range(self.cols):
                x1, y1 = c * CELL_SIZE, r * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                cell = self.maze[r][c]
                # Sử dụng màu xám nhạt cho tường để trông sạch sẽ hơn
                line_color = '#CBD5E1'
                if cell['N']: canvas.create_line(x1, y1, x2, y1, fill=line_color, width=1) 
                if cell['S']: canvas.create_line(x1, y2, x2, y2, fill=line_color, width=1) 
                if cell['W']: canvas.create_line(x1, y1, x1, y2, fill=line_color, width=1) 
                if cell['E']: canvas.create_line(x2, y1, x2, y2, fill=line_color, width=1)
        
        # Điểm Start/Goal hình tròn bo góc
        canvas.create_oval(5, 5, CELL_SIZE-5, CELL_SIZE-5, fill="#22C55E", outline="")
        canvas.create_oval(w-CELL_SIZE+5, h-CELL_SIZE+5, w-5, h-5, fill="#EF4444", outline="")

    def solve_maze(self):
        self.canvas_path.delete("all")
        self.draw_maze(self.canvas_path)
        path, visited = self.algorithms.__getattribute__(f'{self.selected_option.get().lower()}')()
        
        for (r, c) in path:
            parent = visited.get((r, c))
            if parent:
                pr, pc = parent
                x1 = pc * CELL_SIZE + CELL_SIZE // 2
                y1 = pr * CELL_SIZE + CELL_SIZE // 2
                x2 = c * CELL_SIZE + CELL_SIZE // 2
                y2 = r * CELL_SIZE + CELL_SIZE // 2
                # Màu vàng gradient nhạt cho quá trình quét
                self.canvas_path.create_line(x1, y1, x2, y2, fill="#FBBF24", width=3, capstyle=tk.ROUND)
                
            self.root.update()
            time.sleep(DELAY / 1000)
        self.draw_path(visited)

    def draw_path(self, visited):
        current = self.goal
        path = []
        while current is not None:
            path.append(current)
            current = visited.get(current)
        
        path = path[::-1]
        for i in range(len(path) - 1):
            r1, c1 = path[i]
            r2, c2 = path[i+1]
            x1 = c1 * CELL_SIZE + CELL_SIZE // 2
            y1 = r1 * CELL_SIZE + CELL_SIZE // 2
            x2 = c2 * CELL_SIZE + CELL_SIZE // 2
            y2 = r2 * CELL_SIZE + CELL_SIZE // 2
            # Màu xanh dương đậm hiện đại
            self.canvas_path.create_line(x1, y1, x2, y2, fill="#2563EB", width=5, capstyle=tk.ROUND, joinstyle=tk.ROUND)
            self.root.update()
            time.sleep(DELAY / 1000)

    def reset_canvases(self):
        self.canvas_maze.delete("all")
        self.canvas_path.delete("all")
        self.solve_button.configure(state="disabled")

if __name__ == "__main__":
    # Sử dụng CTk thay vì tk.Tk
    root = ctk.CTk()
    app = MazeApp(root)
    root.mainloop()