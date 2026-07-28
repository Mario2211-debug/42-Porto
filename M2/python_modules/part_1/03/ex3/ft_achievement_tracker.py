import random
print("=== Achievement Tracker System ===\n")

ALL_ACHIEVEMENTS = ['Crafting Genius', 'Strategist', 'World Savior',
                    'Speed Runner', 'Survivor',
                    'Master Explorer', 'Treasure Hunter', 'Unstoppable',
                    'First Steps',
                    'Collector Supreme', 'Untouchable', 'Sharp Mind',
                    'Boss Slayer', 'Hidden Path Finder']

players: list = []


def gen_players_achievments() -> set:
    count = random.randint(3, len(ALL_ACHIEVEMENTS))
    return set(random.sample(ALL_ACHIEVEMENTS, count))


class Player:
    def __init__(self, name):
        self.name = name
        self.achievments = gen_players_achievments()
        self.missing = set.difference(set(ALL_ACHIEVEMENTS), self.achievments)

    def show_achievmets(self) -> str:
        return f"Player {self.name}: {self.achievments}"

    def show_missing(self) -> str:
        return f"{self.name} is missing {self.missing}"


bob = Player("Bob")
charlie = Player("Charlie")
alice = Player("Alice")
dylan = Player("Dylan")
players.append(bob)
players.append(charlie)
players.append(alice)
players.append(dylan)


def main() -> None:
    print(f"{bob.show_achievmets()}")
    print(f"{charlie.show_achievmets()}")
    print(f"{alice.show_achievmets()}")
    print(f"{dylan.show_achievmets()}")

    common = set.intersection(
        bob.achievments,
        charlie.achievments)

    print()
    print(f"All distinct achievements: {set(ALL_ACHIEVEMENTS)}\n")
    print(f"Common achievements: {common}\n")
    for player in players:
        all = set.union(*[p.achievments for p in players if p != player])
        unique = player.achievments - all
        print(f"Only {player.name} has: {unique}")
    print()

    print(f"{alice.show_missing()}")
    print(f"{bob.show_missing()}")
    print(f"{charlie.show_missing()}")
    print(f"{dylan.show_missing()}")


if __name__ == "__main__":
    main()
