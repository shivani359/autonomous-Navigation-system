"""Deterministic A* path planner for a four-connected occupancy grid."""

from __future__ import annotations

import heapq
from itertools import count

from .grid import GridMap
from .models import Cell


def manhattan_distance(a: Cell, b: Cell) -> int:
    """Admissible heuristic for unit-cost cardinal moves."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid: GridMap, start: Cell, goal: Cell) -> list[Cell] | None:
    """Return the shortest route, including start and goal, or ``None``.

    Raises:
        ValueError: if either endpoint is outside the map or blocked.
    """
    if not grid.is_free(start):
        raise ValueError(f"Start cell {start} is outside the map or blocked.")
    if not grid.is_free(goal):
        raise ValueError(f"Goal cell {goal} is outside the map or blocked.")
    if start == goal:
        return [start]

    sequence = count()
    frontier: list[tuple[int, int, int, Cell]] = []
    heapq.heappush(frontier, (manhattan_distance(start, goal), 0, next(sequence), start))
    came_from: dict[Cell, Cell] = {}
    cost_so_far: dict[Cell, int] = {start: 0}
    visited: set[Cell] = set()

    while frontier:
        _, current_cost, _, current = heapq.heappop(frontier)
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            path = [goal]
            while path[-1] != start:
                path.append(came_from[path[-1]])
            path.reverse()
            return path

        for neighbor in grid.neighbors(current):
            new_cost = current_cost + 1
            if new_cost >= cost_so_far.get(neighbor, float("inf")):
                continue
            cost_so_far[neighbor] = new_cost
            came_from[neighbor] = current
            estimate = new_cost + manhattan_distance(neighbor, goal)
            heapq.heappush(frontier, (estimate, new_cost, next(sequence), neighbor))

    return None
