# System architecture

## In one sentence

The simulator gives a virtual robot a known occupancy grid, computes a shortest safe route with A*, and moves one cell at a time while checking every action against the map.

## Data flow

```text
JSON scenario
    │  dimensions, start, goal, wall rectangles
    ▼
Scenario loader ── validates map and endpoints
    ▼
GridMap ────────── free / blocked cells + legal four-way neighbors
    ├─────────────────────────────┐
    ▼                             ▼
A* planner                    Simulator state machine
    │  ordered route              │  start / pause / step / reset
    └──────────────┬──────────────┘
                   ▼
        Safety check before each move
                   │
          ┌────────┴─────────┐
          ▼                  ▼
   Pygame visualization   Headless CLI
   robot, map, route      JSON run metrics
```

## Modules

| Module | Responsibility | Input → output |
|---|---|---|
| `data/scenarios/*.json` | Defines a map in editable coordinates. A wall is `[x, y, width, height]`. | JSON → scenario definition |
| `autonav.scenarios` | Loads the JSON, expands walls to occupied cells, and checks endpoints. | scenario file → `Scenario` |
| `autonav.grid` | Applies map bounds and legal movement rules. The robot uses cardinal moves only. | cell → free neighbors |
| `autonav.planner` | Runs A* with unit edge costs and Manhattan distance. | map + start + goal → shortest cell route or no route |
| `autonav.simulator` | Owns robot position, run state, step count, collision count, and safety checks. | route + actions → run metrics |
| `autonav.visualizer` | Draws the grid and reads keyboard input. It contains no planning rules. | simulator state → window |
| `autonav.cli` | Starts the graphical viewer, lists scenarios, or runs the same simulation without a window. | command line → window or JSON |

## Decision loop

1. Load and validate a static grid map.
2. Check that start and goal are in bounds and not blocked.
3. Search for a route. Here, route planning happens once because the map is static.
4. The controller asks the simulator to move to the next route cell.
5. The simulator checks that the next cell is still free before moving.
6. Stop on arrival, a blocked action, or a missing route; report the outcome.

The collision check is intentionally independent of A*. This separation is useful in real robotics, where a route proposal and the low-level safety gate should not be the same code path.

## Assumptions and limits

- This is a deterministic 2D teaching simulation, not a physical robot controller.
- The map is synthetic and fully known. There is no camera, LiDAR, object-detection model, localization uncertainty, or learned policy in version 1.
- The word “AI” here refers to classical search and decision algorithms, not machine learning.
- Four-connected movement avoids diagonal corner cutting. The robot is a point on a grid; it has no turning radius, speed dynamics, or footprint.
- The current sample maps are static. The per-step safety gate is present, but dynamic obstacle sensing and route replanning are future work.
- A* is optimal for this grid because every move costs one and Manhattan distance never overestimates the remaining four-way distance.

## How this relates to real autonomy

An industrial autonomy stack adds sensors, calibration, perception, localization, uncertainty-aware world models, dynamic prediction, behavior planning, trajectory generation, vehicle/robot control, safety monitors, and hardware-in-the-loop validation. This project isolates the map-to-route-to-action core so a learner can understand and test it before taking on those larger systems.
