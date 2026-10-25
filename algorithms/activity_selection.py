"""
Task Scheduling Module: Activity Selection Algorithm
Greedy Strategy: Earliest Finish Time First
Time Complexity: O(n log n)
Space Complexity: O(n)
Author: Bhavya Rattan (Roll No: 2401201004)
"""

from typing import List, Dict, Union


class Activity:
    def __init__(self, name: str, start: float, finish: float):
        self.name = name
        self.start = float(start)
        self.finish = float(finish)
        self.duration = self.finish - self.start

    def __repr__(self):
        return f"Activity({self.name}, [{self.start} -> {self.finish}], dur={self.duration})"


def activity_selection(activities: List[Union[Dict, Activity]]) -> List[Dict]:
    """
    Selects the maximum number of mutually compatible, non-overlapping activities.
    
    Parameters:
        activities: List of activity dicts (with 'name', 'start', 'finish') or Activity instances.
        
    Returns:
        List of selected activity dictionaries sorted in execution order.
    """
    if not activities:
        return []

    # Standardize input to list of Activity objects
    parsed_acts: List[Activity] = []
    for a in activities:
        if isinstance(a, Activity):
            parsed_acts.append(a)
        else:
            parsed_acts.append(Activity(a["name"], a["start"], a["finish"]))

    # Greedy Choice: Sort activities in ASCENDING order of FINISH times
    sorted_acts = sorted(parsed_acts, key=lambda a: a.finish)

    selected: List[Dict] = []
    # Always select the first activity (earliest finish time)
    first = sorted_acts[0]
    selected.append({"name": first.name, "start": first.start, "finish": first.finish, "duration": first.duration})
    last_finish = first.finish

    # Iterate through the rest and pick compatible activities
    for act in sorted_acts[1:]:
        if act.start >= last_finish:
            selected.append({"name": act.name, "start": act.start, "finish": act.finish, "duration": act.duration})
            last_finish = act.finish

    return selected


if __name__ == "__main__":
    sample_activities = [
        {"name": "A1", "start": 1, "finish": 4},
        {"name": "A2", "start": 3, "finish": 5},
        {"name": "A3", "start": 0, "finish": 6},
        {"name": "A4", "start": 5, "finish": 7},
        {"name": "A5", "start": 3, "finish": 9},
        {"name": "A6", "start": 5, "finish": 9},
        {"name": "A7", "start": 6, "finish": 10},
        {"name": "A8", "start": 8, "finish": 11},
    ]
    scheduled = activity_selection(sample_activities)
    print(f"--- Task Scheduling: Selected {len(scheduled)} Activities ---")
    for act in scheduled:
        print(f"  {act['name']}: Start={act['start']}, Finish={act['finish']} (Duration={act['duration']})")
