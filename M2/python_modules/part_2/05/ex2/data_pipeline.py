from abc import ABC, abstractmethod
from typing import Any, Protocol


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
            self._queque.append((self._processed_count, str(value)))
            self._processed_count += 1

    def output(self) -> tuple[int, str]:
        # print(self._queque)
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
            for _ in data:
                item = [f"{d['log_level']}: {d['log_message']}" for d in data]
            self._store(item)
        else:
            self._store(data)


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        pass
    pass


class CsvExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("CSV Output:")
        print(",".join(value for _, value in data))
    pass


class JsonExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("JSON Output:")
        pairs = [f'"item_{rank}: {value}"' for rank, value in data]
        print("{"+", ".join(pairs) + "}")
        pass
    pass


class DataStream:
    def __init__(self):
        self._processors: list[DataProcessor] = []
        pass

    def register_processor(self, proc: DataProcessor):
        if proc in self._processors:
            print(f"{type(proc).__name__} already registered")
        else:
            self._processors.append(proc)
            # print(f"{type(proc).__name__} registered!")
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

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for processor in self._processors:
            data_list = []
            for _ in range(nb):
                try:
                    data_list.append(processor.output())
                except (IndexError):
                    break
            plugin.process_output(data_list)
        pass


number_procesor = NumericProcessor()
text_procesor = TextProcessor()
log_procesor = LogProcessor()
csv = CsvExportPlugin()
json = JsonExportPlugin()


def main():
    stream = DataStream()
    print("Initialize Data Stream...")

    # First Line
    stream.print_processors_stats()
    batch_data1 = [
        "Hello world", [3.14, -1, 2.71],
        [{"log_level": "WARNING",
          "log_message": "Telnet access! Use ssh instead"
          }, {"log_level": "INFO",
              "log_message": "User wil is connected"}],
        42, ["Hi", "five"],]

    batch_data2 = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [{"log_level": "WARNING",
          "log_message": "Telnet access! Use ssh instead"},
         {"log_level": "INFO",
         "log_message": "User wil is connected"}],
        [32, 42, 64, 84, 128, 168], "World Hello"]
    print("\nRegistering Processors\n")
    stream.register_processor(number_procesor)
    stream.register_processor(text_procesor)
    stream.register_processor(log_procesor)

    print(f"\nSend first batch data on stream: {batch_data1}\n")
    try:
        stream.process_stream(batch_data1)
        stream.print_processors_stats()
        print()
        print(f"Send {3} processed data from each processor to a CSV plugin:")
        stream.output_pipeline(3, csv)

        print(f"\nSend another batch of data: {batch_data2}\n")
        stream.process_stream(batch_data2)
        stream.print_processors_stats()
        print()
        print(f"Send {5} processed data from each processor to a JSON plugin:")
        stream.output_pipeline(5, json)

        print()
        stream.print_processors_stats()
    except (ValueError, IndexError) as e:
        print(f"{e}")


if __name__ == "__main__":
    print("=== Code Nexusm - Data Pipeline ===")
    main()
