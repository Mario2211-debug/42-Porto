import sys
from typing import IO


def read_and_save_file(filename: str) -> list[str]:
    file: IO[str] | None = None

    print("=== Cyber Archives Recovery ===")
    print(f"Acessing file '{filename}'")
    try:
        file = open(filename, "r", encoding="utf-8")
        content = file.readlines()
        # file.close()
        print("---\n")
        for data in content:
            print(data, end="")
        print("\n---")
    except (OSError, FileNotFoundError, PermissionError) as e:
        print(f"[STDERR] Error opening file '{filename}': "
              f"[Errno {e.errno}] {e.strerror}")
        return []
    finally:
        if file is not None:
            file.close()
            print(f"File '{filename}' closed\n")
    return content


def new_file(data: list[str] | None):
    saved: bool = True
    if not data:
        return
    new_lines = [line.rstrip("\n") + "#\n" for line in data]
    print("Transform data:")
    print("---\n")
    for line in new_lines:
        print(line, end="")
    print("\n---")
    new_file_name = input("Enter new file name (or empty): ")

    if new_file_name:
        try:
            f = open(f"{new_file_name}", "w")
            print(f"Saving data to '{new_file_name}'")
            f.writelines(new_lines)
            f.close()
        except (IOError, FileNotFoundError, PermissionError) as e:
            saved = False
            print(f"Error opening file: {e}")
        finally:
            if saved is True:
                print(f"Data saved in file '{new_file_name}'.")
            else:
                print("Data not saved.")

    else:
        print("No data saved")


def main() -> None:
    content: list[str] | None
    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py")
        return
    content = read_and_save_file(sys.argv[1])
    new_file(content)


if __name__ == "__main__":
    main()
