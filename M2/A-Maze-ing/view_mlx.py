"""MLX view for a_maze_ing - the graphical version.

The maze is drawn into an MLX image that is refreshed from a loop hook
(the Wayland/Vulkan backend never sends expose events). Keys: 1 to
regenerate, 2 to show/hide the solution path, 3 to change the wall
colour, 4 or ESC to quit.
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING, Literal

from mazegen import WALL_E, WALL_N, WALL_S, WALL_W

if TYPE_CHECKING:
    from a_maze_ing import MazeApp

_BG = 0xFF89CFF0
_ENTRY = 0xFFA6E3A1
_EXIT = 0xFFF38BA8
_PATH = 0xFF000000
_BLOCK = 0xFFFFFFFF

_WALL_COLOURS = [0xFFCDD6F4, 0xFF89DCEB, 0xFFA6E3A1,
                 0xFFF5C2E7, 0xFFFAB387]

_ESC = 65307


def run(app: MazeApp) -> bool:
    """Open the interactive MLX window.

    Args:
        app: the shared maze application state.

    Returns:
        True when the window ran to completion; False when the mlx
        library is missing, so the caller can fall back to the terminal.
    """
    try:
        from mlx import Mlx  # type: ignore
    except ImportError:
        print("mlx is not installed - falling back to the terminal view.")
        return False

    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    _, screen_w, screen_h = mlx.mlx_get_screen_size(mlx_ptr)

    width, height = app.config.width, app.config.height
    thickness = 2
    fit_w = max(1, (int(screen_w * 0.9) - thickness) // width)
    fit_h = max(1, (int(screen_h * 0.9) - thickness) // height)
    cell = max(8, min(48, fit_w, fit_h))
    win_w = width * cell + thickness
    win_h = height * cell + thickness

    img = mlx.mlx_new_image(mlx_ptr, win_w, win_h)
    data, _bpp, sl, fmt = mlx.mlx_get_data_addr(img)

    order: Literal["little", "big"] = "big" if fmt == 1 else "little"

    def pack(colour: int) -> bytes:
        """Pack an ARGB colour into the image's pixel byte order."""
        return colour.to_bytes(4, order)

    def fill(px: int, py: int, w: int, h: int, colour: int) -> None:
        """Fill a clipped rectangle of the image with a solid colour."""
        packed = pack(colour)
        for yy in range(max(0, py), min(win_h, py + h)):
            base = yy * sl
            for xx in range(max(0, px), min(win_w, px + w)):
                off = base + xx * 4
                data[off:off + 4] = packed

    state = {"show_path": False, "palette": 0}

    def draw_path() -> None:
        """Draw the solution path as a connected ribbon."""
        half = max(2, cell // 6)
        for x, y in app.path:
            cx = x * cell + cell // 2
            cy = y * cell + cell // 2
            fill(cx - half, cy - half, 2 * half, 2 * half, _PATH)
        for (x0, y0), (x1, y1) in zip(app.path, app.path[1:]):
            ax = x0 * cell + cell // 2
            ay = y0 * cell + cell // 2
            bx = x1 * cell + cell // 2
            by = y1 * cell + cell // 2
            fill(min(ax, bx) - half, min(ay, by) - half,
                 abs(bx - ax) + 2 * half, abs(by - ay) + 2 * half, _PATH)

    def draw() -> None:
        """Repaint the whole maze image from the current app state."""
        data[:] = pack(_BG) * (len(data) // 4)
        grid = app.generator.grid
        for bx, by in app.generator.blocked:
            fill(bx * cell, by * cell, cell + thickness,
                 cell + thickness, _BLOCK)
        if state["show_path"] and app.path:
            draw_path()
        for (px, py), colour in ((app.config.entry, _ENTRY),
                                 (app.config.exit, _EXIT)):
            fill(px * cell + thickness, py * cell + thickness,
                 cell - thickness, cell - thickness, colour)
        wall = _WALL_COLOURS[state["palette"]]
        for y in range(height):
            for x in range(width):
                v = grid[y][x]
                ox, oy = x * cell, y * cell
                if v & WALL_N:
                    fill(ox, oy, cell + thickness, thickness, wall)
                if v & WALL_W:
                    fill(ox, oy, thickness, cell + thickness, wall)
                if v & WALL_E:
                    fill(ox + cell, oy, thickness,
                         cell + thickness, wall)
                if v & WALL_S:
                    fill(ox, oy + cell, cell + thickness,
                         thickness, wall)

    win = mlx.mlx_new_window(mlx_ptr, win_w, win_h, "a_maze_ing")
    draw()

    def on_key(keycode: int, _param: object) -> None:
        """Handle a key release on the maze window."""
        if keycode in (52, 27, _ESC):
            mlx.mlx_loop_exit(mlx_ptr)
        elif keycode == 49:
            app.regenerate()
            draw()
        elif keycode == 50:
            state["show_path"] = not state["show_path"]
            draw()
        elif keycode == 51:
            state["palette"] = (state["palette"] + 1) % len(_WALL_COLOURS)
            draw()

    def on_close(_param: object) -> None:
        """Handle the window close button."""
        mlx.mlx_loop_exit(mlx_ptr)

    def render(_param: object) -> None:
        """Push the image to the window; called from the loop hook."""
        mlx.mlx_put_image_to_window(mlx_ptr, win, img, 0, 0)
        time.sleep(1 / 60)

    print("MLX window: 1 regenerate | 2 path | 3 colour | 4/ESC quit")
    mlx.mlx_put_image_to_window(mlx_ptr, win, img, 0, 0)
    mlx.mlx_loop_hook(mlx_ptr, render, None)
    mlx.mlx_expose_hook(win, render, None)
    mlx.mlx_key_hook(win, on_key, None)
    mlx.mlx_hook(win, 33, 0, on_close, None)
    mlx.mlx_loop(mlx_ptr)
    mlx.mlx_destroy_image(mlx_ptr, img)
    mlx.mlx_destroy_window(mlx_ptr, win)
    mlx.mlx_release(mlx_ptr)
    return True
