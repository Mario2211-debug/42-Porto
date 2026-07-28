from __future__ import annotations

from abc import ABC, abstractmethod

from ex0.creatures import Creature
from ex1.capabilities import HealCapability, TransformCapability


class BattleError(Exception):
    pass


class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        pass

    @abstractmethod
    def act(self, creature: Creature) -> list[str]:
        pass


class NormalStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return True

    def act(self, creature: Creature) -> list[str]:
        return [creature.attack()]


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> list[str]:
        if not self.is_valid(creature):
            raise BattleError(f"Invalid Creature '{creature.name}' "
                              "for this aggressive strategy")
        transformer = creature
        return [
            transformer.transform(),  # type: ignore[attr-defined]
            transformer.attack(),
            transformer.revert(),  # type: ignore[attr-defined]
        ]


class DefensiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, HealCapability)

    def act(self, creature: Creature) -> list[str]:
        if not self.is_valid(creature):
            raise BattleError(f"Invalid Creature '{creature.name}' "
                              "for this defensive strategy")
        healer = creature
        return [
            healer.attack(),
            healer.heal(),  # type: ignore[attr-defined]
        ]
