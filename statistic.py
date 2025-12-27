import os
import pickle
import numpy as np
import matplotlib.pyplot as plt

from gen_maze import GenMaze
from algorithms import Algorithms
import csv

def export_results_to_csv(results, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, "results_summary.csv")

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "maze_size",
            "maze_algo",
            "path_algo",
            "metric",
            "mean",
            "std"
        ])

        for size_key in results:
            for m_algo in results[size_key]:
                for p_algo in results[size_key][m_algo]:
                    for metric, values in results[size_key][m_algo][p_algo].items():
                        # found chỉ dùng để ký hiệu, không đưa vào bảng số
                        if metric == "found":
                            continue

                        arr = np.array(values)
                        writer.writerow([
                            size_key,
                            m_algo,
                            p_algo,
                            metric,
                            round(arr.mean(), 3),
                            round(arr.std(), 3)
                        ])

    print(f"Đã xuất bảng số liệu CSV: {csv_path}")

class MazeStats:
    def __init__(self, maze, rows, cols):
        self.algorithms = Algorithms(maze, rows, cols)

    def run(self, algo_name):
        found, order, parent, depth, frontier = getattr(
            self.algorithms, algo_name.lower()
        )()

        unique_nodes = len(set(order))
        total_nodes = len(order)

        return {
            "found": found,
            "unique_nodes": unique_nodes,
            "total_nodes": total_nodes,
            "redundancy": total_nodes / unique_nodes if unique_nodes > 0 else 0,
            "max_depth": max(depth.values()) if depth else 0,
            "max_frontier": max(frontier) if frontier else 0
        }

def plot_astar_vs_bfs(results, maze_algos, maze_sizes, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    maze_colors = {
        "dfs": "#1f77b4",
        "prim": "#ff7f0e",
        "kruskal": "#2ca02c"
    }

    sizes = [f"{r}x{c}" for r, c in maze_sizes]
    x = np.arange(len(sizes))
    width = 0.35

    for m_algo in maze_algos:
        bfs_vals = []
        astar_vals = []

        for size_key in sizes:
            bfs_vals.append(
                np.mean(results[size_key][m_algo]["bfs"]["total_nodes"])
            )
            astar_vals.append(
                np.mean(results[size_key][m_algo]["astar"]["total_nodes"])
            )

        plt.figure(figsize=(9, 6))

        plt.bar(x - width/2, bfs_vals, width, label="BFS")
        plt.bar(x + width/2, astar_vals, width, label="A*")

        plt.xticks(x, sizes)
        plt.xlabel("Kích thước mê cung")
        plt.ylabel("Tổng số trạng thái được mở")
        plt.title(f"So sánh BFS và A* ({m_algo.upper()} maze)")

        plt.legend()
        plt.grid(axis="y", alpha=0.3)

        plt.tight_layout()
        plt.savefig(
            os.path.join(output_dir, f"Astar_vs_BFS_{m_algo}.png")
        )
        plt.close()

def run_experiments(maze_algos, path_algos, maze_sizes, runs):
    results = {}

    for rows, cols in maze_sizes:
        size_key = f"{rows}x{cols}"
        results[size_key] = {
            m: {p: {k: [] for k in [
                "unique_nodes",
                "total_nodes",
                "redundancy",
                "max_depth",
                "max_frontier",
                "found"
            ]} for p in path_algos}
            for m in maze_algos
        }

        for m_algo in maze_algos:
            for _ in range(runs):
                gen = GenMaze()
                getattr(gen, f"generate_{m_algo}")(rows, cols)
                maze = gen.maze

                stats = MazeStats(maze, rows, cols)

                for p_algo in path_algos:
                    res = stats.run(p_algo)
                    for k in res:
                        results[size_key][m_algo][p_algo][k].append(res[k])

    return results


def plot_metrics(results, maze_algos, path_algos, maze_sizes, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    maze_colors = {
        "dfs": "#1f77b4",
        "prim": "#ff7f0e",
        "kruskal": "#2ca02c"
    }

    metric_titles = {
        "total_nodes": "Tổng số trạng thái được mở",
        "max_frontier": "Kích thước frontier lớn nhất (Bộ nhớ)",
        "max_depth": "Độ sâu lớn nhất đạt được",
        "redundancy": "Tỷ lệ lặp trạng thái (Redundancy)"
    }

    found_symbols = {True: "✓", False: "✗"}

    for size_key in results:
        for metric, title in metric_titles.items():
            plt.figure(figsize=(13, 8))

            y_pos = np.arange(len(path_algos))
            height = 0.2
            gap = 0.05

            for i, m_algo in enumerate(maze_algos):
                offset = (i - len(maze_algos)/2) * (height + gap) + height/2

                for j, p_algo in enumerate(path_algos):
                    values = np.array(results[size_key][m_algo][p_algo][metric])
                    mean, std = values.mean(), values.std()

                    found_mean = np.mean(
                        results[size_key][m_algo][p_algo]["found"]
                    ) == 1.0

                    plt.barh(
                        y_pos[j] + offset,
                        mean,
                        height,
                        xerr=std,
                        capsize=5,
                        color=maze_colors[m_algo]
                    )

                    plt.text(
                        mean + std + 0.5,
                        y_pos[j] + offset,
                        f"{mean:.1f}±{std:.1f}",
                        va="center",
                        fontsize=9
                    )

                    plt.text(
                        0,
                        y_pos[j] + offset,
                        found_symbols[found_mean],
                        va="center",
                        ha="left",
                        color="white",
                        fontsize=12,
                        fontweight="bold"
                    )

            plt.yticks(y_pos, [p.upper() for p in path_algos])
            plt.ylabel("Thuật toán tìm đường")
            plt.xlabel(title)
            plt.title(f"{title} – Maze {size_key}")

            legend = [
                plt.Rectangle((0, 0), 1, 1, color=maze_colors[m])
                for m in maze_algos
            ]
            plt.legend(legend, [m.upper() for m in maze_algos],
                       title="Thuật toán sinh mê cung")

            plt.tight_layout()
            plt.savefig(
                os.path.join(output_dir, f"{metric}_{size_key}.png")
            )
            plt.close()

def plot_ids_redundancy(results, maze_algos, maze_sizes, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(10, 6))

    maze_colors = {
        "dfs": "#1f77b4",
        "prim": "#ff7f0e",
        "kruskal": "#2ca02c"
    }

    sizes = [f"{r}x{c}" for r, c in maze_sizes]
    x = np.arange(len(sizes))

    for m_algo in maze_algos:
        y = []
        for size_key in sizes:
            values = results[size_key][m_algo]["ids"]["redundancy"]
            y.append(np.mean(values))

        plt.plot(
            x,
            y,
            marker="o",
            linewidth=2,
            label=m_algo.upper(),
            color=maze_colors[m_algo]
        )

    plt.xticks(x, sizes)
    plt.xlabel("Kích thước mê cung")
    plt.ylabel("Redundancy (Total / Unique nodes)")
    plt.title("Thuật toán IDS: Đánh đổi thời gian để tiết kiệm bộ nhớ")

    plt.legend(title="Thuật toán sinh mê cung")
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "IDS_redundancy_vs_size.png"))
    plt.close()

# if __name__ == "__main__":
#     OUTPUT_DIR = "maze_results_V4"

#     maze_algos = ["dfs", "prim", "kruskal"]
#     path_algos = ["bfs", "dfs", "ids", "dls", "ucb", "astar", "gbfs"]

#     maze_sizes = [
#         (5, 5),
#         (10, 10),
#         (20, 20),
#         (30, 30),
#         (40, 40),
#         (50, 50),
#         (70, 70),
#         (90, 90),
#         (100, 100),
#         (120, 120),
#         (150, 150),
#     ]

#     runs = 3

#     results = run_experiments(
#         maze_algos,
#         path_algos,
#         maze_sizes,
#         runs
#     )

#     with open(os.path.join(OUTPUT_DIR, "results_v4.pkl"), "wb") as f:
#         pickle.dump(results, f)
#     export_results_to_csv(results, OUTPUT_DIR)
#     plot_metrics(
#         results,
#         maze_algos,
#         path_algos,
#         maze_sizes,
#         OUTPUT_DIR
#     )


#     plot_ids_redundancy(
#         results,
#         maze_algos,
#         maze_sizes,
#         OUTPUT_DIR
#     )

#     plot_astar_vs_bfs(
#         results,
#         maze_algos,
#         maze_sizes,
#         OUTPUT_DIR
#     )

if __name__ == "__main__":
    OUTPUT_DIR = "maze_results_V5"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    maze_algos = ["dfs"]
    path_algos = ["bfs", "dfs", "ids", "dls", "ucb"]

    maze_sizes = [
        (5, 5),
        (10, 10),
        (20, 20),
        (30, 30),
        (40, 40),
        (50, 50),
    ]

    runs = 3

    results = run_experiments(
        maze_algos,
        path_algos,
        maze_sizes,
        runs
    )

    with open(os.path.join(OUTPUT_DIR, "results_v5.pkl"), "wb") as f:
        pickle.dump(results, f)
    export_results_to_csv(results, OUTPUT_DIR)
    plot_metrics(
        results,
        maze_algos,
        path_algos,
        maze_sizes,
        OUTPUT_DIR
    )


    # plot_ids_redundancy(
    #     results,
    #     maze_algos,
    #     maze_sizes,
    #     OUTPUT_DIR
    # )

    # plot_astar_vs_bfs(
    #     results,
    #     maze_algos,
    #     maze_sizes,
    #     OUTPUT_DIR
    # )

