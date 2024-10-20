# A* Path Finder Visualization

This project is a visualization of the A* pathfinding algorithm using Python's `pygame` library. It allows you to create obstacles, set a start and goal position, and then visualize the A* algorithm finding the shortest path.

## Prerequisites

Make sure you have Python 3 installed on your system. You will also need to install the `pygame` library if you don't already have it. You can install `pygame` using the following command:

```bash 
pip install pygame
````

to Run
```bash
python astar_visualizer.py
```
if Linux
```bash
python3 astar_visualizer.py
```

# Left Mouse Click:
Click to place the start node (orange) if it is not already set.

Click to place the goal node (turquoise) if the start node is already set.

Click to add obstacles (black cells) to the grid after placing the start and goal nodes.

# Right Mouse Click:
Click on any cell to reset it to a blank state (white).

If the cell is the start or goal node, this action will remove them.

# Start
Press Enter to start.

Press the C Key to Clear the window.