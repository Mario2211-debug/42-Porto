import time
from collections.abc import Callable
from functools import wraps


def spell_timer(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Casting {func.__name__}...")
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Spell completed in {end - start:.3f} seconds")
        return result

    return wrapper


def power_validator(min_power: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            power = kwargs.get("power")
            if power is None:
                for value in reversed(args):
                    if isinstance(value, int):
                        power = value
                        break
            if power is None:
                power = 0
            if power < min_power:
                return "Insufficient power for this spell"
            return func(*args, **kwargs)

        return wrapper

    return decorator


def retry_spell(max_attempts: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts:
                        return "Spell casting failed after "
                    f"{max_attempts} attempts"
                    print("Spell failed, retrying... "
                          f"(attempt {attempt}/{max_attempts})")

        return wrapper

    return decorator


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        stripped = name.replace(" ", "")
        return len(name) >= 3 and stripped.isalpha()

    @power_validator(10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


@spell_timer
def fireball() -> str:
    time.sleep(0.1)
    return "Fireball cast!"


def unstable_spell_factory(failures: int) -> Callable[[], str]:
    attempts = {"count": 0}

    @retry_spell(3)
    def unstable_spell() -> str:
        attempts["count"] += 1
        if attempts["count"] <= failures:
            raise RuntimeError("boom")
        return "Waaaaaaagh spelled !"

    return unstable_spell


if __name__ == "__main__":
    print("Testing spell timer...")
    print(f"Result: {fireball()}")
    print("Testing retrying spell...")
    always_fail = unstable_spell_factory(5)
    print(always_fail())
    eventually_works = unstable_spell_factory(2)
    print(eventually_works())
    print("Testing MageGuild...")
    guild = MageGuild()
    print(MageGuild.validate_mage_name("Merlin"))
    print(MageGuild.validate_mage_name("X1"))
    print(guild.cast_spell("Lightning", 15))
    print(guild.cast_spell("Spark", 5))
