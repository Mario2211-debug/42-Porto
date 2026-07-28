def ft_count_harvest_recursive(days: int) -> None:
    def helper(n: int) -> None:
        if n <= 0:
            return
        helper(n - 1)
        print(f"{n}")
    helper(days)
    print("Harvest time!")
