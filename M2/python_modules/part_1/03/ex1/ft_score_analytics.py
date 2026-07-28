import sys
errors: list = []


def parse_scores(args: list[str]) -> list[int]:
    """Parse command-line arguments into a list of valid integer scores."""
    scores: list[int] = []
    for arg in args:
        try:
            scores.append(int(arg))
        except ValueError:
            print(f"Invalid parameter: '{arg}'")
    return scores


def main() -> None:
    """Process game scores and display statistics."""
    print("=== Player Score Analytics ===")

    raw_args: list[str] = sys.argv[1:]

    if not raw_args:
        print(
            "No scores provided. "
            "Usage: python3 ft_score_analytics.py <score1> <score2> ..."
        )
        return

    scores: list[int] = parse_scores(raw_args)

    if not scores:
        print(
            "No scores provided. "
            "Usage: python3 ft_score_analytics.py <score1> <score2> ..."
        )
        return

    total: int = sum(scores)
    average: float = total / len(scores)
    high: int = max(scores)
    low: int = min(scores)
    score_range: int = high - low

    print(f"Scores processed: {scores}")
    print(f"Total players: {len(scores)}")
    print(f"Total score: {total}")
    print(f"Average score: {average}")
    print(f"High score: {high}")
    print(f"Low score: {low}")
    print(f"Score range: {score_range}")


if __name__ == "__main__":
    main()
