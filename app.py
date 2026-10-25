"""
========================================================================================
SMART RESOURCE ALLOCATION AND SCHEDULING SYSTEM USING GREEDY ALGORITHMS
DAA Lab 3 — Application Entrypoint
Author: Bhavya Rattan (Roll No: 2401201004)
Programme: BCA (Artificial Intelligence & Data Science), SOET
Course: Design and Analysis of Algorithms (ENCA301)
Faculty In-Charge: Dr. Aarti
Institution: K.R. Mangalam University, Gurugram, Haryana
========================================================================================
"""

import sys
import os
import time

# Ensure proper encoding on Windows console
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from algorithms.fractional_knapsack import fractional_knapsack, KnapsackItem
from algorithms.activity_selection import activity_selection, Activity
from algorithms.huffman_coding import huffman_encode, huffman_decode, build_huffman_tree


def print_banner():
    print("=" * 80)
    print("   SMART RESOURCE ALLOCATION & SCHEDULING SYSTEM (GREEDY ALGORITHMS)   ")
    print("           K.R. MANGALAM UNIVERSITY - SOET - BCA (AI & DS)             ")
    print("   Student: Bhavya Rattan | Roll No: 2401201004 | Faculty: Dr. Aarti   ")
    print("=" * 80)


def menu_fractional_knapsack():
    print("\n" + "-" * 75)
    print("  [1] RESOURCE ALLOCATION MODULE : FRACTIONAL KNAPSACK ALGORITHM  ")
    print("  Greedy Strategy: Highest Value-to-Weight Ratio First | O(n log n)")
    print("-" * 75)
    print("1. Run with Default University Budget & Resource Dataset")
    print("2. Enter Custom Resources / Items Manually")
    print("3. Return to Main Menu")

    choice = input("Select an option (1-3): ").strip()

    if choice == "1":
        items = [
            {"name": "Gold / Server Compute Cluster", "weight": 10, "value": 60},
            {"name": "Silver / High-Bandwidth Cloud", "weight": 20, "value": 100},
            {"name": "Bronze / Storage Storage Array", "weight": 30, "value": 120},
            {"name": "Platinum / GPU Acceleration Unit", "weight": 15, "value": 105},
            {"name": "Copper / Backup Power Grid", "weight": 25, "value": 50},
        ]
        capacity = 50.0
    elif choice == "2":
        try:
            num = int(input("Enter number of items/resources: "))
            items = []
            for i in range(num):
                name = input(f"  Item {i+1} Name: ").strip() or f"Item_{i+1}"
                wt = float(input(f"  Item {i+1} Weight/Cost: "))
                val = float(input(f"  Item {i+1} Profit/Value: "))
                items.append({"name": name, "weight": wt, "value": val})
            capacity = float(input("Enter Knapsack / Resource Total Capacity: "))
        except ValueError:
            print("[!] Invalid numeric input. Returning to menu.")
            return
    else:
        return

    # Execute algorithm
    t0 = time.perf_counter()
    max_profit, allocation = fractional_knapsack(items, capacity)
    elapsed = (time.perf_counter() - t0) * 1000

    print("\n" + "=" * 70)
    print(f"  OPTIMAL RESOURCE ALLOCATION RESULT (Total Capacity: {capacity})")
    print("=" * 70)
    print(f"{'Item Name':<30} {'Weight':<10} {'Value':<10} {'Ratio':<10} {'Allocated %':<12}")
    print("-" * 70)

    total_weight_used = 0.0
    for name, frac, wt, val in allocation:
        total_weight_used += wt
        ratio = (val / wt) if wt > 0 else 0
        print(f"{name:<30} {wt:<10.1f} {val:<10.1f} {ratio:<10.2f} {frac*100:<11.1f}%")

    print("-" * 70)
    print(f"Total Weight Consumed: {total_weight_used:.1f} / {capacity:.1f}")
    print(f"MAXIMUM ACHIEVABLE PROFIT: ${max_profit:.2f}")
    print(f"Computation Time: {elapsed:.4f} ms")
    print("=" * 70)


def menu_activity_selection():
    print("\n" + "-" * 75)
    print("  [2] TASK SCHEDULING MODULE : ACTIVITY SELECTION ALGORITHM  ")
    print("  Greedy Strategy: Earliest Finish Time First (EFT) | O(n log n)")
    print("-" * 75)
    print("1. Run with Default University Lecture & Lab Schedule")
    print("2. Enter Custom Tasks / Activities Manually")
    print("3. Return to Main Menu")

    choice = input("Select an option (1-3): ").strip()

    if choice == "1":
        activities = [
            {"name": "A1: Python AI Lab", "start": 1, "finish": 4},
            {"name": "A2: DAA Lecture", "start": 3, "finish": 5},
            {"name": "A3: Database Seminar", "start": 0, "finish": 6},
            {"name": "A4: Cloud Computing Lab", "start": 5, "finish": 7},
            {"name": "A5: Math Tutorial", "start": 3, "finish": 9},
            {"name": "A6: Machine Learning Session", "start": 5, "finish": 9},
            {"name": "A7: Operating Systems Quiz", "start": 6, "finish": 10},
            {"name": "A8: Capstone Project Review", "start": 8, "finish": 11},
        ]
    elif choice == "2":
        try:
            num = int(input("Enter number of activities: "))
            activities = []
            for i in range(num):
                name = input(f"  Activity {i+1} Name: ").strip() or f"A_{i+1}"
                start = float(input(f"  Start Time: "))
                finish = float(input(f"  Finish Time: "))
                if finish <= start:
                    print("  [!] Warning: Finish time must be greater than start. Adjusting finish = start + 1")
                    finish = start + 1
                activities.append({"name": name, "start": start, "finish": finish})
        except ValueError:
            print("[!] Invalid numeric input. Returning to menu.")
            return
    else:
        return

    # Execute algorithm
    t0 = time.perf_counter()
    selected = activity_selection(activities)
    elapsed = (time.perf_counter() - t0) * 1000

    print("\n" + "=" * 70)
    print(f"  OPTIMAL TASK SCHEDULING RESULT ({len(selected)} of {len(activities)} Scheduled)")
    print("=" * 70)
    print(f"{'Order':<6} {'Activity Name':<32} {'Start':<8} {'Finish':<8} {'Duration':<10}")
    print("-" * 70)

    for idx, act in enumerate(selected, 1):
        print(f"{idx:<6} {act['name']:<32} {act['start']:<8.1f} {act['finish']:<8.1f} {act['duration']:<10.1f}")

    print("-" * 70)
    print(f"Max Mutually Compatible Non-Overlapping Tasks: {len(selected)}")
    print(f"Schedule Execution Time: {elapsed:.4f} ms")
    print("=" * 70)


def menu_huffman_coding():
    print("\n" + "-" * 75)
    print("  [3] DATA COMPRESSION MODULE : HUFFMAN CODING ALGORITHM  ")
    print("  Greedy Strategy: Frequency-based Min-Priority Tree | O(n log n)")
    print("-" * 75)
    print("1. Run with Classic Benchmark String: 'abracadabra'")
    print("2. Run with Natural Language University Text Sample")
    print("3. Enter Custom String Manually")
    print("4. Return to Main Menu")

    choice = input("Select an option (1-4): ").strip()

    if choice == "1":
        text = "abracadabra"
    elif choice == "2":
        text = "design and analysis of algorithms smart resource allocation system using greedy methods"
    elif choice == "3":
        text = input("Enter text to compress: ").strip()
        if not text:
            print("[!] Text cannot be empty.")
            return
    else:
        return

    # Execute algorithm
    t0 = time.perf_counter()
    bits, codebook, freqs, stats = huffman_encode(text)
    elapsed = (time.perf_counter() - t0) * 1000

    # Verification: Lossless decoding
    root = build_huffman_tree(text)
    decoded = huffman_decode(bits, root)
    is_lossless = (decoded == text)

    print("\n" + "=" * 75)
    print("  HUFFMAN COMPRESSION & CODEBOOK STATISTICS")
    print("=" * 75)
    print(f"Input Text: \"{text[:60]}{'...' if len(text)>60 else ''}\"")
    print(f"Length: {len(text)} characters ({stats['distinct_chars']} unique characters)")
    print("-" * 75)
    print(f"{'Character':<12} {'Frequency':<12} {'Probability':<14} {'Huffman Code':<16} {'Length (bits)':<12}")
    print("-" * 75)

    sorted_chars = sorted(freqs.keys(), key=lambda ch: freqs[ch], reverse=True)
    for ch in sorted_chars:
        code = codebook[ch]
        prob = freqs[ch] / len(text)
        display_ch = repr(ch) if ch in (' ', '\n', '\t') else ch
        print(f"{display_ch:<12} {freqs[ch]:<12} {prob:<14.3f} {code:<16} {len(code):<12}")

    print("-" * 75)
    print(f"Encoded Bitstream: {bits[:70]}{'...' if len(bits)>70 else ''}")
    print(f"Original ASCII Size   : {stats['original_bits']} bits ({len(text)} bytes)")
    print(f"Compressed Size       : {stats['compressed_bits']} bits ({stats['compressed_bits']/8:.2f} bytes)")
    print(f"Compression Ratio     : {stats['compression_ratio']:.2%}")
    print(f"Space Savings         : {stats['space_savings_percent']:.2f}%")
    print(f"Average Bits/Char     : {stats['avg_code_length']:.2f} bits (vs 8.00 standard ASCII)")
    print(f"Lossless Decompression: {'[SUCCESS] Perfectly Preserved' if is_lossless else '[FAILED]'}")
    print(f"Compression Time      : {elapsed:.4f} ms")
    print("=" * 75)


def menu_complexity_comparison():
    print("\n" + "=" * 78)
    print("  COMPLEXITY COMPARISON & BENCHMARK SUMMARY (QUESTION 5)")
    print("=" * 78)
    print(f"{'Algorithm':<22} {'Time Complexity':<18} {'Space Complexity':<18} {'Greedy Strategy'}")
    print("-" * 78)
    print(f"{'Fractional Knapsack':<22} {'O(n log n)':<18} {'O(n)':<18} {'Value/Weight Ratio'}")
    print(f"{'Activity Selection':<22} {'O(n log n)':<18} {'O(n)':<18} {'Earliest Finish Time'}")
    print(f"{'Huffman Coding':<22} {'O(n log n)':<18} {'O(n)':<18} {'Min-Heap Tree Merge'}")
    print("=" * 78)

    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_csv", "benchmark_results.csv")
    if os.path.exists(csv_path):
        import pandas as pd
        df = pd.read_csv(csv_path)
        print("\nEmpirical Benchmark Results (Sample from data_csv/benchmark_results.csv):")
        print(df.to_string(index=False))
    else:
        print("\n[i] Run the benchmark generator (Option 5) to produce data_csv/benchmark_results.csv.")


def menu_generate_visualizations():
    print("\n[*] Invoking visualization suite...")
    try:
        from analysis import generate_benchmarks_and_charts as gbc
        gbc.generate_knapsack_chart()
        gbc.generate_activity_timeline()
        gbc.generate_huffman_chart()
        gbc.generate_huffman_tree_diagram()
        df = gbc.run_benchmarks()
        gbc.generate_performance_and_memory_charts(df)
        print("\n[SUCCESS] All 6 visualization figures generated in 'graphes/' directory!")
        print("1. graphes/knapsack_allocation.png")
        print("2. graphes/activity_timeline.png")
        print("3. graphes/huffman_compression.png")
        print("4. graphes/huffman_tree.png")
        print("5. graphes/performance_comparison.png")
        print("6. graphes/memory_usage_comparison.png")
    except Exception as e:
        print(f"[!] Error generating charts: {e}")


def menu_student_info():
    print("\n" + "=" * 70)
    print("               ACADEMIC CREDENTIALS & METADATA                ")
    print("=" * 70)
    print("  Student Name    : Bhavya Rattan")
    print("  Roll Number     : 2401201004")
    print("  Programme       : Bachelor of Computer Applications (AI & DS)")
    print("  School          : School of Engineering & Technology (SOET)")
    print("  Course          : Design and Analysis of Algorithms (ENCA301)")
    print("  Faculty Mentor  : Dr. Aarti")
    print("  Institution     : K.R. Mangalam University, Gurugram, Haryana")
    print("  Lab Title       : Lab 3: Smart Resource Allocation and Scheduling")
    print("                    System using Greedy Algorithms")
    print("  Mapped Outcome  : CO3 (Design and analyze greedy optimization)")
    print("=" * 70)


def main():
    while True:
        print_banner()
        print("  1. Resource Allocation Module (Fractional Knapsack)")
        print("  2. Task Scheduling Module (Activity Selection)")
        print("  3. Data Compression Module (Huffman Coding)")
        print("  4. View Complexity Comparison Table (Question 5)")
        print("  5. Generate All Visualizations & Performance Charts (Question 6)")
        print("  6. View Student Credentials & Academic Metadata")
        print("  7. Exit Application")
        print("=" * 80)

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            menu_fractional_knapsack()
        elif choice == "2":
            menu_activity_selection()
        elif choice == "3":
            menu_huffman_coding()
        elif choice == "4":
            menu_complexity_comparison()
        elif choice == "5":
            menu_generate_visualizations()
        elif choice == "6":
            menu_student_info()
        elif choice == "7":
            print("\nExiting Smart Resource Allocation & Scheduling System. Good luck Bhavya!")
            sys.exit(0)
        else:
            print("[!] Invalid option. Please enter a number between 1 and 7.")

        input("\nPress [Enter] to return to the main menu...")


if __name__ == "__main__":
    main()
