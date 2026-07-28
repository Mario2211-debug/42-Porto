from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):

    def __init__(self):
        self._queque: list[tuple[int, str]] = []
        self._processed_count = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def _store(self, values: list) -> None:
        for value in values:
            self._queque.append((self._processed_count, value))
            self._processed_count += 1

    def output(self) -> tuple[int, str]:
        if not self._queque:
            raise IndexError("No more data in processor")
        return self._queque.pop(0)
    pass


class NumericProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, int | float):
            return True
        if isinstance(data, list):
            return all(isinstance(item, (int, float)) for item in data)

        return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper Numeric data")
        if isinstance(data, list):
            self._store(data)
        else:
            data = [data]
            self._store(data)


class TextProcessor(DataProcessor):
    def validate(self, data: Any):
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return all(isinstance(item, str) for item in data)

        return False

    def ingest(self, data: Any):
        if not self.validate(data):
            raise ValueError("Improper Text data")
        if isinstance(data, list):
            self._store(data)
        else:
            data = [data]
            self._store(data)


class LogProcessor(DataProcessor):
    def validate(self, data: Any):
        if isinstance(data, dict):
            return True
        if isinstance(data, list):
            return all(isinstance(item, dict) for item in data)

        return False

    def ingest(self, data: Any):
        if not self.validate(data):
            raise ValueError("Improper Log data")
        if isinstance(data, list):
            self._store(data)
        else:
            data = [data]
            self._store(data)


class DataStream:
    def __init__(self):
        self._processors: list[DataProcessor] = []
        pass

    def register_processor(self, proc: DataProcessor):
        if proc in self._processors:
            print(f"{type(proc).__name__} already registered")
        else:
            self._processors.append(proc)
            print(f"{type(proc).__name__} registered!")
        pass

    def process_stream(self, stream: list[tuple[Any]]):
        for element in stream:
            processed = False
            for processor in self._processors:
                if processor.validate(element):
                    processed = True
                    processor.ingest(element)
            if not processed:
                print("DataStream error -"
                      f" Can't process element in stream: {element}")
        pass

    def print_processors_stats(self):
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return
        for processor in self._processors:
            name = type(processor).__name__
            total = processor._processed_count
            remain = len(processor._queque)
            print(f"{name} Processor: total {total} "
                  f"items processed, remain {remain} on processor")
        pass


number_procesor = NumericProcessor()
text_procesor = TextProcessor()
log_procesor = LogProcessor()


def consume_data(data: DataProcessor, amount: int) -> None:
    for _ in range(amount):
        data.output()
    pass


def main():
    stream = DataStream()
    print("Initialize Data Stream...")

    # First Line
    stream.print_processors_stats()
    print()
    batch_data = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {"log_level": "WARNING",
             "log_message": "Telnet access! Use ssh instead"},
            {"log_level": "INFO",
             "log_message": "User wil is connected"},
        ],
        42,
        ["Hi", "five"],
    ]
    print("Registering Numeric Processor\n")
    stream.register_processor(number_procesor)
    print(f"Send first batch data on stream: {batch_data}")
    stream.process_stream(batch_data)
    stream.print_processors_stats()

    # Second Line
    print("\nRegistering other data processors")
    stream.register_processor(text_procesor)
    stream.register_processor(log_procesor)
    print("Send the same batch again")
    stream.process_stream(batch_data)
    stream.print_processors_stats()

    # Third
    print("\nConsume some elents from the"
          " data processors, Numeric 3, Text 2, Log 1")
    consume_data(number_procesor, 3)
    consume_data(text_procesor, 2)
    consume_data(log_procesor, 1)
    stream.print_processors_stats()


if __name__ == "__main__":
    print("=== Code Nexusm - Data Stream ===\n")
    main()
