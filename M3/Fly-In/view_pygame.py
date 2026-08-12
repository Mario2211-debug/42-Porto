# import os
# os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any

import pygame

from model import MapData
from visual_common import (
    DEFAULT_WINDOW_HEIGHT,
    DEFAULT_WINDOW_WIDTH,
    DRONE_FILL,
    DRONE_LABEL,
    DRONE_OUTLINE,
    FOOTER_HEIGHT,
    HEADER_HEIGHT,
    MIN_WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
    NAMED_COLORS,
    SIDEBAR_WIDTH,
    current_locations,
    get_turn_moves,
    text_on_color,
    unique_connections,
    zone_border_color,
    zone_fill_color,
)


class Constants:
    ZOOM_MIN = 0.25
    ZOOM_MAX = 4.0
    ZOOM_STEP = 1.12
    PLAY_DELAY = 45  # frames between turns when playing


@dataclass
class GraphLayout:
    base_scale: float
    node_radius: int
    drone_radius: int
    edge_width: int
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    show_edge_caps: bool
    show_zone_names: bool
    show_zone_meta: bool
    coord_font_size: int
    label_font_size: int


class ViewState:
    """Manages the current view state of the application."""

    def __init__(self) -> None:
        self.turn: int = 0
        self.playing: bool = False
        self.play_timer: int = 0
        self.sidebar_scroll: int = 0
        self.zoom: float = 1.0
        self.pan_x: float = 0.0
        self.pan_y: float = 0.0
        self.dragging: bool = False
        self.drag_origin: Tuple[int, int] = (0, 0)
        self.pan_origin: Tuple[float, float] = (0.0, 0.0)

    def reset_view(self) -> None:
        """Reset zoom and pan to default values."""
        self.zoom = 1.0
        self.pan_x = 0.0
        self.pan_y = 0.0

    def reset_turn(self) -> None:
        """Reset turn and playing state."""
        self.turn = 0
        self.playing = False
        self.play_timer = 0


class GraphRenderer:
    """Handles rendering of the graph visualization."""

    def __init__(self, map_data: MapData,
                 paths: Dict[str, List[Tuple[str, int]]]) -> None:
        self.map_data = map_data
        self.paths = paths
        self.turns = get_turn_moves(paths)
        self.turn_moves = dict(self.turns)
        self.max_t = self.turns[-1][0] if self.turns else 0

        # Fonts
        self.font = pygame.font.SysFont("dejavusans", 15)
        self.font_title = pygame.font.SysFont("dejavusans", 22, bold=True)
        self.font_small = pygame.font.SysFont("dejavusans", 13)
        self.font_coord: Optional[pygame.font.Font] = None
        self.font_label: Optional[pygame.font.Font] = None

        # Layout
        self.layout: Optional[GraphLayout] = None
        self.graph_rect = pygame.Rect(0, 0, 0, 0)
        self.sidebar_rect = pygame.Rect(0, 0, 0, 0)

        # State
        self.state = ViewState()

        # Window dimensions
        self.window_w = DEFAULT_WINDOW_WIDTH
        self.window_h = DEFAULT_WINDOW_HEIGHT

    def update_layout(self) -> None:
        """Update graph and sidebar rectangles and recompute layout."""
        self.graph_rect.update(
            16,
            HEADER_HEIGHT + 12,
            max(200, self.window_w - SIDEBAR_WIDTH - 32),
            max(200, self.window_h - HEADER_HEIGHT - FOOTER_HEIGHT - 24),
        )
        self.sidebar_rect.update(
            self.window_w - SIDEBAR_WIDTH + 4,
            HEADER_HEIGHT + 8,
            SIDEBAR_WIDTH - 12,
            max(200, self.window_h - HEADER_HEIGHT - 16),
        )
        self.layout = self._compute_layout()
        self.font_coord = pygame.font.SysFont(
            "dejavusans", self.layout.coord_font_size, bold=True
        )
        self.font_label = pygame.font.SysFont(
            "dejavusans", self.layout.label_font_size
        )

    def _compute_layout(self) -> GraphLayout:
        """Compute graph layout parameters based on current data."""
        min_x = min(z.x for z in self.map_data.zones.values())
        max_x = max(z.x for z in self.map_data.zones.values())
        min_y = min(z.y for z in self.map_data.zones.values())
        max_y = max(z.y for z in self.map_data.zones.values())
        n_zones = len(self.map_data.zones)

        count_x = max(1, max_x - min_x + 1)
        count_y = max(1, max_y - min_y + 1)

        pad_x = 36
        pad_top = 28
        pad_bottom = 40

        usable_w = max(120, self.graph_rect.width - pad_x * 2)
        usable_h = max(120, self.graph_rect.height - pad_top - pad_bottom)

        scale_x = usable_w / max(count_x - 1, 1)
        scale_y = usable_h / max(count_y - 1, 1)
        base_scale = min(scale_x, scale_y) * 1.15

        node_radius = max(6, min(26, int(base_scale * 0.40)))
        if n_zones > 20:
            node_radius = max(5, min(node_radius, 12))
        elif n_zones > 12:
            node_radius = max(6, min(node_radius, 16))

        drone_radius = max(3, min(8, node_radius - 1))
        edge_width = max(1, min(4, node_radius // 3))

        return GraphLayout(
            base_scale=base_scale,
            node_radius=node_radius,
            drone_radius=drone_radius,
            edge_width=edge_width,
            min_x=min_x,
            max_x=max_x,
            min_y=min_y,
            max_y=max_y,
            show_edge_caps=(base_scale >= 26 and
                            len(self.map_data.connections) // 2 <= 40),
            show_zone_names=base_scale >= 22 and n_zones <= 30,
            show_zone_meta=base_scale >= 34 and n_zones <= 14,
            coord_font_size=max(8, min(12, node_radius + 1)),
            label_font_size=max(8, min(11, node_radius)),
        )

    def _graph_center(self) -> Tuple[float, float]:
        """Get the center of the graph area."""
        return self.graph_rect.centerx, self.graph_rect.centery

    def _world_pos(self, zone_name: str) -> Tuple[float, float]:
        """Convert zone coordinates to world position."""
        assert self.layout is not None
        z = self.map_data.zones[zone_name]
        wx = (z.x - self.layout.min_x) * self.layout.base_scale
        wy = -(z.y - self.layout.min_y) * self.layout.base_scale
        return wx, wy

    def _node_pos(self, zone_name: str) -> Tuple[int, int]:
        """Get screen position of a zone node."""
        wx, wy = self._world_pos(zone_name)
        cx, cy = self._graph_center()
        px = int(cx + self.state.pan_x + wx * self.state.zoom)
        py = int(cy + self.state.pan_y + wy * self.state.zoom)
        return px, py

    def _scaled_radius(self, base: int) -> int:
        """Scale radius by current zoom level."""
        return max(2, int(base * self.state.zoom))

    def _zoom_at(self, factor: float, mx: int, my: int) -> None:
        """Zoom in/out at specific screen position."""
        old_zoom = self.state.zoom
        new_zoom = max(Constants.ZOOM_MIN, min(Constants.ZOOM_MAX,
                                               old_zoom * factor))
        if abs(new_zoom - old_zoom) < 1e-6:
            return
        cx, cy = self._graph_center()
        world_x = (mx - cx - self.state.pan_x) / old_zoom
        world_y = (my - cy - self.state.pan_y) / old_zoom
        self.state.zoom = new_zoom
        self.state.pan_x = mx - cx - world_x * new_zoom
        self.state.pan_y = my - cy - world_y * new_zoom

    def _draw_text(self, surf: pygame.Surface, x: int, y: int, text: str,
                   color: Tuple[int, int, int] = (230, 230, 240),
                   small: bool = False, bold: bool = False) -> None:
        """Draw text on surface."""
        f = self.font_small if small else (
            self.font_title if bold else self.font)
        img = f.render(text, True, color)
        surf.blit(img, (x, y))

    def draw_sidebar(self, surf: pygame.Surface, current_turn: int,
                     locs: Dict[str, Optional[str]]) -> None:
        """Draw the sidebar with legends, controls, and drone status."""
        pygame.draw.rect(surf, (22, 24, 38),
                         self.sidebar_rect, border_radius=10)
        pygame.draw.rect(surf, (55, 60, 85), self.sidebar_rect,
                         width=1, border_radius=10)

        x = self.sidebar_rect.x + 14
        y = self.sidebar_rect.y + 12
        bottom = self.sidebar_rect.bottom - 12

        self._draw_text(surf, x, y, "Legend", bold=True)
        y += 30

        for label, color_name in [
            ("Start", "cyan"), ("End", "yellow"), ("Normal", "blue"),
            ("Priority", "green"), ("Restricted", "orange"),
            ("Blocked", "red"),
        ]:
            swatch = NAMED_COLORS.get(color_name, (160, 160, 170))
            pygame.draw.circle(surf, swatch, (x + 7, y + 7), 6)
            self._draw_text(surf, x + 20, y, label, small=True)
            y += 18

        y += 6
        self._draw_text(surf, x, y, f"Turn {current_turn} / {self.max_t}",
                        bold=True)
        y += 24
        self._draw_text(
            surf, x, y,
            f"{self.map_data.nb_drones} drones · "
            f"{len(self.map_data.zones)} zones",
            (150, 155, 175), small=True,
        )
        y += 22

        self._draw_text(surf, x, y, "Controls", bold=True)
        y += 22
        for line in [
            "← → step turn", "Space play / pause", "R reset turn",
            "Drag graph pan", "Wheel graph zoom", "Wheel sidebar scroll",
            "+ / - zoom", "0 fit view", "Esc quit",
        ]:
            self._draw_text(surf, x, y, line, (150, 155, 175), small=True)
            y += 16

        y += 8
        self._draw_text(surf, x, y, "Drones (white)", bold=True)
        y += 20

        drone_list_top = y
        drone_ids = sorted(self.paths.keys(), key=lambda d: int(d[1:]))
        row_h = 16
        visible_rows = max(1, (bottom - 80 - drone_list_top) // row_h)
        max_scroll = max(0, len(drone_ids) - visible_rows)
        self.state.sidebar_scroll = max(0, min(self.state.sidebar_scroll,
                                               max_scroll))

        clip = pygame.Rect(self.sidebar_rect.x, drone_list_top,
                           self.sidebar_rect.width, visible_rows * row_h)
        surf.set_clip(clip)
        for idx, drone_id in enumerate(drone_ids):
            row_y = (drone_list_top +
                     (idx - self.state.sidebar_scroll) * row_h)
            if (row_y < drone_list_top or
                    row_y >= drone_list_top + visible_rows * row_h):
                continue
            loc = locs.get(drone_id) or "—"
            pygame.draw.circle(surf, DRONE_FILL, (x + 7, row_y + 7), 5)
            pygame.draw.circle(surf, DRONE_OUTLINE, (x + 7, row_y + 7), 5, 1)
            loc_short = loc if len(loc) <= 18 else loc[:16] + "…"
            self._draw_text(surf, x + 18, row_y, f"{drone_id}: {loc_short}",
                            small=True)
        surf.set_clip(None)

        move_y = bottom - 70
        self._draw_text(surf, x, move_y, "This turn", bold=True)
        move_y += 20
        moves = self.turn_moves.get(current_turn, [])
        if moves:
            for move in moves[:4]:
                self._draw_text(surf, x, move_y, move, (255, 220, 120),
                                small=True)
                move_y += 16
            if len(moves) > 4:
                self._draw_text(surf, x, move_y, f"+{len(moves) - 4} more",
                                (130, 135, 155), small=True)
        else:
            self._draw_text(surf, x, move_y, "(no moves)", (130, 135, 155),
                            small=True)

    def draw_graph(self, surf: pygame.Surface, current_turn: int,
                   locs: Dict[str, Optional[str]]) -> None:
        """Draw the graph with nodes, edges, and drones."""
        assert self.layout is not None
        pygame.draw.rect(surf, (16, 18, 30), self.graph_rect, border_radius=12)
        pygame.draw.rect(surf, (45, 50, 72), self.graph_rect,
                         width=1, border_radius=12)

        surf.set_clip(self.graph_rect.inflate(-4, -4))

        zoom = self.state.zoom
        node_r = self._scaled_radius(self.layout.node_radius)
        drone_r = self._scaled_radius(self.layout.drone_radius)
        edge_w = max(1, int(self.layout.edge_width * zoom))

        # Draw edges
        active_edges = set()
        for loc in locs.values():
            if loc and "-" in loc:
                a, b = loc.split("-", 1)
                active_edges.add(tuple(sorted((a, b))))

        for z1_name, z2_name, capacity in unique_connections(self.map_data):
            x1, y1 = self._node_pos(z1_name)
            x2, y2 = self._node_pos(z2_name)
            edge_key = tuple(sorted((z1_name, z2_name)))
            is_active = edge_key in active_edges

            edge_color = (110, 125, 185) if is_active else (50, 55, 75)
            pygame.draw.line(
                surf, edge_color, (x1, y1), (x2, y2),
                edge_w + (1 if is_active else 0),
            )

            if self.layout.show_edge_caps and zoom >= 0.6:
                mx = (x1 + x2) // 2
                my = (y1 + y2) // 2
                cap_label = self.font_small.render(str(capacity),
                                                   True, (140, 145, 165))
                cap_rect = cap_label.get_rect(center=(mx, my))
                pygame.draw.rect(
                    surf, (16, 18, 30),
                    cap_rect.inflate(6, 3), border_radius=3,
                )
                surf.blit(cap_label, cap_rect)

        # Draw zones
        for zone in self.map_data.zones.values():
            cx, cy = self._node_pos(zone.name)
            fill = zone_fill_color(zone, self.map_data)
            border = zone_border_color(fill)
            label_col = text_on_color(fill)

            pygame.draw.circle(surf, border, (cx, cy), node_r + 1)
            pygame.draw.circle(surf, fill, (cx, cy), node_r)

            if node_r >= 7:
                coord_size = max(8, min(
                    14, int(self.layout.coord_font_size * zoom)))
                coord_font = pygame.font.SysFont("dejavusans",
                                                 coord_size, bold=True)
                coord_surf = coord_font.render(f"({zone.x},{zone.y})",
                                               True, label_col)
                coord_rect = coord_surf.get_rect(center=(cx, cy))
                surf.blit(coord_surf, coord_rect)

            if self.layout.show_zone_names and zoom >= 0.7:
                name = (zone.name if len(zone.name) <= 10
                        else zone.name[:9] + "…")
                label_size = max(8,
                                 min(12,
                                     int(self.layout.label_font_size * zoom)))
                label_font = pygame.font.SysFont("dejavusans", label_size)
                name_surf = label_font.render(name, True, (195, 200, 215))
                name_rect = name_surf.get_rect(midtop=(cx, cy + node_r + 3))
                surf.blit(name_surf, name_rect)

                if self.layout.show_zone_meta:
                    meta = f"{zone.zone_type.value} cap - {zone.max_drones}"
                    meta_surf = label_font.render(meta, True, (120, 125, 145))
                    meta_rect = meta_surf.get_rect(
                        midtop=(cx, name_rect.bottom + 1))
                    surf.blit(meta_surf, meta_rect)

        # Draw drones
        drones_at: Dict[str, List[str]] = {}
        for drone_id, loc in locs.items():
            if not loc:
                continue
            drones_at.setdefault(loc, []).append(drone_id)

        for loc, drone_ids in drones_at.items():
            if "-" in loc:
                a, b = loc.split("-", 1)
                x1, y1 = self._node_pos(a)
                x2, y2 = self._node_pos(b)
                base_x = (x1 + x2) // 2
                base_y = (y1 + y2) // 2
            else:
                base_x, base_y = self._node_pos(loc)

            for i, drone_id in enumerate(sorted(drone_ids,
                                                key=lambda d: int(d[1:]))):
                angle = (2 * math.pi * i) / max(len(drone_ids), 1)
                offset = drone_r + 4
                px = int(base_x + offset * math.cos(angle))
                py = int(base_y + offset * math.sin(angle))

                pygame.draw.circle(surf, DRONE_OUTLINE, (px, py), drone_r + 1)
                pygame.draw.circle(surf, DRONE_FILL, (px, py), drone_r)

                if drone_r >= 5:
                    tag_size = max(7, int(9 * zoom))
                    tag_font = pygame.font.SysFont("dejavusans",
                                                   tag_size, bold=True)
                    tag = tag_font.render(drone_id[1:], True, DRONE_LABEL)
                    tag_rect = tag.get_rect(center=(px, py))
                    surf.blit(tag, tag_rect)

        surf.set_clip(None)


class PygameView:
    """Main application class managing the Pygame view."""

    def __init__(self, map_data: MapData,
                 paths: Dict[str, List[Tuple[str, int]]]):
        self.map_data = map_data
        self.paths = paths
        self.renderer: Optional[GraphRenderer] = None
        self.screen: Optional[pygame.Surface] = None
        self.clock = pygame.time.Clock()
        self.running = False

    def run(self) -> bool:
        """Main application loop."""
        pygame.init()

        self.screen = pygame.display.set_mode(
            (DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT),
            pygame.RESIZABLE
        )
        pygame.display.set_caption("Fly-In — Drone Routing Simulation")

        self.renderer = GraphRenderer(self.map_data, self.paths)
        self.renderer.update_layout()

        self.running = True

        while self.running:
            self.clock.tick(60)
            self._update()
            self._handle_events()
            self._draw()

        pygame.quit()
        return True

    def _update(self) -> None:
        """Update game state."""
        if not self.renderer:
            return

        state = self.renderer.state
        if state.playing and state.turn < self.renderer.max_t:
            state.play_timer += 1
            if state.play_timer >= Constants.PLAY_DELAY:
                state.play_timer = 0
                state.turn += 1
        elif state.turn >= self.renderer.max_t:
            state.playing = False

    def _handle_events(self) -> None:
        """Handle pygame events."""
        if not self.renderer or not self.screen:
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.VIDEORESIZE:
                self.renderer.window_w = max(MIN_WINDOW_WIDTH, event.w)
                self.renderer.window_h = max(MIN_WINDOW_HEIGHT, event.h)
                self.screen = pygame.display.set_mode(
                    (self.renderer.window_w, self.renderer.window_h),
                    pygame.RESIZABLE
                )
                self.renderer.update_layout()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_down(event)

            elif event.type == pygame.MOUSEBUTTONUP:
                self._handle_mouse_up(event)

            elif event.type == pygame.MOUSEMOTION:
                self._handle_mouse_motion(event)

            elif event.type == pygame.KEYDOWN:
                self._handle_key_down(event)

            elif event.type == pygame.MOUSEWHEEL:
                self._handle_mouse_wheel(event)

    def _handle_mouse_down(self, event: Any) -> None:
        """Handle mouse button down events."""
        if not self.renderer:
            return

        if event.button == 1 and self.renderer.graph_rect.collidepoint(
                    event.pos):
            self.renderer.state.dragging = True
            self.renderer.state.drag_origin = event.pos
            self.renderer.state.pan_origin = (
                self.renderer.state.pan_x,
                self.renderer.state.pan_y
            )
        elif event.button == 4 and self.renderer.graph_rect.collidepoint(
                    event.pos):
            self.renderer._zoom_at(Constants.ZOOM_STEP, *event.pos)
        elif event.button == 5 and self.renderer.graph_rect.collidepoint(
                    event.pos):
            self.renderer._zoom_at(1 / Constants.ZOOM_STEP, *event.pos)

    def _handle_mouse_up(self, event: Any) -> None:
        """Handle mouse button up events."""
        if not self.renderer:
            return

        if event.button == 1:
            self.renderer.state.dragging = False

    def _handle_mouse_motion(self, event: Any) -> None:
        """Handle mouse motion events."""
        if not self.renderer or not self.renderer.state.dragging:
            return

        dx = event.pos[0] - self.renderer.state.drag_origin[0]
        dy = event.pos[1] - self.renderer.state.drag_origin[1]
        self.renderer.state.pan_x = self.renderer.state.pan_origin[0] + dx
        self.renderer.state.pan_y = self.renderer.state.pan_origin[1] + dy

    def _handle_key_down(self, event: Any) -> None:
        """Handle keyboard key down events."""
        if not self.renderer:
            return

        state = self.renderer.state

        if event.key == pygame.K_ESCAPE:
            self.running = False
        elif event.key == pygame.K_RIGHT and state.turn < self.renderer.max_t:
            state.turn += 1
            state.play_timer = 0
        elif event.key == pygame.K_LEFT and state.turn > 0:
            state.turn -= 1
            state.play_timer = 0
        elif event.key == pygame.K_SPACE:
            state.playing = not state.playing
            state.play_timer = 0
        elif event.key == pygame.K_r:
            state.reset_turn()
        elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
            mx, my = pygame.mouse.get_pos()
            self.renderer._zoom_at(Constants.ZOOM_STEP, mx, my)
        elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
            mx, my = pygame.mouse.get_pos()
            self.renderer._zoom_at(1 / Constants.ZOOM_STEP, mx, my)
        elif event.key == pygame.K_0:
            state.reset_view()

    def _handle_mouse_wheel(self, event: Any) -> None:
        """Handle mouse wheel events."""
        if not self.renderer:
            return

        mx, my = pygame.mouse.get_pos()
        if self.renderer.sidebar_rect.collidepoint(mx, my):
            self.renderer.state.sidebar_scroll -= event.y
        elif self.renderer.graph_rect.collidepoint(mx, my):
            factor = (Constants.ZOOM_STEP if
                      event.y > 0 else 1 / Constants.ZOOM_STEP)
            self.renderer._zoom_at(factor, mx, my)

    def _draw(self) -> None:
        """Draw the entire frame."""
        if not self.renderer or not self.screen:
            return

        self.screen.fill((12, 14, 24))

        current_turn = self.renderer.state.turn
        locs = current_locations(self.paths, current_turn)

        self._draw_header()
        self.renderer.draw_graph(self.screen, current_turn, locs)
        self.renderer.draw_sidebar(self.screen, current_turn, locs)

        pygame.display.flip()

    def _draw_header(self) -> None:
        """Draw the header bar."""
        if not self.renderer or not self.screen:
            return

        header = pygame.Rect(0, 0, self.renderer.window_w, HEADER_HEIGHT)
        pygame.draw.rect(self.screen, (18, 20, 34), header)
        pygame.draw.line(self.screen, (55, 60, 85),
                         (0, HEADER_HEIGHT - 1),
                         (self.renderer.window_w, HEADER_HEIGHT - 1))

        state = self.renderer.state

        self.renderer._draw_text(self.screen, 20, 14, "Fly-In", bold=True)
        self.renderer._draw_text(
            self.screen, 100, 18,
            f"{self.map_data.start_hub} → {self.map_data.end_hub}  ·  "
            f"zoom {state.zoom:.0%}",
            (150, 155, 175), small=True,
        )

        status = "PLAYING" if state.playing else "PAUSED"
        status_color = (100, 220, 140) if state.playing else (220, 180, 80)
        self.renderer._draw_text(
            self.screen,
            max(400, self.renderer.window_w - SIDEBAR_WIDTH - 150),
            18,
            f"T{state.turn}/{self.renderer.max_t}  {status}",
            status_color, small=True,
        )
