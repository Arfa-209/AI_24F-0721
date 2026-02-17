# AI Pathfinder Visualizer

**AI2002 - Artificial Intelligence | Assignment 1 | Spring 2026**

A GUI-based pathfinding visualizer implementing 6 uninformed search algorithms with dynamic obstacle handling and real-time step-by-step visualization.

---

## Algorithms Implemented

- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Uniform-Cost Search (UCS)
- Depth-Limited Search (DLS)
- Iterative Deepening DFS (IDDFS)
- Bidirectional Search

---

## Installation

Make sure you have Python 3.7 or higher installed.

Install the required dependency:

```bash
pip install pygame
```

---

## How to Run

```bash
python pathfinder1.py
```

---

## Controls

| Action | Control |
|--------|---------|
| Set Start Point | Left Click (1st click) |
| Set End Point | Left Click (2nd click) |
| Draw Wall | Left Click (subsequent clicks) |
| Remove Node | Right Click |
| Run BFS | Press 1 |
| Run DFS | Press 2 |
| Run UCS | Press 3 |
| Run DLS | Press 4 |
| Run IDDFS | Press 5 |
| Run Bidirectional | Press 6 |
| Reset Search | Press R |
| Clear Grid | Press SPACE |

---

## Color Guide

- **Green** — Start Node
- **Red** — End Node
- **Black** — Walls / Obstacles
- **Light Blue** — Frontier (nodes to be explored)
- **Cyan** — Explored Nodes
- **Purple** — Final Path

---

## Technical Details

**Movement:** 8-directional (all diagonals included)

**Dynamic Obstacles:** 1% probability per step — if an obstacle blocks the current path, the algorithm re-plans automatically.

**Cost (UCS):** Straight move = 1.0, Diagonal move = 1.414

---

## Project Structure

```
AI_24F-0721/
├── pathfinder1.py       # Main application
├── README.md            # Project documentation
└── report.pdf           # Analysis report with screenshots
```

---

## Author

**Name:** Hafiza Arfa Rashid 
**Student ID:** 24F-0721 
**Course:** AI2002 - Artificial Intelligence  
**Semester:** Spring 2026
