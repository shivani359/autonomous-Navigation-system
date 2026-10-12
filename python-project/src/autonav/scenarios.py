"""Load editable JSON scenarios from the repository's data directory."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import Cell, Scenario

SCENARIO_DIR = Path(__file__).resolve().parents[2] / "data" / "scenarios"


def _cell(value: Any, field: str) -> Cell:
    if (
        not isinstance(value, list)
        or len(value) != 2
        or not all(isinstance(part, int) for part in value)
    ):
        raise ValueError(f"Scenario field '{field}' must be [x, y] integers.")
    return (value[0], value[1])


def load_scenario(path: Path) -> Scenario:
    """Parse and validate one map definition."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Could not read scenario '{path}': {exc}") from exc

    required = {"name", "description", "width", "height", "start", "goal", "walls"}
    if not isinstance(data, dict) or not required.issubset(data):
        raise ValueError(f"Scenario '{path.name}' is missing required fields.")

    width, height = data["width"], data["height"]
    if not isinstance(width, int) or not isinstance(height, int) or min(width, height) < 2:
        raise ValueError("Scenario width and height must be integers of at least 2.")

    obstacles: set[Cell] = set()
    walls = data["walls"]
    if not isinstance(walls, list):
        raise ValueError("Scenario 'walls' must be a list of rectangles.")
    for rect in walls:
        if (
            not isinstance(rect, list)
            or len(rect) != 4
            or not all(isinstance(part, int) for part in rect)
        ):
            raise ValueError("Each wall must be [x, y, width, height] integers.")
        x, y, wall_width, wall_height = rect
        if wall_width < 1 or wall_height < 1:
            raise ValueError("Wall width and height must be positive.")
        for cell_y in range(y, y + wall_height):
            for cell_x in range(x, x + wall_width):
                obstacles.add((cell_x, cell_y))

    scenario = Scenario(
        name=str(data["name"]),
        description=str(data["description"]),
        width=width,
        height=height,
        start=_cell(data["start"], "start"),
        goal=_cell(data["goal"], "goal"),
        obstacles=frozenset(obstacles),
    )

    for label, endpoint in (("start", scenario.start), ("goal", scenario.goal)):
        x, y = endpoint
        if not (0 <= x < width and 0 <= y < height):
            raise ValueError(f"Scenario {label} {endpoint} is outside the map.")
        if endpoint in scenario.obstacles:
            raise ValueError(f"Scenario {label} {endpoint} overlaps a wall.")
    return scenario


def available_scenarios() -> dict[str, Scenario]:
    """Return all scenario files, keyed by their filename stem."""
    if not SCENARIO_DIR.is_dir():
        raise FileNotFoundError(f"Scenario directory not found: {SCENARIO_DIR}")
    scenarios = {
        path.stem: load_scenario(path)
        for path in sorted(SCENARIO_DIR.glob("*.json"))
    }
    if not scenarios:
        raise FileNotFoundError(f"No *.json scenarios found in {SCENARIO_DIR}")
    return scenarios


def scenario_by_key(key: str) -> Scenario:
    scenarios = available_scenarios()
    try:
        return scenarios[key]
    except KeyError as exc:
        choices = ", ".join(scenarios)
        raise ValueError(f"Unknown scenario '{key}'. Choose one of: {choices}") from exc
