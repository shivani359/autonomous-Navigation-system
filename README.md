
# 🤖 AI-Based Autonomous Navigation System

### Project 1 | AI-Enabled Industry-Oriented Project

A Python-based virtual robotics project that demonstrates autonomous path planning, obstacle avoidance, dynamic path replanning, and navigation performance analysis in a 2D simulation environment.

## 📌 Project Overview

The AI-Based Autonomous Navigation System simulates a virtual robot navigating through an environment containing obstacles.

The system calculates a path from a starting position to a destination, follows the planned route, avoids blocked cells, and replans when an obstacle makes the current route unavailable.

This project is designed to demonstrate practical knowledge of robotics concepts, intelligent search algorithms, Python programming, simulation, and software testing without requiring physical robot hardware.

## 🎯 Objectives

- Develop a virtual autonomous navigation system.
- Implement the A* path-planning algorithm.
- Represent environments using a grid map.
- Avoid obstacles and prevent invalid movements.
- Support dynamic obstacle detection and path replanning.
- Visualize robot movement and planned routes.
- Evaluate navigation performance using measurable metrics.
- Build a documented, testable GitHub portfolio project.

## ✨ Key Features

- 🗺️ 2D grid-based simulation
- 🧭 Intelligent path planning using A*
- 🚧 Obstacle-aware navigation
- 🔄 Dynamic path replanning
- 🤖 Virtual robot movement
- 📊 Navigation metrics and visualization
- 🧪 Automated software testing
- 📁 Configurable simulation scenarios

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core implementation |
| NumPy | Grid and numerical operations |
| Matplotlib | Simulation visualization |
| A* Algorithm | Path planning |
| JSON | Configuration and results |
| Pytest | Automated testing |
| Git and GitHub | Version control and project hosting |

## 🏗️ System Architecture

```text
Environment Configuration
          |
          v
     Grid Map
          |
          v
 Environment Representation
          |
          v
    A* Path Planner
          |
          v
  Navigation Controller
          |
          v
 Obstacle and Safety Checks
          |
          v
 Dynamic Path Replanning
          |
          v
 Simulation Visualization
          |
          v
 Performance Evaluation
```

## ⚙️ How It Works

1. Initialize the simulation environment.
2. Define the robot's starting position and destination.
3. Mark obstacles on the grid map.
4. Use A* to calculate a feasible route.
5. Move the virtual robot along the planned path.
6. Check whether the next movement is safe.
7. Recalculate the route if an obstacle blocks the current path.
8. Record the final navigation status and performance metrics.

## 📂 Project Structure

```text
AI-Autonomous-Navigation-System/
│
├── configs/
│   └── default.json
├── data/
├── src/
│   ├── __init__.py
│   ├── environment.py
│   ├── planner.py
│   ├── controller.py
│   ├── simulation.py
│   ├── visualization.py
│   └── metrics.py
├── tests/
│   ├── test_environment.py
│   ├── test_planner.py
│   └── test_controller.py
├── outputs/
│   ├── figures/
│   ├── logs/
│   └── metrics/
├── images/
├── videos/
├── docs/
├── notebooks/
├── main.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

*Note: The structure above describes the intended organization. Keep only files and features that are actually implemented in your repository.*

## 💻 Installation

### Prerequisites

- Python 3.11 or newer
- Git
- Visual Studio Code or another Python editor

### Step 1: Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/AI-Autonomous-Navigation-System.git
cd AI-Autonomous-Navigation-System
```

Replace `YOUR-USERNAME` with your GitHub username.

### Step 2: Create a virtual environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## ▶️ Run the Project

Start the simulation from the project root:

```bash
python main.py
```

The exact command and available options depend on the implemented entry point. Follow the commands documented in the source code and configuration if your implementation uses different options.

## 🧪 Testing

Run the automated test suite:

```bash
python -m pytest tests/ -v
```

Tests should verify:

- Valid path generation
- Obstacle avoidance
- Start and goal validation
- Unreachable destinations
- Safe robot movement
- Dynamic replanning
- Navigation completion

Record the actual test results before publishing them.

## 📊 Performance Evaluation

The project can measure:

- Path length
- Number of explored nodes
- Planning execution time
- Number of replanning operations
- Navigation success or failure
- Collision-free movement

Do not publish performance numbers until they have been measured in an actual run.

## 📸 Simulation Results

Add screenshots of the working simulation to the `images/` folder.

Recommended evidence:

1. Environment with obstacles and start/goal positions
2. Planned path generated by A*
3. Robot navigating the environment
4. Dynamic obstacle and replanning scenario
5. Performance metrics or test results

Example image reference:

```markdown
![Navigation Simulation](images/navigation_simulation.png)
```

Replace the example filename with the actual screenshot you add.

## 🚀 Future Enhancements

- Compare A*, Dijkstra, and BFS.
- Add OpenCV-based image perception.
- Introduce simulated sensor noise.
- Implement waypoint tracking and smoother motion.
- Add a graphical user interface.
- Explore 3D simulation using Webots or CARLA.
- Integrate a trained object-detection model where appropriate.

## ⚠️ Limitations

- The initial implementation uses a virtual 2D environment.
- It does not represent a fully autonomous real-world vehicle.
- Camera-based object detection is not included unless separately implemented.
- Results depend on the map, movement rules, and simulation assumptions.
- Simulation results alone do not establish real-world safety.

## 🎓 Learning Outcomes

Through this project, I aim to strengthen my understanding of:

- Python software development
- AI search and path-planning algorithms
- Robotics and autonomous navigation concepts
- Obstacle avoidance and replanning
- Simulation and visualization
- Software testing and GitHub documentation

## 👩‍💻 Author

**Shivani Chouhan**

Computer Science Student | Aspiring AI/ML Engineer

GitHub: https://github.com/YOUR-USERNAME

## 🙏 Acknowledgements

Special thanks to **Umesh Sir** for his valuable guidance, encouragement, and support throughout my learning journey.

## 📄 License

This project is intended for educational and portfolio purposes.

See the `LICENSE` file for the terms of use.

---

⭐ If you find this project interesting, consider giving the repository a star!

**Project 1 | AI-Enabled Industry-Oriented Project**
