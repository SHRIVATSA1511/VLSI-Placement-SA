# Chip Floor-planning Optimization with Simulated Annealing
This repository contains a Python implementation of the Simulated Annealing optimization algorithm for the traditional chip floor-planning problem. The goal of the project is to achieve an optimal, non-overlapping placement of electronic modules on a chip die by optimizing a weighted sum of wirelength cost and overlap penalties.

## Theoretical Background
Chip floor-planning is a combinatorial optimization problem in which the objective is to place a collection of rectangular modules on a specified region.

The primary objective:

1.Wirelength between connected modules (nets) is minimized.<br/>
2.Module overlaps are eliminated (or strongly penalized)..<br/>
3.Placement is within the chip boundary.<br/>

An optimal solution is expensive because there are such a large number of potential arrangements.

# Simulated Annealing
Simulated annealing is an optimization algorithm that explores solution space for the global optimum by random sampling. It searches the solution space by accepting both lower-cost and, with a given probability, higher-cost solutions to not remain trapped in a local optimum. The probability for accepting a higher solution reduces as the simulation "cools" so that the algorithm converges to a high-quality global optimum.

# Implementation
This project approaches the chip floor-planning problem as a combinatorial optimization task. This method balances two competing objectives: keeping modules physically separated while minimizing the wiring distance between them.

Instead of exhaustively evaluating every possible arrangement—which becomes computationally infeasible as the number of modules grows—we rely on Simulated Annealing (SA), a search method inspired by thermodynamics.

## Key aspects of the methodology:
### Objective Function:
The cost function evaluates the quality of a layout by adding:</b>
1.The total wirelength of all interconnections.</b>
2.A penalty score proportional to the number of overlaps.

### Exploration of the Solution Space:
Neighborhoods are created by moving one module randomly. This provides small, controlled moves that sequentially explore good layouts.

### Acceptance of New Solutions:
The algorithm sometimes accepts worse layouts to prevent convergence before the optimization is complete. The probability of such acceptance diminishes as the system "cools," mirroring the annealing of metals.
