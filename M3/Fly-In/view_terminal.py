import sys
from typing import Dict, List, Tuple, Optional, TextIO

from model import MapData
from visual_common import (
    ANSI_BOLD,
    ANSI_RESET,
    ansi_for_color,
    get_turn_moves,
)


def _supports_color() -> bool:
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def print_sim_output(
    paths: Dict[str, List[Tuple[str, int]]],
    *,
    use_color: bool = True,
) -> None:
    """Print the mandatory simulation output format (one line per turn)."""
    colored = use_color and _supports_color()
    for _turn, moves in get_turn_moves(paths):
        if colored:
            parts = []
            for move in moves:
                drone, _, dest = move.partition("-")
                parts.append(
                    f"{ANSI_BOLD}{ansi_for_color('cyan')}{drone}{ANSI_RESET}"
                    f"-{ansi_for_color('yellow')}{dest}{ANSI_RESET}"
                )
            print(" ".join(parts))
        else:
            print(" ".join(moves))


def print_terminal_vis(
    map_data: MapData,
    paths: Dict[str, List[Tuple[str, int]]],
    *,
    stream: Optional[TextIO] = None,
) -> None:
    """Print a readable, colored turn-by-turn summary to stderr."""
    out = stream or sys.stderr
    colored = hasattr(out, "isatty") and out.isatty()
    turns = get_turn_moves(paths)
    max_t = turns[-1][0] if turns else 0

    def c(text: str, color: str = "white", bold: bool = False) -> str:
        if not colored:
            return text
        prefix = ANSI_BOLD if bold else ""
        return f"{prefix}{ansi_for_color(color)}{text}{ANSI_RESET}"

    print(c("\nFly-In — simulation summary", "cyan", bold=True), file=out)
    print(
        c(
            f"Map: {map_data.start_hub} → {map_data.end_hub}  "
            f"Drones: {map_data.nb_drones}  Turns: {max_t}",
            "white",
        ),
        file=out,
    )
    print(c("─" * 60, "gray"), file=out)

    print(c("\nNetwork", "yellow", bold=True), file=out)
    for z in sorted(map_data.zones.values(),
                    key=lambda zone: (zone.y, zone.x)):
        fill_name = z.color or z.zone_type
        label = (
            f"  {z.name:12} ({z.x:>3},{z.y:<3}) "
            f"type={z.zone_type:<10} cap={z.max_drones}"
        )
        print(c(label, fill_name if z.color else "white"), file=out)

    print(c("\nTurn-by-turn moves", "yellow", bold=True), file=out)
    print(c("  (format: D<ID>-<zone> or D<ID>-<connection>)",
            "gray"), file=out)

    for turn, moves in turns:
        move_parts = []
        for move in moves:
            drone, _, dest = move.partition("-")
            if colored:
                move_parts.append(
                    f"{c(drone, 'cyan', bold=True)}-{c(f'{dest}', 'yellow')}"
                )
            else:
                move_parts.append(move)
        label = c(f"T{turn:02d}", "magenta", bold=True)
        print(f"{label}: {' '.join(move_parts)}", file=out)
    print(c("\nMandatory stdout format (copy/paste):", "gray"), file=out)
    for _turn, moves in turns:
        print(f"  {' '.join(moves)}", file=out)

    print(c("─" * 60, "gray"), file=out)
