def input_temperature(temp_str: str) -> int:
    """Convert string to integer temperature."""
    return int(temp_str)


def test_temperature() -> None:
    """Test temperature input with error handling."""
    print("=== Garden Temperature ===\n")

    tests = ["25", "abc"]

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
