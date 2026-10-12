# AI-Based Autonomous Navigation System

A laptop-friendly 2D robot navigation project built with Python, Pygame, and A*. A virtual delivery robot plans a shortest route around warehouse-style obstacles, checks every move before executing it, and reports repeatable run metrics.

> **Scope:** This project demonstrates classical, map-based path planning. Its environment is synthetic and fully known. It does not use a camera, YOLO, a learned model, ROS, a physical robot, or safety-certified controls.

## Demo

Run the interactive simulator locally:

```bash
python main.py --scenario warehouse
```

Press **Space** to start or pause, **R** to reset, and **Esc** to close. Other maps are `slalom` and `narrow-corridor`.

## Quick start

Requires Python 3.10 or newer.

### macOS / Linux

```bash
cd python-project
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
python main.py --scenario warehouse
```

### Windows PowerShell

```powershell
cd python-project
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
python main.py --scenario warehouse
```

## Run without a graphical window

Headless runs use the same A* planner and simulation logic as the visual application:

```bash
python -m autonav.cli --list-scenarios
python -m autonav.cli --scenario warehouse --headless
python -m autonav.cli --scenario slalom --headless
python -m autonav.cli --scenario narrow-corridor --headless
```

Example output:

```json
{
  "scenario": "Warehouse Aisles",
  "status": "completed",
  "planned_cells": 45,
  "steps_taken": 45,
  "collisions": 0,
  "efficiency": 1.0
}
```

The exact path length depends on the scenario map. Efficiency is planned moves divided by moves taken; `1.0` means the simulated robot followed the planned route without extra moves. This metric is descriptive for this deterministic exercise, not a real-world performance guarantee.

## Run tests

```bash
python -m unittest discover -s tests -v
```

Tests cover shortest-route behavior, blocked/unreachable cases, endpoint validation, route execution, reset/pause state, and all bundled scenarios.

## What happens in the simulation?

1. A JSON scenario defines the grid, start, goal, and rectangular obstacles.
2. The loader expands and validates the obstacle map.
3. A* searches four-connected neighboring cells using unit move costs and Manhattan distance.
4. The simulator advances the robot one cell per action and checks that the next cell is free.
5. Pygame displays the route, robot, goal, run state, and metrics; the CLI can also print JSON without a window.

## Project choices

| Version | Tools | Difficulty | GPU | Result |
|---|---|---|---|---|
| **A — this project** | Python, Pygame, A*, JSON | Beginner | No | Interactive 2D route planning with automated tests |
| B | ROS 2 + Gazebo/Webots | Intermediate | Usually no for basic simulation | Middleware nodes, localization and more realistic sensors |
| C | CARLA + OpenCV + PyTorch / YOLO | Advanced | Recommended for deep-learning workloads | 3D driving scenes and camera-based experiments |

Option A is the recommended starting point: it makes the core planning behavior visible and reproducible without a GPU or hardware. See [the student project guide](docs/project-guide.md) for the complete explanation, industry context, implementation phases, GitHub steps, and resume strategy. See [the architecture guide](docs/architecture.md) for module boundaries, data flow, assumptions, and limitations.

## Add your own map

Copy a JSON file in `data/scenarios/`, change its `name`, `description`, `width`, `height`, `start`, and `goal`, then add rectangles in `walls`:

```json
{
  "name": "My Map",
  "description": "A short test of aisle navigation.",
  "width": 20,
  "height": 12,
  "start": [1, 1],
  "goal": [18, 10],
  "walls": [[6, 0, 2, 8], [12, 4, 2, 8]]
}
```

A wall is `[x, y, width, height]`. The start and goal must be inside the map and not inside any wall. The new file stem becomes the `--scenario` key.

## Repository map

```text
data/scenarios/  Editable obstacle maps
docs/            System architecture and student/portfolio guide
outputs/runs/    Optional run evidence
src/autonav/     Planner, map, simulator, CLI, and Pygame visualizer
tests/           Unit tests using Python's standard library
```

## GitHub portfolio checklist

1. Create a GitHub repository named `AI-Autonomous-Navigation-System`.
2. Run `git init`, `git add .`, and `git commit -m "Build 2D autonomous navigation simulator"` from this folder.
3. Set the repository's `main` branch and add the GitHub remote; push with `git push -u origin main`.
4. Record a short screen capture of two scenarios and link it near the top of this README.
5. Include an example headless run and keep the setup reproducible from a fresh clone.
6. Add at least one scenario of your own and explain the edge case it tests.
7. Be precise in interviews: this project uses classical A*, synthetic maps, and deterministic simulation—not learned perception or real-vehicle control.

Example resume bullet:

> Built a Python/Pygame autonomous-navigation simulator with A* shortest-path planning, validated obstacle maps, per-step collision checks, and deterministic headless metrics; tested route behavior across multiple scenarios.

## Next learning steps

- Add dynamic obstacles and replan when the route is blocked.
- Add a robot footprint and turning constraints.
- Add a local occupancy map generated from simulated range measurements.
- Compare A* with Dijkstra and BFS using the same maps.
- Port one navigation component to a ROS 2 node and a Webots/Gazebo environment.

## License

This project is provided for learning and portfolio demonstration. Add a license file before inviting reuse under specific terms.
