from ex1.factories import HealingCreatureFactory, TransformCreatureFactory


def test_healing() -> None:
    factory = HealingCreatureFactory()
    print("Testing Creature with healing capability")
    print("base:")
    base = factory.create_base()
    print(base.describe())
    print(base.attack())
    print(base.heal())  # type: ignore[attr-defined]
    print("evolved:")
    evolved = factory.create_evolved()
    print(evolved.describe())
    print(evolved.attack())
    print(evolved.heal())  # type: ignore[attr-defined]


def test_transform() -> None:
    factory = TransformCreatureFactory()
    print("Testing Creature with transform capability")
    print("base:")
    base = factory.create_base()
    print(base.describe())
    print(base.attack())
    print(base.transform())  # type: ignore[attr-defined]
    print(base.attack())
    print(base.revert())  # type: ignore[attr-defined]
    print("evolved:")
    evolved = factory.create_evolved()
    print(evolved.describe())
    print(evolved.attack())
    print(evolved.transform())  # type: ignore[attr-defined]
    print(evolved.attack())
    print(evolved.revert())  # type: ignore[attr-defined]


if __name__ == "__main__":
    test_healing()
    print()
    test_transform()
