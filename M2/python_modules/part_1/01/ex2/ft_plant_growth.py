class Plant:
    def __init__(self, name, age, height, week) -> None:
        self.name = name
        self.days = age
        self.height = height
        self.week = week
        self.control: int = 0

    def show(self) -> str:
        return (f"{self.name}: {round(self.height, 2)}cm, "
                f"{self.days} days old")

    def age(self) -> None:
        self.days += 1
        pass

    def grow(self):
        i = 0
        while i <= 7:
            print(f"== Day {i} ==")
            self.week += i
            self.age()
            self.control += 0.8
            self.height += 0.8
            print(self.show())
            i += 1
        self.grow_week()
        pass

    def grow_week(self):
        print(f"Grow this week {round(self.control)}cm")


plant = Plant("Rose", 6, 5, 3)

if __name__ == "__main__":
    print("=== Garden Plant Grow ===")
    plant.grow()
    pass
