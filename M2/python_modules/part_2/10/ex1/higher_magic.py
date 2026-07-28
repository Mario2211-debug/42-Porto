from collections.abc import Callable


Spell = Callable[[str, int], str]
Condition = Callable[[str, int], bool]


def spell_combiner(spell1: Spell, spell2: Spell) -> Callable[[str, int],
                                                             tuple[str, str]]:
    def combined(target: str, power: int) -> tuple[str, str]:
        return spell1(target, power), spell2(target, power)

    return combined


def power_amplifier(base_spell: Spell, multiplier: int) -> Spell:
    def amplified(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)

    return amplified


def conditional_caster(condition: Condition, spell: Spell) -> Spell:
    def conditional(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"

    return conditional


def spell_sequence(spells: list[Spell]) -> Callable[[str, int], list[str]]:
    def sequence(target: str, power: int) -> list[str]:
        return [spell(target, power) for spell in spells]

    return sequence


def fireball(target: str, power: int) -> str:
    return f"Fireball hits {target} for {power} damage"


def heal(target: str, power: int) -> str:
    return f"Heal restores {target} for {power} HP"


if __name__ == "__main__":
    print("Testing spell combiner...")
    combined = spell_combiner(fireball, heal)
    print(f"Combined spell result: {combined('Dragon', 10)}")
    print("Testing power amplifier...")
    boosted = power_amplifier(fireball, 3)
    print(f"Original: {fireball('Dragon', 10)}")
    print(f"Amplified: {boosted('Dragon', 10)}")
    print("Testing conditional caster...")
    safe_spell = conditional_caster(lambda target, power: power >= 5
                                    and bool(target), fireball)
    print(safe_spell("Dragon", 4))
    print(safe_spell("Dragon", 6))
    print("Testing spell sequence...")
    sequence = spell_sequence([fireball, heal])
    print(sequence("Knight", 12))
