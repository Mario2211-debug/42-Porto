import importlib.metadata
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tomli as tomllib
import pathlib


def check_dependencies(req_file: str = "requirements.txt") -> None:
    print("\nChecking dependencies:")
    path = pathlib.Path(req_file)

    if not path.exists():
        print(f"Arquivo {req_file} não encontrado!")
        return

    requirements = path.read_text().splitlines()
    for req in requirements:
        req = req.strip()
        if not req or req.startswith("#"):
            continue

        name = req.replace(">=", "==").replace("<=", "==").split("==")[0]

        try:
            installed = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            installed = "anyone"
        if name == "pandas":
            print(f"{'[MISSING]' if installed == 'anyone' else '[OK]'} "
                  f"{name} ({installed}) - Data manipulation "
                  f"{'not ready' if installed == 'anyone' else 'ready'}")
        if name == "numpy":
            print(f"{'[MISSING]' if installed == 'anyone' else '[OK]'} "
                  f"{name} ({installed}) - Numerical computation "
                  f"{'not ready' if installed == 'anyone' else 'ready'} ")
        if name == "requests":
            print(f"{'[MISSING]' if installed == 'anyone' else '[OK]'} "
                  f"{name} ({installed}) - Network access"
                  f"{'not ready' if installed == 'anyone' else 'ready'}")
        if name == "matplotlib":
            print(f"{'[MISSING]' if installed == 'anyone' else '[OK]'} "
                  f"{name} ({installed}) - Visualization manipulation "
                  f"{'not ready' if installed == 'anyone' else 'ready'}")


def check_toml(toml_file: str = "pyproject.toml") -> None:
    print("\nChecking Poetry dependencies (pyproject.toml):")
    path = pathlib.Path(toml_file)

    if not path.exists():
        print(f"Arquivo {toml_file} não encontrado!")
        return

    with open(path, "rb") as f:
        data = tomllib.load(f)

    print(data)
    # navega até às dependências do Poetry
    deps = data.get("tool", {}).get("poetry", {}).get("dependencies", {})

    for name, version_req in deps.items():
        if name == "python":  # ignora a versão do python
            continue

        try:
            installed = importlib.metadata.version(name)
            print(f"Installed:  {installed}")
            status = "[OK]"
        except importlib.metadata.PackageNotFoundError:
            installed = "not installed"
            status = "[MISSING]"

        print(f"{status} {name} — requerido: {version_req} "
              f"| instalado: {installed}")


def analysis_data() -> None:
    print("Analyzing Matrix data...")
    timelnie = np.linspace(0, 4 * np.pi, 1000)
    noise_data = np.random.normal(0, 15)
    matrix_energy = np.sin(timelnie + noise_data)
    data = pd.DataFrame(
        {
            "tick": np.arange(timelnie.size),
            "matrix_energy": matrix_energy,
            "stability_index": np.cos(timelnie)
        }
    )
    print("Generating visualization...")
    plt.figure(figsize=(10, 4))
    plt.plot(data["tick"], data["stability_index"], label="stability_index")
    plt.plot(data["tick"], data["matrix_energy"], label="matrix_energy")
    plt.title("Matrix Signal Analysis")
    plt.xlabel("tick")
    plt.ylabel("value")
    plt.legend()
    plt.tight_layout()
    output = "matrix_analysis.png"
    plt.savefig(output)
    print("Analysis complete!")
    print(f"Results saved to: {output}")


def main() -> None:
    print("LOADING STATUS: Loading programs...")
    check_dependencies()
    print()
    check_toml()
    analysis_data()
    pass


if __name__ == "__main__":
    main()
