class GardenError(Exception):
    """Base class for all garden-related errors."""
    def __init__(self, message: str = "Unknown garden error") -> None:
        super().__init__(message)


class PlantError(GardenError):
    """Error related to plants."""
    def __init__(self, message: str = "Unknown plant error") -> None:
        super().__init__(message)


class WaterError(GardenError):
    """Error related to watering system."""
    def __init__(self, message: str = "Unknown water error") -> None:
        super().__init__(message)


def test_plant_error() -> None:
    raise PlantError("The tomato plant is wilting!")


def test_water_error() -> None:
    raise WaterError("Not enough water in the tank!")


def test_custom_errors() -> None:
    """Demonstrate custom exceptions and inheritance."""
    print("=== Custom Garden Errors Demo ===\n")

    print("Testing PlantError...")
    try:
        test_plant_error()
    except PlantError as e:
        print(f"Caught PlantError: {e}")

    print("\nTesting WaterError...")
    try:
        test_water_error()
    except WaterError as e:
        print(f"Caught WaterError: {e}")

    print("\nTesting catching all garden errors...")
    for error_func in [test_plant_error, test_water_error]:
        try:
            error_func()
        except GardenError as e:  # Catches both PlantError and WaterError
            print(f"Caught GardenError: {e}")

    print("\nAll custom error types work correctly!")


if __name__ == "__main__":
    test_custom_errors()
