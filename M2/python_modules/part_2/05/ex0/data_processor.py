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


numeric: list = [42, "Hello", "foo", [1, 2, 3, 4, 5]]
text: list = ['Hello', 'Nexus', 'World']
logs: list[dict] = [
    {
        'log_level': 'NOTICE',
        'log_message': 'Connection to server'
    }, {
        'log_level': 'ERROR',
        'log_message': 'Unauthorized access!!'
    }]


test: list[tuple[int, str]] = [(0, "hola"), (1, "bebe")]

number_procesor = NumericProcessor()
text_procesor = TextProcessor()
log_procesor = LogProcessor()


def numeric_test(data: list) -> None:
    for item in numeric[:2]:
        print(f"Trying to validate input '{item}':"
              f" {number_procesor.validate(item)}")
    for item in data[3:]:
        try:
            if isinstance(item, str):
                print(f"Test invalid ingestion of string '{item}'"
                      f"without prior validation:")
            number_procesor.ingest(item)
        except Exception as e:
            print(f"Got exception: {e}")
        if isinstance(item, list):
            print(f"Extracting {len(item)} values... ")
            print(f"Processing data: {item}")
            for d in item[:3]:
                number_procesor.ingest(d)
                idx, a = number_procesor.output()
                print(f"Numeric value {idx}: {a}")


def text_test(data: list[str]) -> None:
    print(f"Trying to validate input '{42}':"
          f" {text_procesor.validate(42)}")
    print(f"Processing data: {data}")
    print("Extracting 1 value...")
    for item in data[:1]:
        try:
            text_procesor.ingest(item)
            idx, a = text_procesor.output()
            print(f"Text value {idx}: {a}")
        except Exception as e:
            print(f"Got exception: {e}")


def log_test(data: list[dict]) -> None:
    print(f"Trying to validate input '{'Hello'}':"
          f" {log_procesor.validate('Hello')}")
    print(f"Processing data: {data}")
    print(f"Extracting {len(data)} value...")
    for item in data:
        try:
            log_procesor.ingest(item)
            idx, a = log_procesor.output()
            print(f"Text value {idx}: {a}")
        except Exception as e:
            print(f"Got exception: {e}")


if __name__ == "__main__":
    print("=== Code Nexusm - Data Processor ===")
    try:
        print("\nTesting Numeric Processor...")
        numeric_test(numeric)
        print("\nTesting Text Processor...")
        text_test(text)
        print("\nTesting Log Processor...")
        log_test(logs)
    except ValueError as e:
        print(f"{e}")
