"""Small domain types shared by the planner and simulator."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

Cell: TypeAlias = tuple[int, int]


@dataclass(frozen=True)
class Scenario:
    """A rectangular map with a fixed robot start and destination."""

    name: str
    description: str
    width: int
    height: int
    start: Cell
    goal: Cell
    obstacles: frozenset[Cell]


@dataclass(frozen=True)
class RunMetrics:
    """Metrics captured from one deterministic simulation run."""

    scenario: str
    status: str
    planned_cells: int
    steps_taken: int
    collisions: int
    efficiency: float

    def as_dict(self) -> dict[str, str | int | float]:
        return {
            "scenario": self.scenario,
            "status": self.status,
            "planned_cells": self.planned_cells,
            "steps_taken": self.steps_taken,
            "collisions": self.collisions,
            "efficiency": round(self.efficiency, 3),
        }
