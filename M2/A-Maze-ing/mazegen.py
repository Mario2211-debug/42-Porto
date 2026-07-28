"""mazegen - a small, reusable maze generator.

This single-file module exposes one class, :class:`MazeGenerator`, which
builds a rectangular maze with the *recursive backtracker* algorithm and
can return the shortest path between two cells.

Wall encoding
-------------
Every cell is an ``int`` holding four wall bits.  A set bit means the wall
is closed::

    bit 0 (WALL_N) = North      bit 2 (WALL_S) = South
    bit 1 (WALL_E) = East       bit 3 (WALL_W) = West

A value of ``0xF`` (``ALL_WALLS``) is a fully closed cell.

Basic example
-------------
>>> from mazegen import MazeGenerator
>>> gen = MazeGenerator(20, 15, perfect=True, seed=42)
>>> gen.generate()
>>> grid = gen.grid                       # list[list[int]] of wall bits
>>> path = gen.solve((0, 0), (19, 14))    # shortest list of (x, y) cells

Custom parameters
-----------------
``width`` / ``height`` set the maze size, ``perfect`` chooses between a
perfect maze (one single path between any two cells) and a braided maze
with extra loops, ``seed`` makes a run reproducible, and ``blocked`` is a
set of cells the generator leaves fully closed and carves around.
"""

import random
from collections import deque
from collections.abc import Iterable

__version__ = "1.0.0"

# Wall bits.
WALL_N = 1
WALL_E = 2
WALL_S = 4
WALL_W = 8
ALL_WALLS = WALL_N | WALL_E | WALL_S | WALL_W

_MOVES = (
    (0, -1, WALL_N, WALL_S),
    (1, 0, WALL_E, WALL_W),
    (0, 1, WALL_S, WALL_N),
    (-1, 0, WALL_W, WALL_E),
)

_LETTER = {
    (0, -1): "N",
    (1, 0): "E",
    (0, 1): "S",
    (-1, 0): "W"
}


class MazeGenerator:
    """Generate and solve a rectangular maze.

    Attributes:
        width: number of cells on each row.
        height: number of cell rows.
        perfect: when True the maze has exactly one path between any two
            cells; when False extra passages are carved to add loops.
        seed: the random seed actually used. It is always set, even when
            the caller passes ``None``, so any maze can be reproduced.
    """

    def __init__(self, width: int, height: int, *,
                 perfect: bool = True,
                 seed: int | None = None,
                 blocked: Iterable[tuple[int, int]] | None = None) -> None:
        """Prepare a fully walled maze ready to be carved.

        Args:
            width: number of cells per row (>= 1).
            height: number of cell rows (>= 1).
            perfect: request a perfect maze (no loops) when True.
            seed: random seed; when None a random one is chosen and kept.
            blocked: cells that must stay fully closed and be carved
                around (used to stamp shapes into the maze).

        Raises:
            ValueError: if width or height is smaller than 1.
        """
        if width < 1 or height < 1:
            raise ValueError("maze width and height must be >= 1")
        self.width = width
        self.height = height
        self.perfect = perfect
        self.seed: int = random.randrange(2 ** 31) if seed is None else seed
        self._random = random.Random(self.seed)
        self._blocked: set[tuple[int, int]] = set(blocked or ())
        self._grid: list[list[int]] = [
            [ALL_WALLS] * width for _ in range(height)
        ]

    @property
    def grid(self) -> list[list[int]]:
        """The live maze grid of wall-bit integers, indexed ``grid[y][x]``.

        The list is the generator's own storage, not a copy, so callers
        may read it freely and tweak outer walls if they need to.
        """
        return self._grid

    @property
    def blocked(self) -> set[tuple[int, int]]:
        """A copy of the set of cells left fully closed by the generator."""
        return set(self._blocked)

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True when (x, y) lies inside the maze grid."""
        return 0 <= x < self.width and 0 <= y < self.height

    def generate(self) -> None:
        """Carve the maze in place.

        A perfect maze is always carved first; when ``perfect`` is False
        extra walls are then removed to create loops.
        """
        self._carve_perfect()
        if not self.perfect:
            self._add_loops()

    def _carve_perfect(self) -> None:
        """Carve a perfect maze with an iterative recursive backtracker."""
        start = self._first_free_cell()
        if start is None:
            return
        visited = [[False] * self.width for _ in range(self.height)]
        for bx, by in self._blocked:
            visited[by][bx] = True
        sx, sy = start
        visited[sy][sx] = True
        stack = [start]
        while stack:
            x, y = stack[-1]
            options = []
            for dx, dy, wall, opp in _MOVES:
                nx, ny = x + dx, y + dy
                if self.in_bounds(nx, ny) and not visited[ny][nx]:
                    options.append((nx, ny, wall, opp))
            if not options:
                stack.pop()
                continue
            nx, ny, wall, opp = self._random.choice(options)
            self._grid[y][x] &= ~wall
            self._grid[ny][nx] &= ~opp
            visited[ny][nx] = True
            stack.append((nx, ny))

    def _first_free_cell(self) -> tuple[int, int] | None:
        """Return the first non-blocked cell, or None if every cell is."""
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) not in self._blocked:
                    return (x, y)
        return None

    def _add_loops(self) -> None:
        """Remove extra walls, never creating a 3x3 fully open area."""
        extra = max(1, (self.width * self.height) // 8)
        for _ in range(extra):
            x = self._random.randrange(self.width)
            y = self._random.randrange(self.height)
            dx, dy, wall, opp = self._random.choice(_MOVES)
            nx, ny = x + dx, y + dy
            if not self.in_bounds(nx, ny):
                continue
            if (x, y) in self._blocked or (nx, ny) in self._blocked:
                continue
            if not self._grid[y][x] & wall:
                continue
            self._grid[y][x] &= ~wall
            self._grid[ny][nx] &= ~opp
            if self._in_open_3x3(x, y) or self._in_open_3x3(nx, ny):
                self._grid[y][x] |= wall
                self._grid[ny][nx] |= opp

    def _in_open_3x3(self, x: int, y: int) -> bool:
        """Return True if cell (x, y) belongs to a 3x3 fully open block."""
        for by in range(y - 2, y + 1):
            for bx in range(x - 2, x + 1):
                if self._is_open_block(bx, by):
                    return True
        return False

    def _is_open_block(self, bx: int, by: int) -> bool:
        """Return True if the 3x3 block at (bx, by) has no inner wall."""
        if bx < 0 or by < 0:
            return False
        if bx + 2 >= self.width or by + 2 >= self.height:
            return False
        for j in range(3):
            for i in range(3):
                cell = self._grid[by + j][bx + i]
                if i < 2 and cell & WALL_E:
                    return False
                if j < 2 and cell & WALL_S:
                    return False
        return True

    def solve(self, start: tuple[int, int],
              goal: tuple[int, int]) -> list[tuple[int, int]]:
        """Return the shortest path between two cells (breadth-first).

        Args:
            start: (x, y) of the first cell.
            goal: (x, y) of the destination cell.

        Returns:
            The list of cells from ``start`` to ``goal`` inclusive, or an
            empty list when ``goal`` cannot be reached from ``start``.
        """
        if start == goal:
            return [start]
        prev: dict[tuple[int, int], tuple[int, int]] = {start: start}
        queue: deque[tuple[int, int]] = deque([start])
        while queue:
            x, y = queue.popleft()
            if (x, y) == goal:
                break
            for dx, dy, wall, _opp in _MOVES:
                if self._grid[y][x] & wall:
                    continue
                nxt = (x + dx, y + dy)
                if not self.in_bounds(*nxt) or nxt in prev:
                    continue
                prev[nxt] = (x, y)
                queue.append(nxt)
        if goal not in prev:
            return []
        path = [goal]
        while path[-1] != start:
            path.append(prev[path[-1]])
        path.reverse()
        return path


def path_to_directions(path: list[tuple[int, int]]) -> str:
    """Turn a cell path into a string of N/E/S/W move letters.

    Args:
        path: a list of adjacent cells, as returned by
            :meth:`MazeGenerator.solve`.

    Returns:
        One letter per step between consecutive cells (empty when the
        path has fewer than two cells).
    """
    letters = []
    for (x0, y0), (x1, y1) in zip(path, path[1:]):
        letters.append(_LETTER[(x1 - x0, y1 - y0)])
    return "".join(letters)
