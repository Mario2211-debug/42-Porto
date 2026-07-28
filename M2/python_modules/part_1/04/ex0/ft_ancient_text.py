import sys
from typing import IO


def read_file(filename: str) -> None:
    file: IO[str] | None = None

    print("=== Cyber Archives Recovery ===")
    print(f"Acessing file '{filename}'")
    try:
        file = open(filename, "r", encoding="utf-8")
        content = file.read()
        print("---\n")
        print(content, end="")
        # file.close()
        print("\n---")
    except (OSError, FileNotFoundError, PermissionError) as e:
        print(f"Error opening file '{filename}': {e}")
    finally:
        if file is not None:
            file.close()
            print(f"File '{filename}' closed")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py <file>")
        return
    read_file(sys.argv[1])


if __name__ == "__main__":
    main()
