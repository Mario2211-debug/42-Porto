from functools import lru_cache, partial, reduce, singledispatch
from operator import add, mul
from typing import Any


def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0
    operations = {
        "add": add,
        "multiply": mul,
        "max": lambda left, right: left if left >= right else right,
        "min": lambda left, right: left if left <= right else right,
    }
    if operation not in operations:
        raise ValueError("Unknown operation")
    return reduce(operations[operation], spells)


def partial_enchanter(base_enchantment):
    return {
        "fire": partial(base_enchantment, 50, "fire"),
        "water": partial(base_enchantment, 50, "water"),
        "earth": partial(base_enchantment, 50, "earth"),
    }


@lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n < 2:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher():
    @singledispatch
    def dispatch(value: Any) -> str:
        return "Unknown spell type"

    @dispatch.register
    def _(value: int) -> str:
        return f"Damage spell: {value} damage"

    @dispatch.register
    def _(value: str) -> str:
        return f"Enchantment: {value}"

    @dispatch.register
    def _(value: list) -> str:
        return f"Multi-cast: {len(value)} spells"

    return dispatch


def enchant(power: int, element: str, target: str) -> str:
    return f"{element.title()} enchantment with {power} power on {target}"


if __name__ == "__main__":
    print("Testing spell reducer...")
    values = [10, 20, 30, 40]
    print(f"Sum: {spell_reducer(values, 'add')}")
    print(f"Product: {spell_reducer(values, 'multiply')}")
    print(f"Max: {spell_reducer(values, 'max')}")
    print(f"Min: {spell_reducer(values, 'min')}")
    print("Testing partial enchanter...")
    variants = partial_enchanter(enchant)
    print(variants["fire"]("Sword"))
    print(variants["water"]("Shield"))
    print("Testing memoized fibonacci...")
    print(f"Fib(0): {memoized_fibonacci(0)}")
    print(f"Fib(1): {memoized_fibonacci(1)}")
    print(f"Fib(10): {memoized_fibonacci(10)}")
    print(f"Fib(15): {memoized_fibonacci(15)}")
    print("Testing spell dispatcher...")
    dispatcher = spell_dispatcher()
    print(dispatcher(42))
    print(dispatcher("fireball"))
    print(dispatcher(["spark", "heal", "barrier"]))
    print(dispatcher({"oops": True}))
