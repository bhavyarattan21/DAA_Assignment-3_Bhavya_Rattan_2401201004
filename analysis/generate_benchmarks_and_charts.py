"""
Benchmark Engine and Visualizations Generator
DAA Lab 3: Smart Resource Allocation and Scheduling System using Greedy Algorithms
Student: Bhavya Rattan (Roll No: 2401201004)
Faculty: Dr. Aarti
"""

import os
import sys
import time
import tracemalloc

# Ensure stdout handles UTF-8 characters on Windows consoles
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
# Project root resolution (must be added before importing algorithms)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import random
import string
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Import our algorithms
from algorithms.fractional_knapsack import fractional_knapsack
from algorithms.activity_selection import activity_selection
from algorithms.huffman_coding import huffman_encode, build_huffman_tree, Node

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Ensure output directories exist
GRAPHES_DIR = os.path.join(PROJECT_ROOT, "graphes")
DATA_DIR = os.path.join(PROJECT_ROOT, "data_csv")
os.makedirs(GRAPHES_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# Styling configuration for professional charts
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 0.8


# ==============================================================================
# 1. VISUALIZATION 1: Fractional Knapsack Resource Allocation
# ==============================================================================
def generate_knapsack_chart():
    items = [
        {"name": "Gold", "weight": 10, "value": 60},
        {"name": "Silver", "weight": 20, "value": 100},
        {"name": "Bronze", "weight": 30, "value": 120},
        {"name": "Platinum", "weight": 15, "value": 105},
        {"name": "Copper", "weight": 25, "value": 50},
    ]
    capacity = 50
    total_val, allocation = fractional_knapsack(items, capacity=capacity)

    names = [x[0] for x in allocation]
    pcts = [x[1] * 100 for x in allocation]
    weights_taken = [x[2] for x in allocation]
    vals_contributed = [x[3] for x in allocation]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8), gridspec_kw={'width_ratios': [1.2, 1]})

    # Bar chart of allocation %
    colors = ['#10b981' if p == 100 else '#f59e0b' if p > 0 else '#94a3b8' for p in pcts]
    bars = ax1.bar(names, pcts, color=colors, edgecolor='#1e293b', linewidth=1.2, width=0.55)

    for bar, pct, wt, val in zip(bars, pcts, weights_taken, vals_contributed):
        height = bar.get_height()
        ax1.annotate(f'{pct:.1f}%\n({wt:.1f}kg / ${val:.0f})',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 4), textcoords="offset points",
                     ha='center', va='bottom', fontsize=9, fontweight='bold', color='#1e293b')

    ax1.set_ylim(0, 120)
    ax1.set_ylabel("Percentage Taken (%)", fontsize=10, fontweight='bold')
    ax1.set_title("Fractional Knapsack: Resource Allocation %", fontsize=11, fontweight='bold', pad=10)
    ax1.grid(axis='y', linestyle='--', alpha=0.5)

    # Donut chart for weight composition
    ax2.pie(weights_taken, labels=names, autopct='%1.1f%%', startangle=140,
            colors=['#3b82f6', '#10b981', '#f59e0b'],
            wedgeprops=dict(width=0.45, edgecolor='w', linewidth=2))
    ax2.set_title(f"Knapsack Weight Fill (Total: {sum(weights_taken):.0f}/{capacity} kg)\nMax Profit Achieved: ${total_val:.2f}",
                  fontsize=10, fontweight='bold', pad=10)

    plt.suptitle("Resource Allocation Module — Fractional Knapsack Analysis\nStudent: Bhavya Rattan (2401201004)",
                 fontsize=12, fontweight='bold', y=1.02)
    plt.tight_layout()
    chart_path = os.path.join(GRAPHES_DIR, "knapsack_allocation.png")
    plt.savefig(chart_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[OK] Saved: {chart_path}")


# ==============================================================================
# 2. VISUALIZATION 2: Activity Selection Gantt-style Timeline
# ==============================================================================
def generate_activity_timeline():
    all_activities = [
        {"name": "A1", "start": 1, "finish": 4},
        {"name": "A2", "start": 3, "finish": 5},
        {"name": "A3", "start": 0, "finish": 6},
        {"name": "A4", "start": 5, "finish": 7},
        {"name": "A5", "start": 3, "finish": 9},
        {"name": "A6", "start": 5, "finish": 9},
        {"name": "A7", "start": 6, "finish": 10},
        {"name": "A8", "start": 8, "finish": 11},
    ]

    selected = activity_selection(all_activities)
    selected_names = {a["name"] for a in selected}

    fig, ax = plt.subplots(figsize=(10, 5))

    # Sort all by finish time to display logically
    sorted_all = sorted(all_activities, key=lambda x: x["finish"])

    y_positions = range(len(sorted_all))
    for i, act in enumerate(sorted_all):
        is_sel = act["name"] in selected_names
        color = '#10b981' if is_sel else '#e2e8f0'
        edge = '#047857' if is_sel else '#94a3b8'
        alpha = 1.0 if is_sel else 0.55
        hatch = None if is_sel else '//'

        # Draw bar
        ax.barh(i, act["finish"] - act["start"], left=act["start"], height=0.55,
                color=color, edgecolor=edge, linewidth=1.5, alpha=alpha, hatch=hatch)

        # Text label inside bar
        label_text = f"{act['name']} [{act['start']}→{act['finish']}]"
        label_color = '#ffffff' if is_sel else '#475569'
        ax.text((act["start"] + act["finish"]) / 2, i, label_text,
                va='center', ha='center', fontsize=9, fontweight='bold', color=label_color)

    ax.set_yticks(list(y_positions))
    ax.set_yticklabels([a["name"] for a in sorted_all], fontsize=10, fontweight='bold')
    ax.set_xlabel("Time Slots (Hours)", fontsize=10, fontweight='bold')
    ax.set_xlim(-0.5, 12)
    ax.set_title("Task Scheduling Module — Activity Selection Timeline\nSelected Non-Overlapping Activities: A1 -> A4 -> A8 (Total: 3 Activities)",
                 fontsize=11, fontweight='bold', pad=12)

    # Legend
    legend_elements = [
        patches.Patch(facecolor='#10b981', edgecolor='#047857', label='Selected (Optimal Non-Overlapping)'),
        patches.Patch(facecolor='#e2e8f0', edgecolor='#94a3b8', hatch='//', label='Rejected (Overlapping Conflict)')
    ]
    ax.legend(handles=legend_elements, loc='upper left', frameon=True, facecolor='#ffffff', edgecolor='#cbd5e1')
    ax.grid(axis='x', linestyle='--', alpha=0.7)

    plt.suptitle("Bhavya Rattan (Roll No: 2401201004) | DAA Lab 3", fontsize=10, color='#64748b', y=0.99)
    plt.tight_layout()
    chart_path = os.path.join(GRAPHES_DIR, "activity_timeline.png")
    plt.savefig(chart_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[OK] Saved: {chart_path}")


# ==============================================================================
# 3. VISUALIZATION 3: Huffman Coding Compression Statistics
# ==============================================================================
def generate_huffman_chart():
    text = "abracadabra"
    encoded_bits, codebook, freqs, stats = huffman_encode(text)

    chars = sorted(freqs.keys(), key=lambda ch: freqs[ch], reverse=True)
    frequencies = [freqs[ch] for ch in chars]
    code_lengths = [len(codebook[ch]) for ch in chars]
    codes_str = [codebook[ch] for ch in chars]

    fig, ax1 = plt.subplots(figsize=(9, 4.8))

    x = np.arange(len(chars))
    width = 0.35

    rects1 = ax1.bar(x - width/2, frequencies, width, label='Character Frequency', color='#6366f1', edgecolor='#312e81')
    ax2 = ax1.twinx()
    rects2 = ax2.bar(x + width/2, code_lengths, width, label='Huffman Code Length (Bits)', color='#06b6d4', edgecolor='#083344')

    ax1.set_xlabel("Characters", fontsize=10, fontweight='bold')
    ax1.set_ylabel("Frequency Count", color='#4338ca', fontsize=10, fontweight='bold')
    ax2.set_ylabel("Code Length (Bits)", color='#0891b2', fontsize=10, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels([f"'{c}'\nCode: {codes_str[i]}" for i, c in enumerate(chars)], fontsize=9, fontweight='bold')

    # Annotations
    for bar in rects1:
        ax1.annotate(f"{bar.get_height()}", xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                     xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')

    for bar in rects2:
        ax2.annotate(f"{bar.get_height()}b", xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                     xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')

    ax1.set_ylim(0, max(frequencies) + 2)
    ax2.set_ylim(0, max(code_lengths) + 2)

    # Info banner on chart
    info_str = f"Original: {stats['original_bits']} bits  |  Compressed: {stats['compressed_bits']} bits  |  Savings: {stats['space_savings_percent']:.1f}%"
    plt.title(f"Data Compression Module — Huffman Coding Analysis\n{info_str}",
              fontsize=11, fontweight='bold', pad=12)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', frameon=True)

    plt.suptitle("Bhavya Rattan (Roll No: 2401201004) | DAA Lab 3", fontsize=9, color='#64748b', y=1.02)
    plt.tight_layout()
    chart_path = os.path.join(GRAPHES_DIR, "huffman_compression.png")
    plt.savefig(chart_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[OK] Saved: {chart_path}")


# ==============================================================================
# 4. VISUALIZATION 4: Huffman Tree Visual Representation
# ==============================================================================
def generate_huffman_tree_diagram():
    text = "abracadabra"
    root = build_huffman_tree(text)

    # Assign positions to nodes using recursive depth and breadth
    node_positions = {}
    edges = []

    def get_width(node):
        if not node:
            return 0
        if node.is_leaf():
            return 1
        return get_width(node.left) + get_width(node.right)

    def assign_coords(node, x_left, x_right, y, level=0):
        if not node:
            return
        x = (x_left + x_right) / 2
        node_positions[id(node)] = (x, y, node)

        if node.left:
            w_left = get_width(node.left)
            w_total = get_width(node)
            split = x_left + (x_right - x_left) * (w_left / w_total)
            edges.append((node, node.left, '0'))
            assign_coords(node.left, x_left, split, y - 1.2, level + 1)

        if node.right:
            w_left = get_width(node.left)
            w_total = get_width(node)
            split = x_left + (x_right - x_left) * (w_left / w_total)
            edges.append((node, node.right, '1'))
            assign_coords(node.right, split, x_right, y - 1.2, level + 1)

    assign_coords(root, 0, 10, 5)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.axis('off')

    # Draw edges
    for parent, child, label in edges:
        px, py, _ = node_positions[id(parent)]
        cx, cy, _ = node_positions[id(child)]
        ax.plot([px, cx], [py, cy], color='#64748b', linewidth=1.5, zorder=1)
        # Edge label (0 or 1)
        mx, my = (px + cx) / 2, (py + cy) / 2
        offset = -0.15 if label == '0' else 0.15
        ax.text(mx + offset, my, label, fontsize=9, fontweight='bold', color='#ef4444' if label=='1' else '#2563eb')

    # Draw nodes
    for nid, (x, y, node) in node_positions.items():
        if node.is_leaf():
            circle = plt.Circle((x, y), 0.35, color='#10b981', ec='#047857', lw=1.8, zorder=2)
            ax.add_patch(circle)
            ax.text(x, y + 0.05, f"'{node.char}'", ha='center', va='center', fontsize=9, fontweight='bold', color='#ffffff', zorder=3)
            ax.text(x, y - 0.18, f"f={node.freq}", ha='center', va='center', fontsize=7.5, color='#ecfdf5', zorder=3)
        else:
            circle = plt.Circle((x, y), 0.32, color='#6366f1', ec='#3730a3', lw=1.8, zorder=2)
            ax.add_patch(circle)
            ax.text(x, y, f"{node.freq}", ha='center', va='center', fontsize=9, fontweight='bold', color='#ffffff', zorder=3)

    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 6.0)
    ax.set_title("Optimal Huffman Binary Prefix Tree for 'abracadabra'\nStudent: Bhavya Rattan (2401201004) | Faculty: Dr. Aarti",
                 fontsize=11, fontweight='bold', pad=12)

    # Legend
    legend_elements = [
        patches.Patch(facecolor='#10b981', edgecolor='#047857', label='Leaf Node (Character & Frequency)'),
        patches.Patch(facecolor='#6366f1', edgecolor='#3730a3', label='Internal Node (Summed Frequency)'),
        patches.Patch(facecolor='#ffffff', edgecolor='#ef4444', label="Branch 0: Left | Branch 1: Right")
    ]
    ax.legend(handles=legend_elements, loc='lower right', frameon=True)

    plt.tight_layout()
    chart_path = os.path.join(GRAPHES_DIR, "huffman_tree.png")
    plt.savefig(chart_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[OK] Saved: {chart_path}")


# ==============================================================================
# 5. BENCHMARK ENGINE: Run Timing & Memory Measurements (Question 5)
# ==============================================================================
def run_benchmarks():
    print("[*] Running comprehensive benchmark experiments for all 3 greedy algorithms...")

    input_sizes = [10, 50, 100, 250, 500, 1000, 2500, 5000, 10000]
    results = []

    for n in input_sizes:
        print(f"    Benchmarking size n = {n} ...")

        # -----------------------------
        # 1. Fractional Knapsack Benchmark
        # -----------------------------
        knapsack_items = [
            {"name": f"Item_{i}", "weight": random.uniform(5, 100), "value": random.uniform(10, 500)}
            for i in range(n)
        ]
        cap = n * 25.0

        tracemalloc.start()
        t0 = time.perf_counter()
        fractional_knapsack(knapsack_items, capacity=cap)
        t_knapsack = time.perf_counter() - t0
        _, mem_knapsack = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # -----------------------------
        # 2. Activity Selection Benchmark
        # -----------------------------
        activities = []
        for i in range(n):
            s = random.randint(0, n * 2)
            f = s + random.randint(1, 50)
            activities.append({"name": f"A_{i}", "start": s, "finish": f})

        tracemalloc.start()
        t0 = time.perf_counter()
        activity_selection(activities)
        t_activity = time.perf_counter() - t0
        _, mem_activity = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # -----------------------------
        # 3. Huffman Coding Benchmark
        # -----------------------------
        # Generate text with skewed frequency distribution
        charset = string.ascii_letters + string.digits
        weights = [1.0 / (i + 1) for i in range(len(charset))]
        text_sample = "".join(random.choices(charset, weights=weights, k=n))

        tracemalloc.start()
        t0 = time.perf_counter()
        huffman_encode(text_sample)
        t_huffman = time.perf_counter() - t0
        _, mem_huffman = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        results.append({
            "Input_Size_n": n,
            "Knapsack_Time_sec": t_knapsack,
            "Knapsack_Mem_KB": mem_knapsack / 1024.0,
            "Activity_Time_sec": t_activity,
            "Activity_Mem_KB": mem_activity / 1024.0,
            "Huffman_Time_sec": t_huffman,
            "Huffman_Mem_KB": mem_huffman / 1024.0,
        })

    df = pd.DataFrame(results)
    csv_path = os.path.join(DATA_DIR, "benchmark_results.csv")
    df.to_csv(csv_path, index=False)
    print(f"[OK] Benchmark results saved to {csv_path}")

    return df


# ==============================================================================
# 6. VISUALIZATIONS 5 & 6: Performance & Memory Comparison Charts
# ==============================================================================
def generate_performance_and_memory_charts(df):
    # -----------------------------
    # Performance Growth Curve (Time)
    # -----------------------------
    fig, ax = plt.subplots(figsize=(9, 5))

    n = df["Input_Size_n"].values
    ax.plot(n, df["Knapsack_Time_sec"] * 1000, marker='o', lw=2, color='#3b82f6', label='Fractional Knapsack (O(n log n))')
    ax.plot(n, df["Activity_Time_sec"] * 1000, marker='s', lw=2, color='#10b981', label='Activity Selection (O(n log n))')
    ax.plot(n, df["Huffman_Time_sec"] * 1000, marker='^', lw=2, color='#f59e0b', label='Huffman Coding (O(n log n))')

    # Theoretical O(n log n) reference curve
    c = (df["Knapsack_Time_sec"].iloc[-1] * 1000) / (n[-1] * np.log2(n[-1]))
    theo_curve = c * n * np.log2(n)
    ax.plot(n, theo_curve, linestyle='--', color='#94a3b8', lw=1.5, label='Theoretical O(n log n) Curve')

    ax.set_xlabel("Input Size (n)", fontsize=10, fontweight='bold')
    ax.set_ylabel("Execution Time (Milliseconds)", fontsize=10, fontweight='bold')
    ax.set_title("Empirical Execution Time vs Input Size (n)\nAll Greedy Algorithms Exhibit O(n log n) Growth",
                 fontsize=11, fontweight='bold', pad=12)
    ax.legend(frameon=True, loc='upper left')
    ax.grid(True, linestyle='--', alpha=0.6)

    plt.suptitle("Bhavya Rattan (Roll No: 2401201004) | DAA Lab 3 Benchmarks", fontsize=9, color='#64748b', y=1.01)
    plt.tight_layout()
    chart_path = os.path.join(GRAPHES_DIR, "performance_comparison.png")
    plt.savefig(chart_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[OK] Saved: {chart_path}")

    # -----------------------------
    # Memory Growth Curve
    # -----------------------------
    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(n, df["Knapsack_Mem_KB"], marker='o', lw=2, color='#3b82f6', label='Fractional Knapsack (O(n))')
    ax.plot(n, df["Activity_Mem_KB"], marker='s', lw=2, color='#10b981', label='Activity Selection (O(n))')
    ax.plot(n, df["Huffman_Mem_KB"], marker='^', lw=2, color='#f59e0b', label='Huffman Coding (O(n))')

    ax.set_xlabel("Input Size (n)", fontsize=10, fontweight='bold')
    ax.set_ylabel("Peak Memory Usage (KB)", fontsize=10, fontweight='bold')
    ax.set_title("Peak Memory Usage vs Input Size (n)\nLinear Memory O(n) Footprint Across All Algorithms",
                 fontsize=11, fontweight='bold', pad=12)
    ax.legend(frameon=True, loc='upper left')
    ax.grid(True, linestyle='--', alpha=0.6)

    plt.suptitle("Bhavya Rattan (Roll No: 2401201004) | DAA Lab 3 Benchmarks", fontsize=9, color='#64748b', y=1.01)
    plt.tight_layout()
    mem_chart_path = os.path.join(GRAPHES_DIR, "memory_usage_comparison.png")
    plt.savefig(mem_chart_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[OK] Saved: {mem_chart_path}")


if __name__ == "__main__":
    print("=" * 65)
    print(" DAA LAB 3: GENERATING BENCHMARKS & VISUALIZATIONS")
    print(" Student: Bhavya Rattan | Roll No: 2401201004 | SOET, KRMU")
    print("=" * 65)

    generate_knapsack_chart()
    generate_activity_timeline()
    generate_huffman_chart()
    generate_huffman_tree_diagram()
    df_results = run_benchmarks()
    generate_performance_and_memory_charts(df_results)

    print("=" * 65)
    print("[SUCCESS] All Lab 3 charts and benchmark_results.csv generated successfully!")
    print("=" * 65)
