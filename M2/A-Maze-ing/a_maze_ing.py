#!/usr/bin/env python3
"""a_maze_ing - generate a maze from a config file and display it.

The program reads a ``KEY=VALUE`` configuration file, builds a maze with
the reusable :mod:`mazegen` module, stamps a visible ``42`` pattern made
of fully closed cells, writes the maze to the configured output file and
finally opens an interactive view (terminal or MLX graphical window).

Usage:
    python3 a_maze_ing.py [config_file] [--terminal | --mlx]

The config file is the only positional argument (``config.txt`` by
default). The optional flag overrides the ``DISPLAY`` config key.
"""

import sys
from dataclasses import dataclass

import view_mlx
import view_terminal
from mazegen import (MazeGenerator, WALL_E, WALL_N, WALL_S, WALL_W,
                     path_to_directions)

# The "42" stencil: 'X' marks a fully closed cell, 7 columns by 5 rows.
_PATTERN: tuple[str, ...] = (
    "X.X.XXX",
    "X.X...X",
    "XXX.XXX",
    "..X.X..",
    "..X.XXX",
)
_PATTERN_W = 7
_PATTERN_H = 5
_PATTERN_MARGIN = 2


class ConfigError(Exception):
    """Raised when the configuration file is missing or invalid."""


@dataclass
class Config:
    """Validated content of a maze configuration file."""

    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None
    display: str


def parse_config(path: str) -> Config:
    """Read and validate a maze configuration file.

    Args:
        path: path to the ``KEY=VALUE`` configuration file.

    Returns:
        A fully validated :class:`Config`.

    Raises:
        ConfigError: if the file is missing, malformed, or describes an
            impossible maze.
    """
    raw: dict[str, str] = {}
    try:
        with open(path, "r") as handle:
            for line in handle:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                raw[key.strip().upper()] = value.strip()
    except OSError as err:
        raise ConfigError(f"cannot read config file '{path}' ({err})")

    def coord(name: str) -> tuple[int, int]:
        try:
            a, b = raw[name].split(",")
            return int(a), int(b)
        except (KeyError, ValueError):
            raise ConfigError(f"{name} must be defined as 'x,y'")

    def integer(name: str) -> int:
        try:
            return int(raw[name])
        except (KeyError, ValueError):
            raise ConfigError(f"{name} must be defined as an integer")

    width = integer("WIDTH")
    height = integer("HEIGHT")
    entry = coord("ENTRY")
    exit_cell = coord("EXIT")
    output_file = raw.get("OUTPUT_FILE", "maze.txt")
    perfect = raw.get("PERFECT", "True").lower() == "true"
    display = raw.get("DISPLAY", "mlx").lower()
    seed: int | None = None
    if "SEED" in raw:
        try:
            seed = int(raw["SEED"])
        except ValueError:
            raise ConfigError("SEED must be an integer")

    if width < 1 or height < 1:
        raise ConfigError("WIDTH and HEIGHT must be 1 or more")
    for name, (cx, cy) in (("ENTRY", entry), ("EXIT", exit_cell)):
        if not (0 <= cx < width and 0 <= cy < height):
            raise ConfigError(
                f"{name} {cx},{cy} is outside the {width}x{height} grid")
    if entry == exit_cell:
        raise ConfigError("ENTRY and EXIT must be different cells")
    if display not in ("mlx", "terminal"):
        raise ConfigError("DISPLAY must be 'mlx' or 'terminal'")

    return Config(width, height, entry, exit_cell, output_file,
                  perfect, seed, display)


def forty_two_pattern(width: int, height: int, entry: tuple[int, int],
                      exit_cell: tuple[int, int]
                      ) -> tuple[set[tuple[int, int]], str]:
    """Compute the cells that draw a centred ``42`` in the maze.

    The stencil is scaled up as much as the maze allows, keeping a free
    margin around it so the maze stays fully connected.

    Args:
        width: maze width in cells.
        height: maze height in cells.
        entry: the entry cell, kept clear of the pattern.
        exit_cell: the exit cell, kept clear of the pattern.

    Returns:
        A tuple ``(cells, note)``. ``cells`` is the set of cells to keep
        fully closed (empty when the pattern cannot be drawn); ``note``
        is an explanatory message when the pattern is skipped, else "".
    """
    span = 2 * _PATTERN_MARGIN
    scale = 0
    for candidate in range(6, 0, -1):
        # The pattern stays at most half of each maze dimension so it
        # never dominates the maze on larger grids.
        if (_PATTERN_W * candidate + span <= width
                and _PATTERN_H * candidate + span <= height
                and 2 * _PATTERN_W * candidate <= width
                and 2 * _PATTERN_H * candidate <= height):
            scale = candidate
            break
    if scale == 0:
        return set(), ("note: the '42' pattern was skipped "
                       "(the maze is too small to fit it).")

    origin_x = (width - _PATTERN_W * scale) // 2
    origin_y = (height - _PATTERN_H * scale) // 2
    cells: set[tuple[int, int]] = set()
    for cy, row in enumerate(_PATTERN):
        for cx, mark in enumerate(row):
            if mark != "X":
                continue
            for sy in range(scale):
                for sx in range(scale):
                    cells.add((origin_x + cx * scale + sx,
                               origin_y + cy * scale + sy))
    if entry in cells or exit_cell in cells:
        return set(), ("note: the '42' pattern was skipped "
                       "(the entry or exit overlaps it).")
    return cells, ""


class MazeApp:
    """Maze state and actions shared by the two interactive views."""

    def __init__(self, config: Config) -> None:
        """Build the first maze described by ``config``.

        Args:
            config: the validated configuration to build from.
        """
        self.config = config
        self.blocked, self.note = forty_two_pattern(
            config.width, config.height, config.entry, config.exit)
        self.generator: MazeGenerator
        self.path: list[tuple[int, int]] = []
        self._build(config.seed)

    def _build(self, seed: int | None) -> None:
        """Generate, solve and save a maze for the given seed."""
        generator = MazeGenerator(self.config.width, self.config.height,
                                  perfect=self.config.perfect, seed=seed,
                                  blocked=self.blocked)
        generator.generate()
        self._open_borders(generator)
        self.generator = generator
        self.path = generator.solve(self.config.entry, self.config.exit)
        self._write_output()

    def regenerate(self) -> None:
        """Rebuild the maze from scratch with a fresh random seed."""
        self._build(None)

    def _open_borders(self, generator: MazeGenerator) -> None:
        """Open the outer wall of the entry and exit cells."""
        grid = generator.grid
        for x, y in (self.config.entry, self.config.exit):
            if y == 0:
                grid[y][x] &= ~WALL_N
            elif y == self.config.height - 1:
                grid[y][x] &= ~WALL_S
            elif x == 0:
                grid[y][x] &= ~WALL_W
            elif x == self.config.width - 1:
                grid[y][x] &= ~WALL_E

    def _write_output(self) -> None:
        """Write the maze and its solution to the output file."""
        lines = ["".join(format(cell, "x") for cell in row)
                 for row in self.generator.grid]
        lines.append("")
        lines.append("{},{}".format(*self.config.entry))
        lines.append("{},{}".format(*self.config.exit))
        lines.append(path_to_directions(self.path))
        with open(self.config.output_file, "w") as handle:
            handle.write("\n".join(lines) + "\n")


def main() -> int:
    """Entry point: parse the config, build the maze and open a view."""
    argv = sys.argv[1:]
    positional = [arg for arg in argv if not arg.startswith("-")]
    config_path = positional[0] if positional else "config.txt"

    try:
        config = parse_config(config_path)
        app = MazeApp(config)
    except ConfigError as err:
        print(f"error: {err}", file=sys.stderr)
        return 1
    except OSError as err:
        print(f"error: cannot write output file ({err})", file=sys.stderr)
        return 1

    kind = "perfect" if config.perfect else "braided"
    print(f"maze: {config.width}x{config.height} {kind}, "
          f"seed={app.generator.seed}")
    print(f"output written to {config.output_file}")
    if app.note:
        print(app.note)

    mode = config.display
    if "--terminal" in argv:
        mode = "terminal"
    elif "--mlx" in argv:
        mode = "mlx"

    if mode == "mlx" and view_mlx.run(app):
        return 0
    view_terminal.run(app)
    return 0


if __name__ == "__main__":
    sys.exit(main())
