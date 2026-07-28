import random
from typing import List, Dict


def main() -> None:
    print("=== Game Data Alchemist ===")

    players: List[str] = ['Alice', 'bob', 'Charlie', 'dylan', 'Emma',
                          'Gregory', 'john', 'kevin', 'Liam']

    # All capitalized
    capitalized_all = [p.capitalize() for p in players]
    print(f"Initial list of players: {players}")
    print(f"New list with all names capitalized: {capitalized_all}")

    # Only already capitalized
    capitalized_only = [p for p in players if p[0].isupper()]
    print(f"New list of capitalized names only: {capitalized_only}")

    # Score dictionary with comprehension
    score_dict: Dict[str, int] = {name: random.randint(50, 999)
                                  for name in capitalized_all}
    print(f"Score dict: {score_dict}")

    avg = sum(score_dict.values()) / len(score_dict)
    print(f"Score average is {avg:.2f}")

    # High scores comprehension
    high_scores = {name: score for name, score in score_dict.items()
                   if score > avg}
    print(f"High scores: {high_scores}")


if __name__ == "__main__":
    main()
