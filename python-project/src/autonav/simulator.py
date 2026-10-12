"""Discrete-time robot state machine used by both GUI and headless runs."""

from __future__ import annotations

from dataclasses import dataclass

from .grid import GridMap
from .models import Cell, RunMetrics, Scenario
from .planner import astar


@dataclass
class Simulator:
    scenario: Scenario

    def __post_init__(self) -> None:
        self.grid = GridMap.from_scenario(self.scenario)
        self.reset()

    def reset(self) -> None:
        self.robot: Cell = self.scenario.start
        self.route = astar(self.grid, self.scenario.start, self.scenario.goal)
        self.route_index = 0
        self.steps_taken = 0
        self.collisions = 0
        self.status = "ready" if self.route is not None else "no_path"

    def start(self) -> None:
        if self.status == "completed":
            self.reset()
        if self.route is None:
            self.status = "no_path"
        elif self.robot == self.scenario.goal:
            self.status = "completed"
        else:
            self.status = "running"

    def pause(self) -> None:
        if self.status == "running":
            self.status = "paused"

    def step(self) -> bool:
        """Advance one safe cell. Return whether the robot moved."""
        if self.status != "running" or self.route is None:
            return False
        next_index = self.route_index + 1
        if next_index >= len(self.route):
            self.status = "completed"
            return False

        next_cell = self.route[next_index]
        # Re-check the next cell at action time. This is a safety invariant even
        # though the current educational maps have static obstacles.
        if not self.grid.is_free(next_cell):
            self.collisions += 1
            self.status = "blocked"
            return False

        self.robot = next_cell
        self.route_index = next_index
        self.steps_taken += 1
        if self.robot == self.scenario.goal:
            self.status = "completed"
        return True

    def metrics(self) -> RunMetrics:
        planned_steps = max(0, len(self.route) - 1) if self.route is not None else 0
        efficiency = (planned_steps / self.steps_taken) if self.steps_taken else 0.0
        return RunMetrics(
            scenario=self.scenario.name,
            status=self.status,
            planned_cells=planned_steps,
            steps_taken=self.steps_taken,
            collisions=self.collisions,
            efficiency=efficiency,
        )
