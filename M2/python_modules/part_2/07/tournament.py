from __future__ import annotations

from ex0.factories import AquaFactory, CreatureFactory, FlameFactory
from ex1.factories import HealingCreatureFactory, TransformCreatureFactory
from ex2.strategies import AggressiveStrategy, BattleError
from ex2.strategies import BattleStrategy, DefensiveStrategy, NormalStrategy


def run_tournament(opponents:
                   list[tuple[CreatureFactory, BattleStrategy]]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")
    try:
        for index, (left_factory, left_strategy) in enumerate(opponents):
            for right_factory, right_strategy in opponents[index + 1:]:
                left = left_factory.create_base()
                right = right_factory.create_base()
                print()
                print("* Battle *")
                print(left.describe())
                print("vs.")
                print(right.describe())
                print("now fight!")
                for action in left_strategy.act(left):
                    print(action)
                for action in right_strategy.act(right):
                    print(action)
    except BattleError as error:
        print(f"Battle error, aborting tournament: {error}")


if __name__ == "__main__":
    print("Tournament 0 (basic)")
    print("[ (Flameling+Normal), (Healing+Defensive) ]")
    run_tournament([
        (FlameFactory(), NormalStrategy()),
        (HealingCreatureFactory(), DefensiveStrategy()),
    ])
    print()
    print("Tournament 1 (error)")
    print("[ (Flameling+Aggressive), (Healing+Defensive) ]")
    run_tournament([
        (FlameFactory(), AggressiveStrategy()),
        (HealingCreatureFactory(), DefensiveStrategy()),
    ])
    print()
    print("Tournament 2 (multiple)")
    print("[ (Aquabub+Normal), (Healing+Defensive), (Transform+Aggressive) ]")
    run_tournament([
        (AquaFactory(), NormalStrategy()),
        (HealingCreatureFactory(), DefensiveStrategy()),
        (TransformCreatureFactory(), AggressiveStrategy()),
    ])
