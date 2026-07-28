class Plant:
    class _Stats:
        def __init__(self):
            self._grow_count = 0
            self._age_count = 0
            self._show_count = 0

        def increment_grow(self) -> None:
            self._grow_count += 1
            pass

        def increment_age(self) -> None:
            self._age_count += 1
            pass

        def increment_show(self) -> None:
            self._show_count += 1
            pass

        def display(self) -> None:
            print(f"Stats: {self._grow_count} grow, "
                  f"{self._age_count} age, "
                  f"{self._show_count} show")
            pass

        """Classe Principal"""
    def __init__(self, name, age, height) -> None:
        self.name = name
        self._days = age
        self._height = height
        self.control = 0
        self.type = "None"
        self._stats = Plant._Stats()

    def anonymous(self):
        self.name = " Unknown plant"
        self._days = 0
        self._height = 0
        self.control = 0
        self._stats.increment_show()
        print(f"{self.name}: {round(self._days, 2)}cm, {self._days} days old")
        print(f"{'[statistics for Unknown plant]'}")
        print(f"Stats: {self._stats._grow_count} grow, "
              f" {self._stats._age_count} age, {self._stats._show_count} show")

    @staticmethod
    def age_check(age: int) -> bool:
        if age > 365:
            return True
        else:
            return False

    def show(self) -> str:
        self._stats.increment_show()
        return (f"{self.name}: {round(self._height, 2)}cm, "
                f"{self._days} years old")

    def age(self) -> None:
        self._stats.increment_age()
        self._days += 1
        pass

    def grow(self, value):
        self._height += value
        self._stats.increment_grow()
        pass

    def creation(self) -> None:
        print(f"{self.name}: {round(self._height, 2)}cm, "
              f"{self._days} years old")
        pass

    def get_stats(self) -> None:
        self._stats.display()


class Flower(Plant):
    def __init__(self, name, age, height, color):
        super().__init__(name, age, height)
        self.color = color
        self.bloomed = False
        self.type = "Flower"

    def bloom(self) -> None:
        self.bloomed = True
        pass

    def creation(self) -> None:
        super().creation()
        super().show()

        print(f"Color: {self.color}")
        if self.bloomed is False:
            print(f"{self.name} has not bloomed yet")
        else:
            print(f"{self.name} is blooming beautifully")
        pass

    def grow_and_blow(self, heigth: int) -> str:
        super().grow(heigth)
        self.bloom()
        return f"[make {self.name} grow, and bloom]"
    pass


class Tree(Plant):
    def __init__(self, name, age, height, diameter):
        super().__init__(name, age, height)
        self.trunk_diameter = diameter
        self.type = "Tree"
        self.shade = 0

    def produce_shade(self, value):
        print(f"[asking the {self.name} to produce shade]")
        self.trunk_diameter = value
        self.shade += 1
        super().show()
        print(f"Tree Oak now produces a shade of {round(self._height, 2)} cm, "
              f"long and {round(self.trunk_diameter, 2)}cm wide.")
        pass

    def get_stats(self):
        super().get_stats()
        print(f"shade {self.shade}")

    def creation(self):
        super().creation()
        super().show()
        if self.trunk_diameter != 0:
            print(f"Trunk Diameter: {self.trunk_diameter}")
    pass


class Seed(Flower):
    def __init__(self, name: str, age: int, height: int, color: str):
        super().__init__(name, age, height, color)
        self.color = color
        self.bloomed = False
        self.type = "Seed"
        self.seed = 0

    def creation(self) -> None:
        super().creation()
        print(f"Seeds: {self.seed}")
        pass

    def get_stats(self):
        return super().get_stats()

    def grow_and_blow_seed(self, value: int):
        print("[make sunflower grow, age and bloom")
        super().grow_and_blow(value)
        self.seed += 42
        return


plants: list = []

flower = Flower("Rose", 23, 16, "Red")
tree = Tree("Palm", 250, 170, 34)
seed = Seed("Sunflower", 45, 80, "Yellow")
anonym = Plant("Name", 0, 0)

plants.append(flower)
plants.append(tree)
plants.append(seed)
plants.append(anonym)

day_check_less: int = 30
day_check_more: int = 400


if __name__ == "__main__":
    print("=== Garden statistics ===")
    print("===  Check year-old ===")
    print(f"Is {day_check_less} days more than a year? ->"
          f"{Plant.age_check(day_check_less)}")
    print(f"Is {day_check_more} days more than a year? -> "
          f"{Plant.age_check(day_check_more)}\n")

    for plant in plants:

        if plant.type == "Flower":
            print("=== Flower")
            plant.creation()
            print(f"[statistics for {plant.name}]")
            plant.get_stats()
            if plant.bloomed is False:
                plant.grow_and_blow(5)
                plant.creation()
                print(f"[statistics for {plant.name}]")
                plant.get_stats()
                print("\n")

        if plant.type == "Tree":
            print("=== Tree")
            plant.creation()
            print(f"[statistics for {plant.name}]")
            plant.get_stats()
            if plant.trunk_diameter != 0:
                plant.produce_shade(2)
                print(f"[statistics for {plant.name}]")
                plant.get_stats()
                print("\n")

        if plant.type == "Seed":
            print("=== Seed")
            plant.creation()
            if plant.control == 0:
                plant.grow_and_blow_seed(5)
                plant.age()
                plant.creation()
                print(f"[statistics for {plant.name}]")
                plant.get_stats()
                print("\n")

        if plant.type == "None":
            print("=== Anonymous")
            plant.anonymous()
