class TemperatureError(Exception):
    pass


def input_temperature(temp_str: str) -> int:
    try:
        temp: int = int(temp_str)
    except ValueError as e:
        raise ValueError(f"invalid literal for int() with base 10: "
                         f"'{temp_str}'") from e

    if temp < 0:
        raise TemperatureError(f"{temp}°C is too cold for plants (min 0°C)")
    if temp > 40:
        raise TemperatureError(f"{temp}°C is too hot for plants (max 40°C)")

    return temp


def test_temperature() -> None:
    """Test temperature validation with various cases."""
    print("=== Garden Temperature Checker ===\n")

    tests = ["25", "abc", "100", "-50"]

    for data in tests:
        print(f"Input data is '{data}'")
        try:
            temp = input_temperature(data)
            print(f"Temperature is now {temp}°C")
        except Exception as e:
            print(f"Caught input_temperature error: {e}")
        print()


if __name__ == "__main__":
    test_temperature()
    print("All tests completed - program didn't crash!")
