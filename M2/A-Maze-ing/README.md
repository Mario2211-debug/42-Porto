*This project has been created as part of the 42 curriculum by mafonso and lpaiva.*


# A-Maze-ing

## Description

**A-Maze-ing** is a maze generator written in Python. It reads a plain-text
configuration file, builds a maze, writes it to an output file using a
hexadecimal wall encoding, and displays it in an interactive view.

The maze can be **perfect** (exactly one path between any two cells) or
**braided** (extra passages create loops). Every maze also contains a visible
**"42"** drawn with fully closed cells, and the program can show the shortest
path between the entry and the exit.

Two views are provided:

- a **terminal** version (simple, text only);
- a **graphical** version built with the **MiniLibX (MLX)** library.

## Instructions

### Requirements

- Python **3.10+**
- The bundled `mlx` wheel (only needed for the graphical view)

### Installation

```bash
make install
```

This creates a virtual environment in `.venv/`, installs the MLX library and
the developer tools, builds the reusable `mazegen` package and installs it.

### Execution

```bash
make run                              # run with config.txt
.venv/bin/python a_maze_ing.py config.txt
.venv/bin/python a_maze_ing.py config.txt --terminal   # force the terminal view
.venv/bin/python a_maze_ing.py config.txt --mlx        # force the graphical view
```

Other useful targets:

```bash
make debug          # run under the Python debugger (pdb)
make lint           # flake8 + mypy
make lint-strict    # flake8 + mypy --strict
make test           # run the automated test suite (pytest)
make clean          # remove caches and build artifacts
make package        # rebuild the mazegen-* package
```

### Interactions

Both views offer the same actions:

| Key (MLX) | Menu (terminal) | Action                          |
|-----------|-----------------|---------------------------------|
| `1`       | `1`             | Regenerate a new maze           |
| `2`       | `2`             | Show / hide the solution path   |
| `3`       | `3`             | Change the wall colour          |
| `4` / ESC | `4`             | Quit                            |

## Configuration file

The configuration file contains one `KEY=VALUE` pair per line. Lines starting
with `#` and blank lines are ignored.

| Key           | Required | Description                              | Example              |
|---------------|----------|------------------------------------------|----------------------|
| `WIDTH`       | yes      | Maze width in cells                      | `WIDTH=20`           |
| `HEIGHT`      | yes      | Maze height in cells                     | `HEIGHT=15`          |
| `ENTRY`       | yes      | Entry cell coordinates `x,y`             | `ENTRY=0,0`          |
| `EXIT`        | yes      | Exit cell coordinates `x,y`              | `EXIT=19,14`         |
| `OUTPUT_FILE` | yes      | Output file name                         | `OUTPUT_FILE=maze.txt` |
| `PERFECT`     | yes      | `True` for a perfect maze, else braided  | `PERFECT=True`       |
| `DISPLAY`     | no       | `mlx` (default) or `terminal`            | `DISPLAY=mlx`        |
| `SEED`        | no       | Integer seed for a reproducible maze     | `SEED=42`            |

`ENTRY` and `EXIT` must be different cells, both inside the maze bounds. A
default `config.txt` is provided in this repository.

## Output file format

The output file describes the maze with **one hexadecimal digit per cell**.
Each bit of a digit tells whether a wall is **closed** (`1`) or **open** (`0`):

| Bit | Direction |
|-----|-----------|
| 0   | North     |
| 1   | East      |
| 2   | South     |
| 3   | West      |

Cells are stored row by row, one row per line. After an empty line, three
extra lines are written: the entry coordinates, the exit coordinates, and the
shortest path from entry to exit as a string of `N`, `E`, `S`, `W` letters.

A `output_validator.py` script (provided with the subject) checks that
neighbouring cells share consistent walls.

## Maze generation algorithm

The maze is generated with the **recursive backtracker** (a randomized
depth-first search), implemented iteratively with an explicit stack to avoid
recursion-depth limits.

1. Every cell starts fully walled in.
2. Starting from a random cell, the algorithm repeatedly walks to a random
   unvisited neighbour, knocking down the wall between them.
3. When a cell has no unvisited neighbour, it backtracks.

This always produces a **perfect maze**: a spanning tree of the grid, i.e.
exactly one path between any two cells. When `PERFECT=False`, a few extra
walls are then removed to create loops, while guaranteeing no `3x3` fully
open area appears (corridors stay at most 2 cells wide).

The **"42"** pattern is handled by marking its cells as *blocked* before
generation: the algorithm carves around them, so they stay fully closed and
the rest of the maze remains fully connected.

### Why this algorithm

- It is simple to implement and easy to explain.
- It guarantees a perfect maze with no extra bookkeeping.
- It naturally produces long, winding corridors, which makes the maze look
  good and the solution path interesting.
- It is easy to extend: blocked cells (the "42" pattern) are handled by a
  one-line check, and braided mazes only need a small post-processing pass.

## Reusable code

The maze generation logic is isolated in a standalone, single-file module:
**`mazegen.py`**, packaged as **`mazegen`** (`mazegen-1.0.0-*.whl` /
`mazegen-1.0.0.tar.gz` at the repository root, built with `pyproject.toml`).

It exposes one class, `MazeGenerator`, plus the helper `path_to_directions`.
The application file `a_maze_ing.py` only handles the configuration, the "42"
pattern, the output file and the views; the algorithm itself lives in
`mazegen` and can be reused by any other project.

```python
from mazegen import MazeGenerator, path_to_directions

# Custom parameters: size, perfect/braided, seed, blocked cells.
gen = MazeGenerator(20, 15, perfect=True, seed=42)
gen.generate()

grid = gen.grid                       # access the maze structure
path = gen.solve((0, 0), (19, 14))    # access a solution (shortest path)
moves = path_to_directions(path)      # "SSEE..." direction string
print(gen.seed)                       # the seed actually used
```

`MazeGenerator.grid` is a `list[list[int]]` of wall-bit integers; this is the
internal structure and is not necessarily identical to the output file
format. `MazeGenerator.solve()` returns the shortest path as a list of cells.

## Resources

Classic references on maze generation:

- Jamis Buck, *Mazes for Programmers* (recursive backtracker, braiding).
- Wikipedia: "Maze generation algorithm".
- The relation between perfect mazes and spanning trees in graph theory.

### Use of AI

> **TODO:** review and adjust this section so it reflects your own use.

AI assistance (an LLM coding assistant) was used as a support tool, not as a
replacement for understanding. Concretely, it helped with:

- explaining the MLX image/event API and the loop-hook rendering pattern;
- drafting and reviewing the maze-generation and solving code;
- setting up packaging (`pyproject.toml`), the `Makefile` and lint configs.

Every generated piece of code was read, tested (`output_validator.py`,
`flake8`, `mypy`) and is fully understood by the team.
