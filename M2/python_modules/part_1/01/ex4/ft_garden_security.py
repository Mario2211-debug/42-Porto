class Plant:
    def __init__(self, name, age, height) -> None:
        self.name = name
        self._days = age
        self._height = height

    def creation(self) -> None:
        print(f"Created: {self.name}: {round(self._height, 2)}cm, "
              f"{self._days} years old\n")
        pass

    """ Height """
    def set_height(self, height: int) -> None:
        if height < 0:
            print("Height update rejected")
            raise ValueError("Height can't be negative")
        self._height = height
        print(f"Heigth updated: {round(self._height, 2)}cm")
        pass

    def get_height(self) -> None:
        return self._height

    """ Age """
    def set_age(self, age: int) -> None:
        if age < 0:
            print("Height update rejected")
            raise ValueError("Age can't be negative")
        self._days = age
        print(f"Age updated: {self._days} days\n")
        pass

    def get_age(self) -> None:
        return self._days

    def curr_status(self) -> None:
        print(f"\nCurrent state: {self.name}: {round(self._height, 2)}cm, "
              f"{self._days} days old")
        pass


plant = Plant("Rose", 6, 5)

if __name__ == "__main__":
    print("=== Garden Security System ===")
    plant.creation()

    try:
        plant.set_height(25)
        plant.set_age(30)
    except ValueError as e:
        print(f"Error: {e}")
    try:
        plant.set_height(-56)
    except ValueError as e:
        print(f"Error: {e}")
    try:
        plant.set_age(-24)
    except ValueError as e:
        print(f"Error: {e}")
    plant.curr_status()
