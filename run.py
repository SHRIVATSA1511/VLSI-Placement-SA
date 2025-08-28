#! C:\Users\shriv\OneDrive\Documents\Simulated_anneling\myenv\Scripts\python.exe

import random
import math
import matplotlib.pyplot as plt
from typing import Dict, Tuple, List

# size of each rectangle
modules: Dict[str, Tuple[int, int]] = {
    "A": (2, 3),
    "B": (3, 2),
    "C": (2, 2),
    "D": (1, 4),
    "E": (3, 3),
    "F": (2, 4),
    "G": (4, 2),
    "H": (2, 3),
    "I": (3, 1),
    "J": (2, 2),
}

# Relation Between the Modules
nets: List[Tuple[str, str]] = [
    ("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"),
    ("E", "F"), ("F", "G"), ("G", "H"),
    ("H", "I"), ("I", "J"), ("E", "A"),
    ("B", "F"), ("C", "H"), ("D", "J")
]

# chip dimensions(20x20)
CHIPLENGTH: int = 20
CHIPWIDTH: int = 20


def random_placement(mods: Dict[str, Tuple[int, int]]) -> Dict[str, Tuple[int, int]]:
    """
    Randomly places the modules within the chip area.

    Returns:
       (x, y) bottom-left coordinates.
    """
    placement: Dict[str, Tuple[int, int]] = {}

    for m, (w, h) in mods.items():
        x: int = random.randint(0, CHIPLENGTH - w)
        y: int = random.randint(0, CHIPWIDTH - h)

        placement[m] = (x, y)

    return placement


def cost(placement: Dict[str, Tuple[int, int]]) -> float:
    """
    Computes the cost of a placement.

    Cost = total wirelength + overlap penalty.

    Returns:
         Cost of the placement.
    """
    wl: float = 0.0
    # Wirelength = Manhattan distance between the center of the modules.
    for a, b in nets:
        xa, ya = placement[a]
        xb, yb = placement[b]
        wa, ha = modules[a]
        wb, hb = modules[b]
        ca: Tuple[float, float] = (xa + wa/2, ya + ha/2)
        cb: Tuple[float, float] = (xb + wb/2, yb + hb/2)
        wl += abs(ca[0] - cb[0]) + abs(ca[1] - cb[1])

    # Overlap penalty
    overlap: float = 0.0
    mods_list: List[Tuple[str, Tuple[int, int]]] = list(placement.items())
    for i in range(len(mods_list)):

        m1, (x1, y1) = mods_list[i]
        w1, h1 = modules[m1]

        for j in range(i+1, len(mods_list)):

            m2, (x2, y2) = mods_list[j]
            w2, h2 = modules[m2]

            if not (x1+w1 <= x2 or x2+w2 <= x1 or y1+h1 <= y2 or y2+h2 <= y1):
                overlap += 10
    return wl + overlap


def randommove(placement: Dict[str, Tuple[int, int]]) -> Dict[str, Tuple[int, int]]:
    """
    Generate a new placement by moving a single random module.

    Returns:
        New placement after moving one module.
    """
    new_place: Dict[str, Tuple[int, int]] = placement.copy()
    m: str = random.choice(list(modules.keys()))
    w, h = modules[m]
    new_place[m] = (
        random.randint(0, CHIPLENGTH - w),
        random.randint(0, CHIPWIDTH - h)
    )
    return new_place


def plotplacement(placement: Dict[str, Tuple[int, int]], title: str = "") -> None:
    """
    Plot the current placement of modules on the chip.

    """
    plt.figure(figsize=(6, 6))
    ax = plt.gca()
    ax.set_xlim(0, CHIPLENGTH)
    ax.set_ylim(0, CHIPWIDTH)

    for m, (x, y) in placement.items():
        w, h = modules[m]
        rect = plt.Rectangle((x, y), w, h, fill=True, alpha=0.4, label=m)
        ax.add_patch(rect)
        plt.text(x+w/2, y+h/2, m, ha="center",
                 va="center", fontsize=10, weight="bold")

    plt.title(title)
    plt.grid(True)
    plt.show()

# Simulated Annealing


def simulated_annealing(
    max: int = 50000,
    T_start: float = 100.0,
    cooling: float = 0.995
) -> Tuple[Dict[str, Tuple[int, int]], float, List[float]]:
    """
    Performs Simulated Annealing for VLSI floorplanning.

        Arguments:
        max: Maximum iterations for the annealing process.
        T_start : Starting temperature.
        cooling : Cooling factor per iteration.

    Returns:
            - Best placement found
            - Best cost value
            - Cost history across iterations
    """
    placement: Dict[str, Tuple[int, int]] = random_placement(modules)
    best: Dict[str, Tuple[int, int]] = placement
    T: float = T_start
    best_cost: float = cost(placement)

    cost_history: List[float] = []

    for i in range(max):
        new_place = randommove(placement)
        c_old: float = cost(placement)
        c_new: float = cost(new_place)

        if c_new < c_old or random.random() < math.exp((c_old - c_new)/T):
            placement = new_place

        if cost(placement) < best_cost:
            best = placement
            best_cost = cost(placement)

        cost_history.append(best_cost)
        T *= cooling  # cooling schedule

    return best, best_cost, cost_history


# --- Run Simulated Annealing ---
best_placement, best_c, cost_history = simulated_annealing()
print("Best Cost:", best_c)
print("Best Placement:", best_placement)

# --- Plot cost convergence ---
plt.figure(figsize=(7, 4))
plt.plot(cost_history, label="Best Cost")
plt.xlabel("Iteration")
plt.ylabel("Cost")
plt.title("Simulated Annealing Cost Convergence")
plt.legend()
plt.grid(True)
plt.show()

# --- Plot final placement ---
plotplacement(best_placement, title=f"Final Placement (Cost={best_c})")
