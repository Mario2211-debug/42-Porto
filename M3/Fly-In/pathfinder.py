import heapq
from typing import Dict, List, Tuple, DefaultDict
from collections import defaultdict
from model import MapData, ZoneType


class Pathfinder:
    """Time-expanded, capacity-aware pathfinder for the drone routing
    simulation.

    Internally runs an A*-style search over a "time-expanded" state
    space of (zone, turn) pairs: each state additionally accounts for
    the zone and connection capacity already reserved by previously
    routed drones, so drones planned later route around conflicts
    instead of colliding with earlier ones.
    """
    def __init__(self, map_data: MapData):
        """Initialize the pathfinder for a given map.

        Args:
            map_data: The parsed map (zones, connections, drone count)
                to route drones through.
        """
        self.map_data = map_data
        self.zone_res: DefaultDict[str,
                                   DefaultDict[int, int]] = defaultdict(
                                       lambda: defaultdict(int))
        self.conn_res: DefaultDict[Tuple[str, str],
                                   DefaultDict[int, int]] = defaultdict(
                                       lambda: defaultdict(int))

    def get_occupancy(self, zone: str, turn: int) -> int:
        """Return how many drones are reserved in a zone at a given turn."""
        inner: Dict[int, int] = self.zone_res.get(zone, {})
        return inner.get(turn, 0)

    def get_zone_capacity(self, zone: str) -> float:
        """Return the maximum number of drones a zone may hold at once.

        The start and end hubs have unlimited capacity regardless of
        any `max_drones` metadata present in the map file; every other
        zone uses its configured `max_drones` value.

        Args:
            zone: Name of the zone to look up.

        Returns:
            The zone's capacity as a float, or `float('inf')` for the
            start/end hubs.
        """
        if zone == self.map_data.start_hub or zone == self.map_data.end_hub:
            return float('inf')
        return self.map_data.zones[zone].max_drones

    def get_conn_capacity(self, z1: str, z2: str) -> int:
        """Return the max_link_capacity of the connection between two
        zones.

        Args:
            z1: Name of one endpoint zone.
            z2: Name of the other endpoint zone, matched in the same
                order as it was declared in the map file (connections
                are undirected, but this lookup is direction-sensitive).

        Returns:
            The connection's max_link_capacity, or 0 if no matching
            connection exists.
        """
        for c in self.map_data.connections:
            if c.zone1 == z1 and c.zone2 == z2:
                return c.max_link_capacity
        return 0

    def bfs(self) -> None:
        """Compute an admissible heuristic distance from every zone to
        the end hub.

        Runs a Dijkstra-like relaxation (weighted BFS) backwards from
        `end_hub`, where each hop into a zone costs 2 turns if that
        zone is `restricted` and 1 turn otherwise. `blocked` zones are
        treated as unreachable and never relaxed into. The resulting
        distances are stored in `self.h` and used as the heuristic for
        the A* search in `find_path`.
        """
        dist = {z: float('inf') for z in self.map_data.zones}
        dist[self.map_data.end_hub] = 0
        queue = [self.map_data.end_hub]

        while queue:
            curr = queue.pop(0)

            for c in self.map_data.connections:
                if c.zone1 == curr:
                    neighbor = c.zone2
                elif c.zone2 == curr:
                    neighbor = c.zone1
                else:
                    continue
                neighbor_type = self.map_data.zones[neighbor].zone_type
                if neighbor_type == ZoneType.BLOCKED:
                    continue
                cost = 2 if neighbor_type == ZoneType.RESTRICTED else 1
                if dist[curr] + cost < dist[neighbor]:
                    dist[neighbor] = dist[curr] + cost
                    queue.append(neighbor)
        self.h = dist

    def find_path(self, start_t: int) -> List[Tuple[str, int]]:
        """Find the cheapest capacity-respecting path for a single
        drone, from the start hub to the end hub.

        Performs an A* search over (zone, turn) states. From each
        state, the drone may either wait in its current zone for one
        turn (if the zone has spare capacity at the next turn) or move
        along any available connection, provided the destination zone
        and the connection itself have spare capacity for every turn
        of the transit. Moves into a `restricted` zone take 2 turns,
        during which the drone occupies an in-transit pseudo-location
        named "`<from>-<to>`" (matching the connection's name) rather
        than a real zone. `priority` zones get a small negative cost
        bonus so the search favors them when costs would otherwise tie.

        Args:
            start_t: The simulation turn at which the drone starts its
                journey from the start hub.

        Returns:
            A list of (location, turn) pairs describing the full path,
            including any in-transit pseudo-locations for multi-turn
            moves, or an empty list if no valid path exists given the
            capacity already reserved by earlier drones.
        """
        visited = set()
        end = self.map_data.end_hub
        start = self.map_data.start_hub
        queue = [(self.h[start], 0, start, start_t, [(start, start_t)])]

        while queue:
            f, g, curr, t, path = heapq.heappop(queue)

            if curr == end:
                return path
            if (curr, t) in visited:
                continue
            visited.add((curr, t))

            curr_cap = self.get_zone_capacity(curr)
            can_wait = (curr == start) or self.zone_res[curr][t + 1] < curr_cap
            if can_wait:
                wait_path = list(path)
                wait_path.append((curr, t + 1))
                heapq.heappush(queue, (self.h[curr] + g + 1, g + 1, curr, t +
                                       1, wait_path))

            for c in self.map_data.connections:
                if c.zone1 == curr:
                    dest = c.zone2
                elif c.zone2 == curr:
                    dest = c.zone1
                else:
                    continue
                dest_type = self.map_data.zones[dest].zone_type
                dest_cap = self.get_zone_capacity(dest)
                dest_cost = 2 if dest_type == ZoneType.RESTRICTED else 1
                arr_time = dest_cost + t

                if dest_type == ZoneType.BLOCKED:
                    continue
                if self.zone_res[dest][t + dest_cost] >= dest_cap:
                    continue

                can_move = True
                for transit_t in range(t, arr_time):
                    if self.conn_res[(curr,
                                      dest)][transit_t] >= c.max_link_capacity:
                        can_move = False
                        break
                if can_move:
                    move_path = list(path)

                    for transit_t in range(t + 1, arr_time):
                        move_path.append((f"{curr}-{dest}", transit_t))
                    move_path.append((dest, arr_time))

                    g_penalty = float(dest_cost)

                    if dest_type == ZoneType.PRIORITY:
                        g_penalty -= 0.1
                    heapq.heappush(queue,
                                   (self.h[dest] + g + g_penalty,
                                    g + dest_cost, dest, arr_time,
                                    move_path))
        return []

    def reserve(self, path: List[Tuple[str, int]]) -> None:
        """Reserve the zone and connection capacity used by a drone's
        path, so subsequent `find_path` calls for later drones avoid
        conflicting with it.

        Waiting in place reserves that zone's capacity for the turn
        being waited into (the start hub is exempt, since it has
        unlimited capacity). Moving between two real zones reserves
        the destination zone for its arrival turn and the connection
        for the turn of departure. Multi-turn moves (e.g. into a
        `restricted` zone) pass through an in-transit pseudo-location
        (named "`<from>-<to>`") in `path`; this method recognizes that
        pseudo-location and reserves the connection capacity under the
        real `(from, to)` zone pair, for every turn of the transit,
        rather than reserving anything against the pseudo-location
        itself.

        Args:
            path: The (location, turn) path returned by `find_path`.
        """
        for i in range(1, len(path)):
            curr_zone, curr_t = path[i]
            prev_zone, prev_t = path[i - 1]

            if curr_zone == prev_zone:
                if curr_zone != self.map_data.start_hub:
                    self.zone_res[curr_zone][curr_t] += 1
            else:
                self.zone_res[curr_zone][curr_t] += 1
                self.conn_res[(prev_zone, curr_zone)][prev_t] += 1

    def solve(self) -> Dict[str, List[Tuple[str, int]]]:
        """Compute a conflict-free path for every drone in the map.

        Drones are routed one at a time, in id order (D1, D2, ...):
        each drone's path is planned with `find_path`, immediately
        reserved with `reserve`, and only then is the next drone
        planned. This greedy, sequential strategy means later drones
        always route around the capacity already consumed by earlier
        ones.

        Returns:
            A mapping of drone id (e.g. "D1") to its (location, turn)
            path, as returned by `find_path`. A drone for which no
            path could be found maps to an empty list.
        """
        paths = {}
        self.bfs()
        drones = self.map_data.nb_drones
        for i in range(1, drones + 1):
            drone_id = f"D{i}"
            path = self.find_path(0)
            self.reserve(path)
            paths[drone_id] = path
        return paths
