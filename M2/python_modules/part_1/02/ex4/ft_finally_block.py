print("=== Garden Watering System ===")


class GardenError(Exception):
    default_message = "Garden Error"

    def __init__(self, message):
        self.message = message
        super().__init__(message or self.default_message)


class PlantError(GardenError):
    default_message = "Plant error"

    def __init__(self, message):
        super().__init__(f"{message}" or self.default_message)


class Plant:
    def __init__(self, plant: str):
        self.name = plant


plant_list: list[Plant] = []
plant_list1: list[Plant] = []

tomato = Plant("Tomato")
lettecute = Plant("Lettuce")
carrot = Plant("Carrots")
plant1 = Plant("lettuce")

plant_list.append(tomato)
plant_list.append(lettecute)
plant_list.append(carrot)

plant_list1.append(tomato)
plant_list1.append(plant1)


def water_plant(plant) -> None:
    if plant.name != plant.name.capitalize():
        raise PlantError(f"Invalid plant name to water: '{plant.name}'")
    print(f"Watering {plant.name} [OK]")


def test_watering_system():
    print("\nTesting vavalid plants...")
    print("Opening watering system")
    for plant in plant_list:
        try:
            water_plant(plant)
        except PlantError as e:
            print(f"Caught PlantError: {e}\n")
    print("Closing watering system\n")

    print("Testing invalid plants...")
    print("Opening watering system")
    for plant in plant_list1:
        try:
            water_plant(plant)
        except PlantError as e:
            print(f"Caught PlantError: {e}")
    print(".. ending tests and returning to main")
    print("Closing watering system")


if __name__ == "__main__":
    test_watering_system()
    print("\nCleanup always happens, even with errors!")
