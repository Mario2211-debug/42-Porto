from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class ZoneType(str, Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    PRIORITY = "priority"
    RESTRICTED = "restricted"


@dataclass
class Zone:
    name: str
    x: int
    y: int
    max_drones: int = 1
    color: Optional[str] = None
    zone_type: ZoneType = ZoneType.NORMAL


@dataclass
class Connection:
    zone1: str
    zone2: str
    max_link_capacity: int = 1


@dataclass
class Drone:
    id: str
    current_zone: str
    in_transit: bool = False
    target_zone: Optional[str] = None
    transit_connection: Optional[str] = None


@dataclass
class MapData:
    nb_drones: int = 0
    start_hub: str = ""
    end_hub: str = ""
    zones: Dict[str, Zone] = field(default_factory=dict)
    connections: List[Connection] = field(default_factory=list)
