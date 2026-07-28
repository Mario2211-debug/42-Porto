class Plant:
    """Base Plant class"""

    def __init__(self, name: str, height: float = 0.0, age: int = 0) -> None:
        self.name: str = name
        self._height: float = max(0.0, height)
        self._age: int = max(0, age)

    def grow(self) -> None:
        self._height += 1.0

    def age_day(self) -> None:
        self._age += 1

    def show(self) -> None:
        print(f"{self.name}: {self._height}cm, {self._age} days old")


class Flower(Plant):
    def __init__(self, name: str, height: float = 0.0, age: int = 0,
                 color: str = "white") -> None:
        super().__init__(name, height, age)
        self.color: str = color
        self._bloomed: bool = False

    def bloom(self) -> None:
        self._bloomed = True
        print(f"{self.name} is blooming beautifully!")

    def show(self) -> None:
        super().show()
        print(f"Color: {self.color}")
        if self._bloomed:
            print(f"{self.name} is blooming beautifully!")
        else:
            print(f"{self.name} has not bloomed yet")


class Tree(Plant):
    def __init__(self, name: str, height: float = 0.0, age: int = 0,
                 trunk_diameter: float = 0.0) -> None:
        super().__init__(name, height, age)
        self.trunk_diameter: float = trunk_diameter

    def produce_shade(self) -> None:
        print(f"Tree {self.name} now produces a shade of {self._height}cm long"
              f" and {self.trunk_diameter}cm wide.")

    def show(self) -> None:
        super().show()
        print(f"Trunk diameter: {self.trunk_diameter}cm")


class Vegetable(Plant):
    def __init__(self, name: str, height: float = 0.0, age: int = 0,
                 harvest_season: str = "Summer") -> None:
        super().__init__(name, height, age)
        self.harvest_season: str = harvest_season
        self.nutritional_value: int = 0

    def grow(self) -> None:
        super().grow()
        self.nutritional_value += 1

    def age_day(self) -> None:
        super().age_day()
        self.nutritional_value += 1

    def show(self) -> None:
        super().show()
        print(f"Harvest season: {self.harvest_season}")
        print(f"Nutritional value: {self.nutritional_value}")


def main() -> None:
    print("=== Garden Plant Types ===\n")

    # Flower
    print("=== Flower")
    rose = Flower("Rose", 15.0, 10, "red")
    rose.show()
    print("[asking the rose to bloom]")
    rose.bloom()
    rose.show()

    print("\n=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    print("[asking the oak to produce shade]")
    oak.produce_shade()

    print("\n=== Vegetable")
    tomato = Vegetable("Tomato", 5.0, 10, "April")
    tomato.show()
    print("[make tomato grow and age for 20 days]")
    for _ in range(20):
        tomato.grow()
        tomato.age_day()
    tomato.show()


if __name__ == "__main__":
    main()
