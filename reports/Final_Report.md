# K.R. MANGALAM UNIVERSITY, GURUGRAM, HARYANA
## SCHOOL OF ENGINEERING AND TECHNOLOGY (SOET)
### DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING / APPLICATIONS

---

# LAB 3 FINAL REPORT: SMART RESOURCE ALLOCATION AND SCHEDULING SYSTEM USING GREEDY ALGORITHMS

* **Course Title & Code:** Design and Analysis of Algorithms (ENCA301)
* **Programme:** BCA (Artificial Intelligence & Data Science)
* **Semester / Academic Year:** 3rd Semester / 2026–2027
* **Faculty In-Charge:** Dr. Aarti
* **Student Name:** **Bhavya Rattan**
* **Roll Number:** **2401201004**
* **Mapped Course Outcome (CO):** CO3 (Design and analyze greedy optimization techniques)
* **Repository Link:** `https://github.com/bhavyarattan/daa-lab3-greedy-system`
* **Submission Platform:** ZOSIMA + GitHub

---

## 1. EXECUTIVE SUMMARY & PROBLEM STATEMENT

Modern distributed systems, cloud computing data centers, and telecommunication networks face complex optimization challenges daily. These systems must:
1. Maximize utility from budget-constrained physical resources (e.g., allocating virtual CPUs and memory).
2. Schedule shared computational tasks and meeting facilities to avoid overlap while maximizing throughput.
3. Minimize data storage footprint and transmission bandwidth across communication channels.

This lab implements a unified **Smart Resource Allocation and Scheduling System** powered by three foundational greedy algorithms:
* **Resource Allocation Module:** Fractional Knapsack Algorithm
* **Task Scheduling Module:** Activity Selection Algorithm
* **Data Compression Module:** Huffman Coding Algorithm

Through formal mathematical proofs, empirical benchmarking, memory profiling, and visualization charts, this report analyzes the efficiency, correctness, and practical viability of greedy optimization strategies.

---

## 2. THEORETICAL FOUNDATION: THE GREEDY PARADIGM

A **Greedy Algorithm** constructs an optimal solution incrementally, making a sequence of locally optimal choices with the expectation that these choices lead to a globally optimal solution. Unlike Dynamic Programming, a greedy algorithm never backtracks or reconsiders past decisions.

### Core Properties Required for Greedy Optimality:
1. **Greedy-Choice Property:** A globally optimal solution can be arrived at by making locally optimal (greedy) choices without looking ahead to subproblem solutions.
2. **Optimal Substructure:** An optimal solution to the overall problem contains within it optimal solutions to its subproblems.

```
+-----------------------------------------------------------------------------------+
|                              THE GREEDY CYCLE                                    |
|                                                                                   |
|  [Input Set S]  -->  [Sort/Order by Greedy Metric]  -->  [Pick Best Item x]       |
|                             ^                                     |               |
|                             |                                     v               |
|                    [Update Constraints]  <--  [Include x if Feasible & Compatible]|
+-----------------------------------------------------------------------------------+
```

---

## 3. ALGORITHMIC DESIGN & GREEDY STRATEGY EFFECTIVENESS

### 3.1 Resource Allocation Module: Fractional Knapsack

#### Problem Formulation:
Given $n$ resources/items where each item $i$ possesses a weight $w_i > 0$ and a profit/value $v_i > 0$, and a system with total knapsack capacity $W$. The objective is to maximize total profit by taking fractions $x_i \in [0, 1]$ of items:
$$\text{Maximize } \sum_{i=1}^{n} v_i x_i \quad \text{subject to} \quad \sum_{i=1}^{n} w_i x_i \le W$$

#### Greedy Strategy:
Sort items in descending order of value-to-weight ratio $r_i = \frac{v_i}{w_i}$. Sequentially take whole items ($x_i = 1$) as long as remaining capacity permits. When an item cannot fit completely, take the fraction $x_i = \frac{W_{\text{remaining}}}{w_i}$ to saturate capacity.

#### Proof of Optimality (Exchange Argument):
Assume there exists an optimal solution $O = (o_1, o_2, \dots, o_n)$ different from the greedy solution $G = (g_1, g_2, \dots, g_n)$. Let $k$ be the first item where $g_k \ne o_k$. By definition of our greedy rule, $g_k > o_k$. There must exist another item $j > k$ where $o_j > g_j$ and $r_k \ge r_j$.
If we exchange a small amount of weight $\Delta w$ from item $j$ to item $k$ in $O$, the change in total value is:
$$\Delta V = \Delta w (r_k - r_j) \ge 0$$
Since $r_k \ge r_j$, the new solution is at least as valuable as $O$. Continuing this exchange process transforms $O$ into $G$ without ever decreasing the total value, proving $G$ is globally optimal.

---

### 3.2 Task Scheduling Module: Activity Selection

#### Problem Formulation:
Given a set of $n$ activities $S = \{A_1, A_2, \dots, A_n\}$ where each activity $A_i$ has a start time $s_i$ and finish time $f_i$ ($s_i < f_i$). Find a maximum-cardinality subset of mutually compatible (non-overlapping) activities.

#### Greedy Strategy:
Sort activities by **earliest finish time** ($f_1 \le f_2 \le \dots \le f_n$). Select $A_1$, then iteratively add activity $A_i$ if and only if $s_i \ge f_{\text{last\_selected}}$.

#### Why Other Greedy Metrics Fail:
* *Shortest Duration First ($f_i - s_i$):* Fails. Example: $[0, 5]$, $[4, 6]$, $[5, 10]$. Picking the shortest $[4, 6]$ leaves room for only 1 activity, whereas picking $[0, 5]$ and $[5, 10]$ yields 2.
* *Fewest Conflicts First:* Suboptimal and requires $O(n^2)$ recomputation.
* *Earliest Finish Time First:* **Provably Optimal**. Finishes as early as possible, freeing the maximum remaining time for subsequent activities.

---

### 3.3 Data Compression Module: Huffman Coding

#### Problem Formulation:
Given a string of characters with known frequencies $f(c)$, construct a variable-length prefix-free binary tree that minimizes the total weighted path length (total encoded bits):
$$B(T) = \sum_{c \in C} f(c) \cdot d_T(c)$$
where $d_T(c)$ is the depth of character $c$ in the prefix tree.

#### Greedy Strategy:
Maintain a min-priority queue (min-heap). Repeatedly extract the two nodes with the lowest frequencies, merge them into a parent node with sum frequency, and reinsert into the heap.

#### Matroid / Prefix Property:
Because no codeword is a prefix of another (prefix-free condition), the compressed bitstream is decoded unambiguously without lookahead delimiters in linear time $O(\text{bits})$.

---

## 4. EXPERIMENTAL BENCHMARKING & COMPLEXITY ANALYSIS

### 4.1 Theoretical Complexity Summary (Question 5 Table)
| Algorithm | Module Focus | Time Complexity | Space Complexity | Dominant Computational Step |
| :--- | :--- | :---: | :---: | :--- |
| **Fractional Knapsack** | Resource Allocation | $\mathbf{O(n \log n)}$ | $\mathbf{O(n)}$ | Sorting items by ratio ($v_i/w_i$) |
| **Activity Selection** | Task Scheduling | $\mathbf{O(n \log n)}$ | $\mathbf{O(n)}$ | Sorting activities by finish time ($f_i$) |
| **Huffman Coding** | Data Compression | $\mathbf{O(n \log n)}$ | $\mathbf{O(n)}$ | $n-1$ min-heap extractions & insertions |

### 4.2 Empirical Benchmarking Results (`../data_csv/benchmark_results.csv`)
The algorithms were executed across growing problem sizes ($n = 10$ to $n = 10,000$). Execution times and peak memory consumption were recorded using Python's high-resolution `time.perf_counter()` and `tracemalloc` profilers:

| Input Size ($n$) | Knapsack Time (ms) | Knapsack Mem (KB) | Activity Time (ms) | Activity Mem (KB) | Huffman Time (ms) | Huffman Mem (KB) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **10** | 0.20 ms | 2.75 KB | 0.14 ms | 2.48 KB | 0.45 ms | 2.92 KB |
| **50** | 0.57 ms | 7.41 KB | 1.03 ms | 10.68 KB | 2.27 ms | 8.00 KB |
| **100** | 2.37 ms | 14.35 KB | 1.31 ms | 20.27 KB | 1.28 ms | 10.97 KB |
| **250** | 4.96 ms | 41.91 KB | 5.93 ms | 54.14 KB | 5.28 ms | 19.46 KB |
| **500** | 10.96 ms | 82.68 KB | 9.67 ms | 110.04 KB | 5.82 ms | 23.88 KB |
| **1,000** | 19.91 ms | 166.93 KB | 21.13 ms | 223.14 KB | 7.11 ms | 31.75 KB |
| **2,500** | 48.05 ms | 431.63 KB | 63.91 ms | 564.02 KB | 5.02 ms | 50.90 KB |
| **5,000** | 131.60 ms | 836.10 KB | 109.21 ms | 1,126.13 KB | 11.16 ms | 84.16 KB |
| **10,000** | 332.03 ms | 1,923.63 KB | 213.48 ms | 2,261.45 KB | 25.95 ms | 151.36 KB |

### 4.3 Analysis of Empirical Curves:
* **Time Scalability:** As plotted in `../graphes/performance_comparison.png`, the runtime curve perfectly mirrors the theoretical $c \cdot n \log_2 n$ curve. At $n = 10,000$, total execution time for all modules combined remains under **0.58 seconds**, demonstrating production-grade scalability.
* **Memory Footprint:** As plotted in `../graphes/memory_usage_comparison.png`, peak memory scales strictly linearly ($O(n)$), requiring under **2.3 MB** even at 10,000 elements.

---

## 5. GENERATED VISUALIZATIONS OVERVIEW (QUESTION 6)

The system automatically generates 6 high-resolution charts saved in the `../graphes/` directory:

1. **`../graphes/knapsack_allocation.png`**: Dual-subplot graphic showing:
   - Bar chart of allocation percentages ($100\%$ for Gold, Platinum, Silver, and $33.3\%$ for Bronze).
   - Donut chart displaying the proportional weight saturation of the knapsack ($50/50\text{ kg}$) yielding a maximum profit of **$280.00**.
2. **`../graphes/activity_timeline.png`**: Gantt-style schedule displaying all 8 candidate activities, highlighting the 3 mutually compatible selected tasks (**A1 [1→4]**, **A4 [5→7]**, **A8 [8→11]**) in emerald green, while graying out overlapping conflicts.
3. **`../graphes/huffman_compression.png`**: Bar chart comparing character frequency versus assigned bit lengths. Frequently occurring characters (such as `'a'` with frequency 5) receive compact 1-bit codes, while rare characters receive 3-bit codes.
4. **`../graphes/huffman_tree.png`**: Hierarchical binary tree diagram visualizing root frequency 11, internal decision nodes, left (`0`) and right (`1`) branches, and colored leaf nodes.
5. **`../graphes/performance_comparison.png`**: Runtime growth curve comparing empirical execution against the theoretical $O(n \log n)$ benchmark.
6. **`../graphes/memory_usage_comparison.png`**: Peak memory allocation graph showing strict linear $O(n)$ behavior.

---

## 6. PRACTICAL REAL-WORLD APPLICATIONS

1. **Cloud Computing Resource Slicing (Fractional Knapsack):**
   - Cloud providers (AWS EC2, Google Cloud Compute) allocate fractional virtual CPUs, RAM bursts, and network bandwidth from physical hypervisors to maximize tenant yield.
2. **University & Enterprise Scheduling (Activity Selection):**
   - Automated room reservation, lecture hall allocation, conference room scheduling, and CPU pipeline instruction dispatching where tasks cannot share a single physical executor concurrently.
3. **Multimedia & Telecom Compression (Huffman Coding):**
   - Huffman coding serves as the entropy-encoding backend for ubiquitous compression formats including **JPEG** image compression, **MP3** audio, **GZIP**, and **PKZIP** (`.zip` archives).

---

## 7. KEY OBSERVATIONS: WHEN DOES GREEDY FAIL?

A critical insight in algorithmic design is recognizing problems where greedy heuristics **fail** to guarantee global optimality:

### The 0/1 Knapsack Breakdown:
When items cannot be divided (items must be taken whole or left behind), the greedy value-to-weight ratio strategy fails catastrophically:
* **Example:** Knapsack capacity $W = 50$.
  * Item 1: Weight = 10, Value = 60 (Ratio = 6.0)
  * Item 2: Weight = 20, Value = 100 (Ratio = 5.0)
  * Item 3: Weight = 30, Value = 120 (Ratio = 4.0)
* **Greedy Choice (0/1):** Takes Item 1 ($w=10$), then Item 2 ($w=20$). Total weight = 30. Item 3 ($w=30$) cannot fit!
  $$\text{Greedy Profit} = 60 + 100 = \mathbf{\$160}$$
* **Optimal Solution (Dynamic Programming):** Take Item 2 and Item 3. Total weight = $20 + 30 = 50$.
  $$\text{Optimal Profit} = 100 + 120 = \mathbf{\$220}$$
* **Conclusion:** The greedy choice fails because leaving unoccupied capacity prevents higher-value combinations. The 0/1 Knapsack problem requires **Dynamic Programming** ($O(n \cdot W)$ pseudo-polynomial time), which explores overlapping subproblem choices as studied in Lab 4.

---

## 8. CONCLUSION

Lab 3 successfully developed, validated, and benchmarked the **Smart Resource Allocation and Scheduling System**. By applying the greedy paradigm to Fractional Knapsack, Activity Selection, and Huffman Coding, the system achieves:
1. Guaranteed global optimality through mathematically verified exchange arguments.
2. Near-instantaneous computation ($O(n \log n)$ time complexity).
3. Minimal memory footprint ($O(n)$ space complexity).
4. Comprehensive visualization dashboards and automated reporting.

---
**Report Prepared & Submitted By:**  
**Bhavya Rattan**  
Roll Number: **2401201004**  
BCA (Artificial Intelligence & Data Science), SOET  
K.R. Mangalam University, Gurugram, Haryana
