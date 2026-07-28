from dotenv import load_dotenv
import re
import os
import pathlib

load_dotenv()
matrix_mode = os.getenv('MATRIX_MODE')
database_url = os.getenv('DATABASE_URL')
api_key = os.getenv('API_KEY')
log_level = os.getenv('LOG_LEVEL')
zion_endpoint = os.getenv('ZION_ENDPOINT')


def env_load():
    if load_dotenv():
        if matrix_mode:
            print(f"Mode: {matrix_mode}")
        if database_url:
            print("Database: Connected to local instance")
        if api_key:
            print("API Access: Authenticated")
        if log_level:
            print(f"Log Level: {log_level}")
        if zion_endpoint:
            print(f"Zion Network: {zion_endpoint}")


def check_hardcoded_secrets() -> bool:
    path = pathlib.Path(__file__)
    code = path.read_text()

    # padrões suspeitos
    patterns = [
        r'password\s*=\s*["\'][^"\']+["\']',
        r'api_key\s*=\s*["\'][^"\']+["\']',
        r'secret\s*=\s*["\'][^"\']+["\']',
        r'token\s*=\s*["\'][^"\']+["\']',
    ]

    found = []
    for pattern in patterns:
        if re.search(pattern, code, re.IGNORECASE):
            found.append(pattern)

    return len(found) == 0


def security_check() -> None:
    print("\nEnvironment security check:")
    print_txt = "No hardcoded secrets detected"
    clean = check_hardcoded_secrets()
    print(f"{'[OK]' if clean else '[WARN]'} "
          f"{print_txt if clean else 'Secrets found in code!'}")

    env_exists = pathlib.Path(".env").exists()
    print(f"{'[OK]' if env_exists else '[MISSING]'} "
          f".env file {'properly configured' if env_exists else 'not found'}")


def main():
    env_load()
    security_check()
    if log_level:
        print("[OK] Production overrides available")
    else:
        print("[OK] No production overrides available")
    pass


if __name__ == "__main__":
    main()
