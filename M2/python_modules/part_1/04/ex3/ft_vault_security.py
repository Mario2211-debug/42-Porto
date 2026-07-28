def secure_archive(filename: str, action: str,
                   content: str = "") -> tuple[bool, str]:
    try:
        if action == "r":
            with open(filename, "r") as f:
                data = f.read()
                return True, data
        elif action == "w":
            with open(filename, "w") as f:
                f.write(content)
                return True, "Content successfully written to file"
            pass
        else:
            return False, "Invalid mode"
    except Exception as e:
        return False, str(e)


def main() -> None:
    try:
        test0 = secure_archive("/not/existing/file", "r")
        print("\nUsing 'secure_archive' to read from a nonexistent file:")
        print(f"{test0}\n")

        test1 = secure_archive("/etc/master.passwd", "r")
        print("Using 'secure_archive' to read from a inaccessible file:")
        print(f"{test1}\n")

        test2 = secure_archive("ancient_fragment.txt", "r")
        print("Using 'secure_archive' to read from a regular file:")
        print(f"{test2}\n")

        test3 = secure_archive("new_file.txt", "w")
        print("Using 'secure_archive' to write "
              "previous content to a new file:")
        print(f"{test3}")

    except ValueError as e:
        print(f"Error as {e}")
    pass


if __name__ == "__main__":
    main()
