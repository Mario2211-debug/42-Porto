import os
import site
import sys


def in_virtualenv() -> bool:
    return (sys.prefix != getattr(sys, "base_prefix", sys.prefix)
            or hasattr(sys, "real_prefix"))


def main() -> None:
    inside: bool = in_virtualenv()
    if inside:
        print("MATRIX STATUS: Welcome to the construct")
        print()
        print(f"Current Python: {sys.executable}")
        print(f"Virtual Environment: {os.path.basename(sys.prefix)}")
        print(f"Environment Path: {sys.prefix}")
        print()
        print("SUCCESS: You're in an isolated environment!")
        print("Safe to install packages without affecting")
        print("the global system.")
        print()
        print("Package installation path:")
        paths = site.getsitepackages()
        print(paths[0] if paths else "No site-packages path found")
    else:
        print("MATRIX STATUS: You're still plugged in")
        print()
        print(f"Current Python: {sys.executable}")
        print("Virtual Environment: None detected")
        print()
        print("WARNING: You're in the global environment!")
        print("The machines can see everything you install.")
        print()
        print("To enter the construct, run:")
        print("python -m venv matrix_env")
        print("source matrix_env/bin/activate # On Unix")
        print(r"matrix_env\Scripts\activate # On Windows")
        print()
        print("Then run this program again.")


"""         for path in site.getsitepackages():
            print(path)
 """

if __name__ == "__main__":
    main()
    print(f"Teste: {getattr(sys, 'base_prefix', sys.prefix)}")
