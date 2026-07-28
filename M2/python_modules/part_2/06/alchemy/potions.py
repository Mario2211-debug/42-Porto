from elements import create_fire, create_water
from alchemy import elements, create_air


def healing_potion() -> str:
    return f"Healing potion brewed with '{elements.create_earth()}' and '{create_air()}'"


def strength_potion() -> str:
    return f"Strength potion brewed with '{create_fire()}' and '{create_water()}'"
