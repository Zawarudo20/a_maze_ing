*This project has been created as part of the 42 curriculum by mbakha, rakaarir.*

# A-Maze-ing

## Description

A-Maze-ing is a maze generator and solver written in Python. The goal of this project is to generate a random maze, find the shortest path between two points, and optionally allow the user to interact with the maze as a simple game.

The maze is generated using Prim’s algorithm, which ensures a well-distributed and fully connected maze. To solve the maze, the program uses Breadth-First Search (BFS) to guarantee the shortest path is found.

The project also includes customization features such as colored maze output and a playable mode.

---

## Instructions

### Installation

First, install the project dependency using the Makefile:

```bash
make install
```

Then, install the mazegen package

```bash
python3 -m pip install mazegen-1.0.0-py3-none-any.whl
```

### Run the program

```bash
make run
```

---

## Features

* Random maze generation
* maze generation using seed
* Shortest path solving
* Customizable maze colors
* Playable maze mode
* Output file that has :
    * Maze in Base16
    * Start and End point cordinations 
    * The shortest path direction

---

## Configuration File Structure

The configuration file allows customization of the maze display and behavior. It typically includes:

* Maze dimensions (width, height)
* Start and end positions
* The name of the Output file
* Perfect maze option
* Seed number

Example structure:

```txt
WIDTH=25
HEIGHT=30
ENTRY=5,29
EXIT=20,1
OUTPUT_FILE=maze.txt
PERFECT=false
SEED=42
```

---

## Maze Generation Algorithm

### Prim’s Algorithm

The maze is generated using a randomized version of Prim’s algorithm:

1. Start with a grid full of walls.
2. Make a list of Positions as Starting Position..
3. Pick a starting cell and mark it as visited cell adn add it to this list.
4. Get a Rondom cell from this list.
3. Check if there is a neighbor cell not visited.
   * If all the neighbor are visited Remove this cell from the Starting position..list
   * Else : continue reading ...
4. Add the neighbors that not visited to a list.
5. select a Random neighbor and mark it as visited.
6. Remove the wall between them.
7. add this neighbor to the Starting positions list.
9. Repeat until The Starting positions is empty.

### Why Prim’s Algorithm?

Prim’s algorithm was chosen because:

* It easy to work
* Optimized

---

## Pathfinding Algorithm

### Breadth-First Search (BFS)

BFS is used to find the shortest path:

1. Make a list of Paths.
2. Start from the start position and make it owen path list and add it to the Paths.
3. Check every Path where it reached
    * if the last position has no not visited neighbor can move to remove the path from paths
    * else: continue reading...
4. make new paths to each point that origin path can reach to
5. add those paths to a new paths list
6. repeate until you check every path in the old paths list
7. repeate everything but using the new paths list until a path reach the end point

Why BFS:

* It easy to work
* Optimized
* Can give you the shortest path

---

## Reusable Code

Several parts of the project are reusable:

* A_Maze_ing.py files that has:
    * Maze generation logic (can be reused in games or simulations)
    * BFS pathfinding (usable in grids, maps, AI systems)
    * To generate maze send {HEIGHT: INT, WIDTH: INT, ENTRY: TUPLE[INT, INT], EXIT: TUPLE[INT, INT], PERFECT: BOOL, OUTPUT_FILE: STR, SEED: OPTIONAL} to MazeGenerator.update()
    then MazeGenerator.generate_maze()
* pars.py file for Parsing system
* Printing.py for printing MazeGenerator class that in (A_Maze_ing.py)

---

## Team & Project Management

### Team Members

* **mbakha**

  * Maze generation (Prim)
  * Output file handling
  * Game mode
  * Readme

* **Rakaarir**

  * Pathfinding (BFS)
  * Parsing system
  * Maze color cust~omization
  * Makefile

---

### Planning & Evolution

* Initial plan focused on maze generation only
* Pathfinding was added after basic maze creation
* Game mode and customization were added later as improvements

---

### What Worked Well

* Clear separation of responsibilities
* Efficient algorithms (Prim + BFS)
* Modular code structure

---

### What Could Be Improved

* More advanced UI (e.g., graphical interface)
* Additional algorithms (DFS, A*)
* Better configuration system

---

### Tools Used

* Python standard library
* ReadChar
* Makefile
* poetry

---

## Resources

* [Prim’s Algorithm](https://www.youtube.com/shorts/GHQ4fjPCVLI)
* [Maze generation algorithms](https://www.youtube.com/watch?v=ioUl1M77hww&t=190s)
* [BFS pathfinding](https://www.youtube.com/watch?v=aW9kZcJx64o)

### AI Usage

We used AI to:
* get famous maze generation algorithms
* get famous path-finding generation algorithms
* get some usable python libraries