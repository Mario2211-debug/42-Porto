from typing import Dict, List, Optional, Tuple

from model import MapData, Zone

# Default pygame window size (resizable at runtime)
DEFAULT_WINDOW_WIDTH = 1600
DEFAULT_WINDOW_HEIGHT = 900
MIN_WINDOW_WIDTH = 960
MIN_WINDOW_HEIGHT = 540

# Subject colours apply to zones, not drones
DRONE_FILL = (245, 245, 250)
DRONE_OUTLINE = (35, 38, 50)
DRONE_LABEL = (25, 28, 38)

# Layout regions inside the window
HEADER_HEIGHT = 56
SIDEBAR_WIDTH = 300
FOOTER_HEIGHT = 8

NAMED_COLORS: Dict[str, Tuple[int, int, int]] = {
    "red": (220, 70, 70),
    "green": (70, 200, 90),
    "blue": (80, 140, 230),
    "yellow": (240, 210, 60),
    "cyan": (60, 210, 210),
    "magenta": (220, 90, 220),
    "orange": (240, 160, 60),
    "gray": (150, 150, 160),
    "grey": (150, 150, 160),
    "white": (240, 240, 245),
    "black": (30, 30, 40),
    "purple": (160, 100, 220),
    "pink": (240, 130, 180),
    "brown": (160, 110, 70),
}

ZONE_TYPE_COLORS: Dict[str, Tuple[int, int, int]] = {
    "normal": (100, 120, 160),
    "blocked": (180, 60, 60),
    "restricted": (220, 140, 50),
    "priority": (70, 180, 100),
}

DRONE_COLORS: List[Tuple[int, int, int]] = [
    (255, 220, 80),
    (120, 200, 255),
    (255, 140, 120),
    (180, 255, 160),
    (220, 160, 255),
    (255, 200, 120),
    (140, 255, 240),
    (255, 180, 200),
]

ANSI_COLORS: Dict[str, str] = {
    "red": "\033[91m",
    "green": "\033[92m",
    "blue": "\033[94m",
    "yellow": "\033[93m",
    "cyan": "\033[96m",
    "magenta": "\033[95m",
    "orange": "\033[38;5;208m",
    "gray": "\033[90m",
    "grey": "\033[90m",
    "white": "\033[97m",
    "black": "\033[30m",
    "purple": "\033[35m",
    "pink": "\033[95m",
}

ANSI_RESET = "\033[0m"
ANSI_BOLD = "\033[1m"
ANSI_DIM = "\033[2m"


def parse_named_color(name: Optional[str]) -> Optional[Tuple[int, int, int]]:
    if not name:
        return None
    return NAMED_COLORS.get(name.lower())


def zone_fill_color(zone: Zone, map_data: MapData) -> Tuple[int, int, int]:
    if zone.name == map_data.start_hub:
        return parse_named_color(zone.color) or (60, 210, 210)
    if zone.name == map_data.end_hub:
        return parse_named_color(zone.color) or (240, 210, 70)
    if zone.color:
        return (parse_named_color(zone.color) or
                ZONE_TYPE_COLORS[zone.zone_type])
    return ZONE_TYPE_COLORS.get(zone.zone_type, ZONE_TYPE_COLORS["normal"])


def zone_border_color(fill: tuple[int, int, int]) -> tuple[int, int, int]:
    r, g, b = fill
    return (
        max(0, r - 45),
        max(0, g - 45),
        max(0, b - 45),
    )


def text_on_color(fill: Tuple[int, int, int]) -> Tuple[int, int, int]:
    return (20, 20, 30) if sum(fill) > 420 else (245, 245, 250)


def drone_color(drone_id: str) -> Tuple[int, int, int]:
    idx = int(drone_id[1:]) - 1 if drone_id[1:].isdigit() else 0
    return DRONE_COLORS[idx % len(DRONE_COLORS)]


def unique_connections(map_data: MapData) -> List[Tuple[str, str, int]]:
    seen = set()
    result = []
    for conn in map_data.connections:
        pair = tuple(sorted((conn.zone1, conn.zone2)))
        if pair in seen:
            continue
        seen.add(pair)
        result.append((conn.zone1, conn.zone2, conn.max_link_capacity))
    return result


def get_turn_moves(
    paths: Dict[str, List[Tuple[str, int]]],
) -> List[Tuple[int, List[str]]]:
    max_t = max((p[-1][1] for p in paths.values() if p), default=0)
    turns: List[Tuple[int, List[str]]] = []

    for t in range(1, max_t + 1):
        moves: List[str] = []
        for drone_id in sorted(paths.keys(), key=lambda x: int(x[1:])):
            path = paths[drone_id]
            curr_loc = None
            prev_loc = None
            for loc, turn in path:
                if turn == t:
                    curr_loc = loc
                if turn == t - 1:
                    prev_loc = loc

            if curr_loc and prev_loc and curr_loc != prev_loc:
                moves.append(f"{drone_id}-{curr_loc}")

        if moves:
            turns.append((t, moves))

    return turns


def current_locations(
    paths: Dict[str, List[Tuple[str, int]]],
    turn: int,
) -> Dict[str, Optional[str]]:
    result: Dict[str, Optional[str]] = {}
    for drone_id, path in paths.items():
        loc = None
        for step_loc, step_t in path:
            if step_t <= turn:
                loc = step_loc
            else:
                break
        result[drone_id] = loc
    return result


def ansi_for_color(name: Optional[str], fallback: str = "white") -> str:
    if not name:
        return ANSI_COLORS.get(fallback, ANSI_RESET)
    return ANSI_COLORS.get(name.lower(), ANSI_COLORS.get(fallback, ANSI_RESET))
