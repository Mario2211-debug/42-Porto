from typing import Dict, Optional
from io import TextIOWrapper
import sys

from model import (
    MapData,
    Zone,
    Connection,
    ZoneType,
)


class Parser ():
    def __init__(self) -> None:
        self.valid_zone_types = {
            "normal",
            "blocked",
            "restricted",
            "priority",
        }

    def parse_options(self,
                      options_list: list[str]
                      ) -> Dict[str, Optional[str]]:
        """
        Parse metadata options from a list of bracket-enclosed strings.

        Args:
            options_list: List of strings like
            ['[zone=normal]', '[color=red]'].

        Returns:
            Dictionary mapping option keys to values. Options without '='
            are stored with None as value.

        Example:
            >>> parse_options(['[zone=priority]',
            '[color=green]', '[max_drones=2]'])
            {'zone': 'priority', 'color': 'green', 'max_drones': '2'}
            >>> parse_options(['[blocked]'])
            {'blocked': None}
        """
        options_dict: Dict[str, Optional[str]] = {}

        for op in options_list:
            op = op.strip("[]")
            if "=" in op:
                key, value = op.split("=", 1)
                options_dict[key] = value
            else:
                options_dict[op] = None

        return options_dict

    def parse(self, file: TextIOWrapper) -> MapData:
        """Parse the input file and return a MapData object.

        The file must follow the expected format with:
            - nb_drones: positive integer
            - start_hub: name x y [metadata]
            - end_hub: name x y [metadata]
            - hub: name x y [metadata]
            - connection: zone1-zone2 [metadata]

        Args:
            file: A file-like object opened for reading.

        Returns:
            MapData object containing all parsed zones and connections.

        Raises:
            ValueError: If the file
            format is invalid or required fields are missing.
            Exception: For any other unexpected parsing errors.

        Example:
            >>> with open("map.txt", "r") as f:
            ...     data = parser(f) """

        data = file.readlines()
        conf = MapData()
        self.valid_zone_types = {"normal", "blocked", "restricted", "priority"}

        for line_num, line in enumerate(data, 1):
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            try:
                if line.startswith("nb_drones:"):
                    _, value = line.split(":", 1)
                    try:
                        conf.nb_drones = int(value.strip())
                    except ValueError:
                        raise ValueError(
                            f"Line {line_num}: nb_drones must be an integer, "
                            f"got '{value.strip()}'"
                        )

                elif line.startswith("start_hub:"):
                    _, values = line.split(":", 1)
                    parts = values.strip().split()

                    if len(parts) < 3:
                        raise ValueError(
                            f"Line {line_num}: start_hub requires name x y, "
                            f"got {len(parts)} arguments"
                        )

                    name = parts[0]

                    """Validate zone name (without spaces or hyphens)"""
                    if " " in name or "-" in name:
                        raise ValueError(
                            f"Line {line_num}: zone name '{name}' contains "
                            f"spaces or dashes (not allowed)"
                        )

                    try:
                        x = int(parts[1])
                        y = int(parts[2])
                    except ValueError as e:
                        raise ValueError(
                            f"Line {line_num}: coordinates must be integers"
                        ) from e

                    options = self.parse_options(parts[3:])

                    """Validate zone_type"""
                    zone_type = options.get("zone", "normal")
                    if zone_type not in self.valid_zone_types:
                        raise ValueError(
                            f"Line {line_num}: "
                            f"invalid zone type '{zone_type}'. "
                            f"Must be one of: "
                            f"{', '.join(self.valid_zone_types)}"
                        )

                    """Validate max_drones (start_hub ignores,
                    but we validate if present)"""
                    max_drones = int(options.get("max_drones") or 1)
                    if max_drones <= 0:
                        raise ValueError(
                            f"Line {line_num}: max_drones must be positive, "
                            f"got {max_drones}"
                        )

                    """Check for duplicates"""
                    if name in conf.zones:
                        raise ValueError(
                            f"Line {line_num}: duplicate zone '{name}' "
                            f"(already defined at line {conf.zones[name].x})"
                        )

                    zone = Zone(
                        name=name,
                        x=x,
                        y=y,
                        max_drones=max_drones,
                        color=options.get("color"),
                        zone_type=ZoneType(zone_type),
                    )

                    conf.zones[name] = zone
                    conf.start_hub = name

                elif line.startswith("end_hub:"):
                    _, values = line.split(":", 1)
                    parts = values.strip().split()

                    if len(parts) < 3:
                        raise ValueError(
                            f"Line {line_num}: end_hub requires name x y, "
                            f"got {len(parts)} arguments"
                        )

                    name = parts[0]

                    """Validate zone name (without spaces or hyphens)"""
                    if " " in name or "-" in name:
                        raise ValueError(
                            f"Line {line_num}: zone name '{name}' contains "
                            f"spaces or dashes (not allowed)"
                        )

                    try:
                        x = int(parts[1])
                        y = int(parts[2])
                    except ValueError as e:
                        raise ValueError(
                            f"Line {line_num}: coordinates must be integers"
                        ) from e

                    options = self.parse_options(parts[3:])

                    """Validate zone_type"""
                    zone_type = options.get("zone", "normal")
                    if zone_type not in self.valid_zone_types:
                        raise ValueError(
                            f"Line {line_num}: invalid "
                            f"zone type '{zone_type}'. "
                            f"Must be one of: "
                            f"{', '.join(self.valid_zone_types)}"
                        )

                    """Validate max_drones (end_hub ignores,
                    but we validate if present)"""
                    max_drones = int(options.get("max_drones") or 1)
                    if max_drones <= 0:
                        raise ValueError(
                            f"Line {line_num}: max_drones must be positive, "
                            f"got {max_drones}"
                        )

                    # Verificar duplicados
                    if name in conf.zones:
                        raise ValueError(
                            f"Line {line_num}: duplicate zone '{name}' "
                            f"(already defined at line {conf.zones[name].x})"
                        )

                    zone = Zone(
                        name=name,
                        x=x,
                        y=y,
                        max_drones=max_drones,
                        color=options.get("color"),
                        zone_type=ZoneType(zone_type),
                    )

                    conf.zones[name] = zone
                    conf.end_hub = name

                elif line.startswith("hub:"):
                    _, values = line.split(":", 1)
                    parts = values.strip().split()

                    if len(parts) < 3:
                        raise ValueError(
                            f"Line {line_num}: hub requires name x y, "
                            f"got {len(parts)} arguments"
                        )

                    name = parts[0]

                    """Validate zone name (without spaces or hyphens)"""
                    if " " in name or "-" in name:
                        raise ValueError(
                            f"Line {line_num}: zone name '{name}' contains "
                            f"spaces or dashes (not allowed)"
                        )

                    try:
                        x = int(parts[1])
                        y = int(parts[2])
                    except ValueError as e:
                        raise ValueError(
                            f"Line {line_num}: coordinates must be integers"
                        ) from e

                    options = self.parse_options(parts[3:])

                    """Validate zone_type"""
                    zone_type = options.get("zone", "normal")
                    if zone_type not in self.valid_zone_types:
                        raise ValueError(
                            f"Line {line_num}: invalid"
                            f" zone type '{zone_type}'."
                            f"Must be one of:"
                            f"{', '.join(self.valid_zone_types)}"
                        )

                    """Validate max_drones"""
                    max_drones = int(options.get("max_drones") or 1)
                    if max_drones <= 0:
                        raise ValueError(
                            f"Line {line_num}: max_drones must be positive, "
                            f"got {max_drones}"
                        )

                    """Check for duplicates"""
                    if name in conf.zones:
                        raise ValueError(
                            f"Line {line_num}: duplicate zone '{name}' "
                            f"(already defined at line {conf.zones[name].x})"
                        )

                    conf.zones[name] = Zone(
                        name=name,
                        x=x,
                        y=y,
                        max_drones=max_drones,
                        color=options.get("color"),
                        zone_type=ZoneType(zone_type),
                    )

                elif line.startswith("connection:"):
                    _, values = line.split(":", 1)
                    parts = values.strip().split()

                    if len(parts) < 1:
                        raise ValueError(
                            f"Line {line_num}: connection requires name"
                        )

                    name = parts[0]

                    if "-" not in name:
                        raise ValueError(
                            f"Line {line_num}: connection name must be "
                            f"'zone1-zone2', got '{name}'"
                        )

                    """Check if there is more than one hyphen (e.g., a-b-c)"""
                    if name.count("-") > 1:
                        raise ValueError(
                            f"Line {line_num}: connection name '{name}' has "
                            f"multiple dashes, expected exactly one"
                        )

                    zone1, zone2 = name.split("-", 1)

                    """Validate zone names (without spaces)"""
                    if " " in zone1 or " " in zone2:
                        raise ValueError(
                            f"Line {line_num}: zone names contain spaces: "
                            f"'{zone1}' or '{zone2}'"
                        )

                    options = self.parse_options(parts[1:])

                    """Validate max_link_capacity"""
                    max_link_capacity = int(options.get("max_link_capacity")
                                            or 1)
                    if max_link_capacity <= 0:
                        raise ValueError(
                            f"Line {line_num}: "
                            "max_link_capacity must be positive, "
                            f"got {max_link_capacity}"
                        )

                    conf.connections.append(
                        Connection(
                            zone1=zone1,
                            zone2=zone2,
                            max_link_capacity=max_link_capacity,
                        )
                    )

                else:
                    raise ValueError(
                        f"Line {line_num}: unknown"
                        f" directive '{line.split()[0] if line else ''}'"
                    )

            except ValueError as e:
                print(f"Parser error at line {line_num}: {e}", file=sys.stderr)
                raise
            except Exception as e:
                print(f"Unexpected error at line"
                      f" {line_num}: {e}", file=sys.stderr)
                raise

        if conf.nb_drones <= 0:
            raise ValueError("nb_drones must be positive")

        if not conf.start_hub:
            raise ValueError("start_hub not found")

        if not conf.end_hub:
            raise ValueError("end_hub not found")

        if conf.start_hub == conf.end_hub:
            raise ValueError("start_hub and end_hub must be different")

        for zone_name, zone in conf.zones.items():

            """Validate zone_type (already validated
            during analysis, but reinforce)"""
            if zone.zone_type not in self.valid_zone_types:
                raise ValueError(
                    f"Zone '{zone_name}' has invalid type '{zone.zone_type}'"
                )

            """ max_drones must be positive
            (except start/end - these are ignored)"""
            if zone_name not in [conf.start_hub, conf.end_hub]:
                if zone.max_drones <= 0:
                    raise ValueError(
                        f"Zone '{zone_name}' max_drones must be positive, "
                        f"got {zone.max_drones}"
                    )

        """Check if the zones exist."""
        for conn in conf.connections:
            if conn.zone1 not in conf.zones:
                raise ValueError(
                    f"Connection '{conn.zone1}-{conn.zone2}' references "
                    f"undefined zone '{conn.zone1}'"
                )
            if conn.zone2 not in conf.zones:
                raise ValueError(
                    f"Connection '{conn.zone1}-{conn.zone2}' references "
                    f"undefined zone '{conn.zone2}'"
                )

        """Check for duplicate connections (a-b and b-a are duplicates)"""
        seen_connections = set()
        for conn in conf.connections:
            key = tuple(sorted((conn.zone1, conn.zone2)))
            if key in seen_connections:
                raise ValueError(
                    f"Duplicate connection: '{conn.zone1}-{conn.zone2}' "
                    f"(already exists as '{key[0]}-{key[1]}')"
                )
            seen_connections.add(key)

        """Check max_link_capacity
        (already validated during parsing, but reinforce it)"""
        for conn in conf.connections:
            if conn.max_link_capacity <= 0:
                raise ValueError(
                    f"Connection '{conn.zone1}-{conn.zone2}' "
                    f"max_link_capacity must be positive, "
                    f"got {conn.max_link_capacity}"
                )

        """Check for self-loop connections."""
        for conn in conf.connections:
            if conn.zone1 == conn.zone2:
                raise ValueError(
                    f"Error '{conn.zone1}-{conn.zone2}' connects a zone "
                    f"to itself (self-loop not allowed)"
                )

        """Check if start and end are connected (warning, not error)."""
        start_has_connection = False
        end_has_connection = False

        for conn in conf.connections:
            if conn.zone1 == conf.start_hub or conn.zone2 == conf.start_hub:
                start_has_connection = True
            if conn.zone1 == conf.end_hub or conn.zone2 == conf.end_hub:
                end_has_connection = True

        if not start_has_connection:
            raise ValueError(
                f"start_hub '{conf.start_hub}' has no connections")

        if not end_has_connection:
            raise ValueError(
                f"end_hub '{conf.end_hub}' has no connections")

        return conf
