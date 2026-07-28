import math
from typing import Tuple


def get_player_pos() -> Tuple[float, float, float]:
    while True:
        try:
            user_input = input("Enter new coordinates as "
                               "floats in format 'x,y,z': ").strip()
            parts = [p.strip() for p in user_input.split(",")]
            if len(parts) != 3:
                print("Invalid syntax")
                continue
            x, y, z = map(float, parts)
            return (x, y, z)
        except ValueError as e:
            print(f"Error on parameter: {e}")
        except Exception:
            print("Invalid syntax")


def main() -> None:
    print("=== Game Coordinate System ===")

    print("Get a first set of coordinates")
    pos1 = get_player_pos()
    print(f"Got a first tuple: {pos1}")
    print(f"It includes: X={pos1[0]}, Y={pos1[1]}, Z={pos1[2]}")

    dist_to_center = math.sqrt(pos1[0]**2 + pos1[1]**2 + pos1[2]**2)
    print(f"Distance to center: {dist_to_center:.4f}")

    print("\nGet a second set of coordinates")
    pos2 = get_player_pos()

    dist_between = math.sqrt(
        (pos2[0] - pos1[0])**2 +
        (pos2[1] - pos1[1])**2 +
        (pos2[2] - pos1[2])**2
    )
    print(f"Distance between the 2 sets of coordinates: {dist_between:.4f}")


if __name__ == "__main__":
    main()
