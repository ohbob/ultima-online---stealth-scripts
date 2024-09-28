from py_stealth import *
import time
from typing import List, Tuple
from itertools import product

BAD_LOCATIONS: List[Tuple[int, int, int, int]] = [
    (1600, 2923, 1624, 2898), (1515, 2923, 1533, 2934), (1515, 2981, 1533, 2969),
    (3216, 530, 3247, 592), (3243, 541, 3268, 583)
]

def generate_bad_locations() -> set[Tuple[int, int]]:
    return {
        (x, y)
        for x1, y1, x2, y2 in BAD_LOCATIONS
        for x, y in product(
            range(min(x1, x2), max(x1, x2) + 1),
            range(min(y1, y2), max(y1, y2) + 1)
        )
    }

def set_bad_locations() -> None:
    start_time = time.perf_counter()
    
    AddToSystemJournal("Clearing existing bad locations")
    ClearBadLocationList()
    
    AddToSystemJournal("Generating bad locations")
    bad_locations = generate_bad_locations()
    
    AddToSystemJournal(f"Total bad locations to add: {len(bad_locations)}")
    
    for x, y in bad_locations:
        SetBadLocation(x, y)
    
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    
    AddToSystemJournal(f"Finished adding bad locations in {execution_time:.4f} seconds")

if __name__ == "__main__":
    loop_count = 0
    while True:
        loop_start_time = time.perf_counter()
        loop_count += 1
        
        print(f"Starting bad location update (Loop {loop_count})")
        set_bad_locations()
        GetHP(Self())
        loop_end_time = time.perf_counter()
        loop_duration = loop_end_time - loop_start_time
        print(f"Finished bad location update (Loop {loop_count})")
        print(f"Loop duration: {loop_duration:.4f} seconds")
        
       