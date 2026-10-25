"""
DAA Lab 3: Smart Resource Allocation and Scheduling System using Greedy Algorithms
Algorithms Package
Author: Bhavya Rattan (Roll No: 2401201004)
Course: Design and Analysis of Algorithms (ENCA301)
Faculty: Dr. Aarti
"""

from .fractional_knapsack import fractional_knapsack, KnapsackItem
from .activity_selection import activity_selection, Activity
from .huffman_coding import huffman_encode, huffman_decode, build_huffman_tree, Node

__all__ = [
    "fractional_knapsack",
    "KnapsackItem",
    "activity_selection",
    "Activity",
    "huffman_encode",
    "huffman_decode",
    "build_huffman_tree",
    "Node",
]
