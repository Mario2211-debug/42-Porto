from ex0.factories import AquaFactory, CreatureFactory, FlameFactory


def test_factory(factory: CreatureFactory) -> None:
    print("Testing factory")
    base = factory.create_base()
    evolved = factory.create_evolved()
    print(base.describe())
    print(base.attack())
    print(evolved.describe())
    print(evolved.attack())


def test_battle(first: CreatureFactory, second: CreatureFactory) -> None:
    print("Testing battle")
    left = first.create_base()
    right = second.create_base()
    print(left.describe())
    print("vs.")
    print(right.describe())
    print("fight!")
    print(left.attack())
    print(right.attack())


if __name__ == "__main__":
    flame_factory = FlameFactory()
    aqua_factory = AquaFactory()
    test_factory(flame_factory)
    print()
    test_factory(aqua_factory)
    print()
    test_battle(flame_factory, aqua_factory)
