# Student project guide

## 1. What the project does

### Simple explanation

Imagine a small delivery robot in a warehouse. It knows which floor tiles are clear and which are blocked by shelves. You choose where it starts and where it must go. The software searches for a short route that avoids walls, then moves the virtual robot along that route. The screen shows the map, the planned route, the robot, and whether the run finished safely.

### Technical explanation

This is a deterministic, discrete-time, 2D grid-world navigation system. A scenario loader validates an occupancy grid, a four-connected A* search finds an optimal path under unit movement costs, and a state-machine simulator executes the route with an independent collision gate. Pygame visualizes the state; a headless command returns reproducible JSON metrics.

It solves a simplified version of the navigation problem: “Given a map, a start pose, and a destination, what collision-free sequence of local moves should the robot follow?”

## Why autonomous navigation matters

Robots and autonomous vehicles need to move toward goals without relying on a person to steer every action. Reliable navigation can increase throughput, reduce repetitive manual movement, reach hazardous or inaccessible areas, and make service more consistent. A real deployed system must also be safe, maintainable, observable, and tested against edge cases; finding a path is only one part of that responsibility.

## Real-world uses

- **Warehouse automation:** mobile robots carry totes, replenish picking areas, and share aisles with people and other robots.
- **Industrial robotics:** autonomous mobile robots move tools and parts between work cells, subject to restricted zones and right-of-way rules.
- **Delivery robots and smart mobility:** sidewalk robots and low-speed shuttles plan routes around mapped obstacles and changing pedestrian conditions.
- **Drones:** a flight stack reasons about obstacles and reachable trajectories in three dimensions; this grid project covers only the basic planning idea.
- **Autonomous vehicles:** production systems combine perception, localization, prediction, behavior planning, trajectory planning, and control. The demo implements only a tiny map-based planning slice.
- **Industrial safety:** safety-rated sensing, stop zones, speed limits, and independent safety controllers constrain where and how a robot may move. This teaching demo is not safety-certified.

Companies adapt navigation to their operating environment. They combine maps and sensor observations, assign goals, coordinate shared space, monitor performance, record failures, and validate updates in simulation before controlled real-world tests. The exact stack differs by robot, site, and safety requirements.

## The complete autonomy workflow (industry context)

1. **Perception:** turn sensor data into useful observations about the surroundings.
2. **Computer vision:** process camera images; for example, recognize a lane marking or an object.
3. **Object detection:** estimate object classes and bounding regions; a detector may identify a pallet, person, vehicle, or cone.
4. **Lane/path detection:** infer drivable or walkable space from markings, geometry, or a prebuilt map.
5. **Localization:** estimate where the robot is in the map. Real systems fuse sources such as wheel odometry, cameras, and LiDAR.
6. **Obstacle avoidance:** keep clearance from static or moving objects, including objects not present in the original map.
7. **Decision making:** choose a behavior such as proceed, yield, stop, turn, or request assistance.
8. **Path planning:** find a route through a map; this demo uses A* on a grid.
9. **Control/navigation:** convert a route or trajectory into motor or steering commands and check that the robot follows them.
10. **Simulation/testing:** exercise normal cases and failures repeatedly; compare metrics; then validate increasingly realistic models and hardware.

The selected beginner project uses a known, synthetic map. Its “perception” is a direct lookup of occupied grid cells, not computer vision or YOLO. This is deliberate: adding a pretrained detector before understanding maps and planning would add downloads, hardware demands, and failure modes without improving this first learning goal.

## 2. Three practical technology options

| Option | Tools | Difficulty | GPU? | Outcome |
|---|---|---:|---|---|
| **A — beginner (selected)** | Python, Pygame, standard-library A*, JSON maps, `unittest` | Beginner | No | A visible 2D robot routes around obstacles; repeatable command-line results and tests make a compact portfolio project. |
| **B — intermediate** | ROS 2, Gazebo or Webots, Python nodes, Nav2 or equivalent | Intermediate | Usually no for basic simulation | A more realistic robot workflow with separate nodes, sensors, localization, and a robotics middleware stack. Installation and operating-system compatibility take more time. |
| **C — advanced** | CARLA, Python, ROS bridge, OpenCV, PyTorch or a detector such as YOLO | Advanced | Recommended for deep-learning workloads; depends on model and resolution | Camera-based driving experiments in a 3D simulator, with substantially higher setup, compute, and debugging costs. |

**Best for a strong proof of work quickly:** Option A. It has visible output, understandable algorithms, named test scenarios, a clean install path, and no GPU/hardware dependency. The trade-off is clear: it demonstrates classical planning, not learned perception or full vehicle autonomy.

## 3. Architecture and data flow

See [architecture.md](architecture.md) for the block diagram, module responsibilities, decision loop, and limitations. In short: JSON map → validation → occupancy grid → A* route → safe one-cell actions → visualization and metrics.

## 4. Implementation phases

| Phase | What to do and why | Expected output | Common beginner mistakes | Completion check |
|---|---|---|---|---|
| 1. Set up Python | Use Python 3.10+ and a virtual environment so dependencies are isolated. | `python --version` works; `.venv` exists. | Installing to the system interpreter; using an incompatible Python version. | Activate the environment and run `python --version`. |
| 2. Install the project | Run `pip install -r requirements.txt` and `pip install -e .`. This installs Pygame and makes `autonav` importable. | Pygame and the local package are available. | Skipping editable install and then seeing `ModuleNotFoundError`. | `python -m autonav.cli --list-scenarios` lists three maps. |
| 3. Inspect scenarios | Read the JSON map dimensions, start/goal, and rectangular walls. Each wall is `[x, y, width, height]`. | You can explain how a map becomes blocked grid cells. | Putting a start or goal inside a wall; using coordinates outside the map. | The scenario loader starts successfully and validation errors are readable. |
| 4. Understand the planner | Trace A*: frontier priority, `g` cost, Manhattan heuristic, parent links, and route reconstruction. | A shortest route from start to goal, or an explicit no-route result. | Using a heuristic that overestimates; treating visited cells as always optimal with inconsistent costs. | `python -m unittest discover -s tests -v` passes planner tests. |
| 5. Run the visualization | Launch Pygame and start/pause/reset the robot. | A visible route and robot movement. | Expecting camera perception or physical robot motion from a static map demo. | Complete each sample map and inspect route length / collisions. |
| 6. Run headlessly | Run the deterministic CLI on all named maps. This enables CI and reproducible screenshots/metrics later. | JSON with status, path length, steps, collisions, efficiency. | Leaving loops unbounded; comparing different map sizes as if the metrics were equivalent. | All sample scenarios report `completed` and zero collisions. |
| 7. Add a scenario | Copy a JSON file, choose dimensions and endpoints, add wall rectangles, then run it. | A new selectable map. | Miscounting wall bounds, blocking a corridor, or overlapping an endpoint. | `--list-scenarios` discovers it; the route completes or reports no path. |
| 8. Test edge cases | Add maps with a direct route, a detour, a blocked endpoint, and no route. | Tests that define expected behavior. | Testing only one easy map; confusing no-route with a crash. | Unit tests cover shortest path, no path, same-cell endpoints, invalid endpoints, and simulation completion. |
| 9. Publish on GitHub | Create a repository from this folder, add a clear README, outputs, and a short demo recording. | A browsable proof-of-work repository. | Committing `.venv`, generated caches, huge videos, or claiming unsupported features. | Clone into a fresh folder, install from README, run headless mode, and open the GUI. |
| 10. Explain it in applications | Describe the implemented algorithms and the limits honestly. Link the repo and a short demo. | Resume entry and a concise interview walkthrough. | Calling the project “self-driving AI” or claiming neural-network object detection. | A reviewer can reproduce a run using only the README. |

## 5. GitHub folder structure

```text
AI-Autonomous-Navigation-System/
├── data/
│   └── scenarios/             # Editable warehouse/corridor JSON maps
├── docs/
│   ├── architecture.md        # Design, workflow, and limitations
│   └── project-guide.md       # Student tutorial, phases, and portfolio strategy
├── outputs/
│   └── runs/                  # Optional small JSON run results
├── src/
│   └── autonav/
│       ├── cli.py             # GUI/headless command-line interface
│       ├── grid.py            # Occupancy grid and movement rules
│       ├── models.py          # Scenario and metrics types
│       ├── planner.py         # A* path search
│       ├── scenarios.py       # JSON loader and validation
│       ├── simulator.py       # Robot state machine and safety gate
│       └── visualizer.py      # Pygame window and keyboard controls
├── tests/                     # Standard-library unit tests
├── .gitignore
├── main.py                    # Convenience launcher after installation
├── pyproject.toml             # Python package metadata and CLI entry point
├── README.md                  # Project landing page and quick start
└── requirements.txt           # Minimal runtime dependency
```

## 6. Building credible proof of work

### Suggested GitHub workflow

From the `python-project` folder:

```bash
git init
git add .
git commit -m "Build 2D autonomous navigation simulator"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/AI-Autonomous-Navigation-System.git
git push -u origin main
```

Create the empty GitHub repository first. Replace `YOUR-USERNAME` with your GitHub username. Never commit credentials or tokens.

After publishing, improve the proof:

1. Record a 20–40 second screen capture of at least two scenarios.
2. Add the capture or a compressed GIF to the repository and link it near the top of the README.
3. Include a sample headless JSON result and a short note on how it was produced.
4. Keep commits focused: planner, visualizer, tests, and documentation are useful milestones.
5. Add one scenario of your own and describe the challenge it tests.
6. Ask another person to follow the setup instructions from a clean clone; fix unclear steps they encounter.
7. Do not claim “AI perception,” real-time sensor fusion, or collision-free real-world deployment: those are outside the current implementation.

### Resume wording

> Built a Python/Pygame 2D autonomous-navigation simulator with A* shortest-path planning, validated JSON obstacle maps, a per-action collision safety check, and deterministic headless run metrics; verified behavior with unit tests across multiple scenarios.

### Interview walkthrough

Be ready to explain:

- Why A* is appropriate and why Manhattan distance is admissible for four-way moves.
- How the map turns wall rectangles into occupied cells.
- How the planner returns no route and how the simulator handles it.
- Why the collision check is separate from route planning.
- Which assumptions break when moving from a static grid to a physical robot.
- What you would implement next: sensor-derived local maps, dynamic obstacle updates, replanning, robot footprint/kinematics, or ROS 2 integration.

### Honest project scope

This is a portfolio teaching simulator, not a certified industrial controller, an autonomous road vehicle, or a machine-learning perception system. Stating that precisely makes the project more credible, not less.
