import sys


def main() -> None:
    raw = len(sys.argv)
    count = int(raw)
    print("=== Command Quest ===")
    print(f"Program name: {sys.argv[0]}")
    print(f"Arguments recived: {count - 1}")
    i = 1

    if count == 1:
        print("No arguments provided!")
    while i < count:
        print(f"Arguments {i}: {sys.argv[i]}")
        i += 1
    print(f"Total arguments: {count}")


if __name__ == "__main__":
    main()
