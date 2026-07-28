def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts,
                  key=lambda artifact: artifact["power"], reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda mage: mage["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda spell: f"* {spell} *", spells))


def mage_stats(mages: list[dict]) -> dict:
    return {
        "max_power": max(mages, key=lambda mage: mage["power"])["power"],
        "min_power": min(mages, key=lambda mage: mage["power"])["power"],
        "avg_power": round(sum(map(lambda mage: mage["power"], mages))
                           / len(mages), 2),
    }


if __name__ == "__main__":
    artifacts = [
        {"name": "Crystal Orb", "power": 85, "type": "focus"},
        {"name": "Fire Staff", "power": 92, "type": "weapon"},
        {"name": "Moon Blade", "power": 74, "type": "weapon"},
    ]
    spells = ["fireball", "heal", "shield"]
    mages = [
        {"name": "Aryn", "power": 40, "element": "fire"},
        {"name": "Borin", "power": 25, "element": "earth"},
        {"name": "Cyra", "power": 60, "element": "air"},
    ]
    print("Testing artifact sorter...")
    sorted_artifacts = artifact_sorter(artifacts)
    print(
        f"{sorted_artifacts[0]['name']} ({sorted_artifacts[0]['power']} power)"
        f"comes before {sorted_artifacts[1]['name']} "
        f"({sorted_artifacts[1]['power']} power)"
    )
    print("Testing spell transformer...")
    print(" ".join(spell_transformer(spells)))
    print("Testing power filter...")
    print(power_filter(mages, 30))
    print("Testing mage stats...")
    print(mage_stats(mages))
