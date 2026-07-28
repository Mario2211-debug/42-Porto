def garden_operations(operation_number: int) -> None:
    """Simulate different types of errors based on operation number."""
    if operation_number == 0:
        # ValueError
        int("abc")
    elif operation_number == 1:
        # ZeroDivisionError
        10 / 0
    elif operation_number == 2:
        # FileNotFoundError
        open("/non/existent/file.txt")
    elif operation_number == 3:
        # TypeError
        "hello" + 42
    return


def test_error_types() -> None:
    """Test multiple error types with proper catching."""
    print("=== Garden Error Types Demo ===\n")

    for i in range(5):
        print(f"Testing operation {i}...")
        try:
            garden_operations(i)
            if i == 4:
                print("Operation completed successfully")
        except ValueError as e:
            print(f"Caught ValueError: {e}")
        except ZeroDivisionError as e:
            print(f"Caught ZeroDivisionError: {e}")
        except FileNotFoundError as e:
            print(f"Caught FileNotFoundError: {e}")
        except TypeError as e:
            print(f"Caught TypeError: {e}")
        except Exception as e:
            print(f"Caught unexpected error: {e}")
        # print()

    print("\nAll error types tested successfully!")


if __name__ == "__main__":
    test_error_types()
