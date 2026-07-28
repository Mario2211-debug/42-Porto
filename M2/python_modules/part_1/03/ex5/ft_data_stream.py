import random
from random import choice
from typing import Generator, List, Tuple

print("=== Game Data Stream Processor ===")

players: list = ["bod", "alice", "dylan", "charlie"]
actions: list = ["move", "sleep", "run", "sleep",
                 "eat", "grab", "climb", "release"]
ten_tuples = []


def gen_event() -> Generator[Tuple[str, str], None, None]:
    while True:
        player = choice(players)
        action = choice(actions)
        yield (player, action)


event_generator = gen_event()

for i in range(1000):
    event = next(event_generator)
    player, action = event
    print(f" Event {i}: player {player} did action {action}")


for i in range(10):
    event = next(event_generator)
    ten_tuples.append(event)
print(f"Built list of 10 events: {ten_tuples}")


def consume_event(events: List[Tuple[str, str]]) -> Generator[Tuple[str, str],
                                                              None, None]:
    while events:
        idx = random.randint(0, len(events) - 1)
        selected_event = events.pop(idx)
        yield selected_event


if __name__ == "__main__":
    for data in range(len(ten_tuples)):
        print(f"Got event from list:{next(consume_event(ten_tuples))}")
        print(f"Remains in list: {ten_tuples}")
