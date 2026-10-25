"""
Resource Allocation Module: Fractional Knapsack Algorithm
Greedy Strategy: Value-to-Weight Ratio Maximization
Time Complexity: O(n log n)
Space Complexity: O(n)
Author: Bhavya Rattan (Roll No: 2401201004)
"""

from typing import List, Dict, Tuple, Union


class KnapsackItem:
    def __init__(self, name: str, weight: float, value: float):
        self.name = name
        self.weight = float(weight)
        self.value = float(value)
        self.ratio = self.value / self.weight if self.weight > 0 else 0.0

    def __repr__(self):
        return f"Item({self.name}, w={self.weight}, v={self.value}, ratio={self.ratio:.2f})"


def fractional_knapsack(
    items: List[Union[Dict, KnapsackItem]], 
    capacity: float
) -> Tuple[float, List[Tuple[str, float, float, float]]]:
    """
    Computes the maximum achievable profit using Fractional Knapsack algorithm.
    
    Parameters:
        items: List of item dictionaries (with 'name', 'weight', 'value') or KnapsackItem instances.
        capacity: Maximum weight capacity of the knapsack.
        
    Returns:
        total_value: Maximum total value/profit achievable.
        allocation: List of tuples (item_name, fraction_taken, weight_taken, value_contributed).
    """
    if capacity <= 0 or not items:
        return 0.0, []

    # Standardize to list of KnapsackItem objects
    parsed_items: List[KnapsackItem] = []
    for it in items:
        if isinstance(it, KnapsackItem):
            parsed_items.append(it)
        else:
            parsed_items.append(KnapsackItem(it["name"], it["weight"], it["value"]))

    # Greedy Choice: Sort items in DESCENDING order of value-to-weight ratio
    sorted_items = sorted(parsed_items, key=lambda x: x.ratio, reverse=True)

    total_value = 0.0
    allocation: List[Tuple[str, float, float, float]] = []
    remaining_capacity = float(capacity)

    for item in sorted_items:
        if remaining_capacity <= 0:
            break

        if item.weight <= remaining_capacity:
            # Take the entire item (fraction = 1.0)
            fraction = 1.0
            weight_taken = item.weight
            val_taken = item.value
            total_value += val_taken
            remaining_capacity -= weight_taken
            allocation.append((item.name, fraction, weight_taken, val_taken))
        else:
            # Take a fraction of the item to fill the remaining capacity
            fraction = remaining_capacity / item.weight
            weight_taken = remaining_capacity
            val_taken = item.value * fraction
            total_value += val_taken
            allocation.append((item.name, fraction, weight_taken, val_taken))
            remaining_capacity = 0.0

    return total_value, allocation


if __name__ == "__main__":
    test_items = [
        {"name": "Gold", "weight": 10, "value": 60},
        {"name": "Silver", "weight": 20, "value": 100},
        {"name": "Bronze", "weight": 30, "value": 120},
    ]
    cap = 50
    max_val, details = fractional_knapsack(test_items, capacity=cap)
    print(f"--- Fractional Knapsack Allocation (Capacity: {cap}) ---")
    print(f"Maximum Achievable Profit: {max_val:.2f}")
    for name, frac, wt, val in details:
        print(f"  {name}: {frac*100:.1f}% taken | Weight: {wt:.1f} | Value: {val:.1f}")
