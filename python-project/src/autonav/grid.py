"""Grid occupancy map and legal movement rules."""

from __future__ import annotations

from dataclasses import dataclass

from .models import Cell, Scenario

CARDINAL_DIRECTIONS: tuple[Cell, ...] = ((0, -1), (1, 0), (0, 1), (-1, 0))


@dataclass(frozen=True)
class GridMap:
    width: int
    height: int
    obstacles: frozenset[Cell]

    @classmethod
    def from_scenario(cls, scenario: Scenario) -> "GridMap":
        return cls(scenario.width, scenario.height, scenario.obstacles)

    def in_bounds(self, cell: Cell) -> bool:
        x, y = cell
        return 0 <= x < self.width and 0 <= y < self.height

    def is_free(self, cell: Cell) -> bool:
        return self.in_bounds(cell) and cell not in self.obstacles

    def neighbors(self, cell: Cell) -> tuple[Cell, ...]:
        """Return free four-connected neighbors in a stable order.

        Four-connected movement deliberately avoids diagonal corner cutting,
        keeping this beginner simulator's geometry and safety checks clear.
        """
        x, y = cell
        candidates = tuple((x + dx, y + dy) for dx, dy in CARDINAL_DIRECTIONS)
        return tuple(candidate for candidate in candidates if self.is_free(candidate))
