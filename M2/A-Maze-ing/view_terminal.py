"""Terminal view for a_maze_ing - the simple, text-only version.

It renders the maze with block characters and ANSI colours and offers a
small menu so the user can regenerate the maze, show or hide the solution
path, and cycle the wall colour.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from mazegen import WALL_E, WALL_N, WALL_S, WALL_W

if TYPE_CHECKING:
    from a_maze_ing import MazeApp

_EMPTY, _WALL, _PATH, _ENTRY, _EXIT, _BLOCK = range(6)

_RESET = "\033[0m"
_CLEAR = "\033[2J\033[H"

_WALL_COLOURS: list[tuple[str, str]] = [
    ("white", "\033[97m"),
    ("cyan", "\033[96m"),
    ("green", "\033[92m"),
    ("magenta", "\033[95m"),
    ("yellow", "\033[93m"),
]

_GLYPH = {_EMPTY: " ", _WALL: "█", _PATH: "·",
          _ENTRY: "E", _EXIT: "S", _BLOCK: "▓"}
_COLOUR = {_PATH: "\033[96m", _ENTRY: "\033[92m",
           _EXIT: "\033[91m", _BLOCK: "\033[93m"}


def _build_canvas(app: MazeApp, show_path: bool) -> list[list[int]]:
    """Build a category grid of size (2H+1) x (2W+1) for the maze."""
    width, height = app.config.width, app.config.height
    grid = app.generator.grid
    rows, cols = 2 * height + 1, 2 * width + 1
    canvas = [[_EMPTY] * cols for _ in range(rows)]

    for y in range(height):
        for x in range(width):
            cell = grid[y][x]
            r, c = 2 * y + 1, 2 * x + 1
            for dr in (-1, 1):
                for dc in (-1, 1):
                    canvas[r + dr][c + dc] = _WALL
            if cell & WALL_N:
                canvas[r - 1][c] = _WALL
            if cell & WALL_S:
                canvas[r + 1][c] = _WALL
            if cell & WALL_W:
                canvas[r][c - 1] = _WALL
            if cell & WALL_E:
                canvas[r][c + 1] = _WALL

    for x, y in app.generator.blocked:
        canvas[2 * y + 1][2 * x + 1] = _BLOCK

    if show_path and app.path:
        for x, y in app.path:
            canvas[2 * y + 1][2 * x + 1] = _PATH
        for (x0, y0), (x1, y1) in zip(app.path, app.path[1:]):
            canvas[y0 + y1 + 1][x0 + x1 + 1] = _PATH

    ex, ey = app.config.entry
    xx, xy = app.config.exit
    canvas[2 * ey + 1][2 * ex + 1] = _ENTRY
    canvas[2 * xy + 1][2 * xx + 1] = _EXIT
    return canvas


def _draw(app: MazeApp, show_path: bool, palette: int) -> None:
    """Print the whole maze to the terminal."""
    canvas = _build_canvas(app, show_path)
    wall_colour = _WALL_COLOURS[palette][1]
    lines = []
    for row in canvas:
        chunks = []
        for category in row:
            glyph = _GLYPH[category]
            colour = wall_colour if category == _WALL \
                else _COLOUR.get(category, "")
            chunks.append(f"{colour}{glyph}{_RESET}" if colour else glyph)
        lines.append("".join(chunks))
    print(_CLEAR + "\n".join(lines))


def _menu(app: MazeApp, show_path: bool, palette: int) -> None:
    """Print the interactive menu under the maze."""
    kind = "perfect" if app.config.perfect else "braided"
    path_state = "shown" if show_path else "hidden"
    print(f"\n=== a_maze_ing (terminal) ===  "
          f"{app.config.width}x{app.config.height} {kind}, "
          f"seed={app.generator.seed}")
    if app.note:
        print(app.note)
    print("  1) Regenerate a new maze")
    print(f"  2) Show/Hide the solution path   [{path_state}]")
    print(f"  3) Change the wall colour        "
          f"[{_WALL_COLOURS[palette][0]}]")
    print("  4) Quit")


def run(app: MazeApp) -> None:
    """Run the interactive terminal view until the user quits.

    Args:
        app: the shared maze application state.
    """
    show_path = False
    palette = 0
    while True:
        _draw(app, show_path, palette)
        _menu(app, show_path, palette)
        try:
            choice = input("choice> ").strip()
        except EOFError:
            print()
            return
        if choice == "1":
            app.regenerate()
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            palette = (palette + 1) % len(_WALL_COLOURS)
        elif choice == "4":
            return
