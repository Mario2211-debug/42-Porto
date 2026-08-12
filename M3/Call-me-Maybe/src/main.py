import sys
import time
import argparse
from pathlib import Path
from typing import Sequence
from .services.parser import Parser, ParserError
from .models import FunctionCall, FunctionDefinition
from .services.functoin_caller import FunctionCaller
from .services.vocab_map import VocabMap, VocabMapError
from .services.functoin_caller import FunctionCallerError
from .services.result_writer import ResultWriter, ResultWriterError


DEFAULT_MODEL = "Qwen/Qwen-0.6B"
DEFAULT_OUTPUT = Path("data/output/function_calling_result.json")
DEFAULT_INPUT = Path("data/input/function_calling_tests.json")
DEFAULT_FUNCTIONS = Path("data/input/functions_definition.json")


def parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parses the command line.

    Args:
        argv: Argument list, defaulting to ``sys.argv[1:]``.

    Returns:
        The parsed arguments.
    """
    parser = argparse.ArgumentParser(
        prog="python -m src",
        description=(
            "Translate natural language prompts into function calls using "
            "constrained decoding on a small language model."
        ),
    )
    parser.add_argument(
        "--functions_definition", type=Path, default=DEFAULT_FUNCTIONS,
        help=f"JSON file describing the callable functions "
             f"(default: {DEFAULT_FUNCTIONS})",
    )
    parser.add_argument(
        "--input", type=Path, default=DEFAULT_INPUT,
        help=f"JSON file with the prompts to process "
             f"(default: {DEFAULT_INPUT})",
    )
    parser.add_argument(
        "--output", type=Path, default=DEFAULT_OUTPUT,
        help=f"JSON file to write the results to (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--model", default=DEFAULT_MODEL,
        help=f"Hugging Face model id to use (default: {DEFAULT_MODEL})",
    )
    return parser.parse_args(argv)


def build_caller(model_name: str,
                 functions: list[FunctionDefinition]) -> FunctionCaller:
    from llm_sdk import Small_LLM_Model  # type: ignore[attr-defined]

    start = time.perf_counter()
    try:
        model = Small_LLM_Model()
        vocab_map = VocabMap(model.get_path_to_vocab_file())
    except VocabMapError as exc:
        raise RuntimeError(str(exc)) from exc
    except Exception as exc:
        raise RuntimeError(f"Could not load model {model_name}: {exc}"
                           ) from exc
    finally:
        print(f"[build_caller] took {time.perf_counter() - start:.3f}s")
    return FunctionCaller(model=model,
                          vocab_map=vocab_map, functions=functions)


def process_prompts(caller: FunctionCaller,
                    prompts: list[str]) -> tuple[list[FunctionCall],
                                                 list[str]]:
    results = []
    failures: list[str] = []
    total = len(prompts)

    for position, prompt in enumerate(prompts, start=1):
        try:
            call = caller.call(prompt)
        except FunctionCallerError as exc:
            failures.append(f"{prompt!r}: {exc.reason}")
            print(f"[{position}/{total}] failed: {prompt!r}", file=sys.stderr)
            continue
        results.append(call)
        print(f"[{position}/{total}] {call.name}, {call.parameters}")
    return results, failures


def main(argv: Sequence[str] | None = None) -> int:

    parser = Parser()
    start = time.perf_counter()
    arguments = parse_arguments(argv)

    try:
        functions = parser.load_functions(arguments.functions_definition)
        prompts = parser.load_prompts(arguments.input)
    except ParserError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    try:
        caller = build_caller(model_name=DEFAULT_MODEL, functions=functions)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    try:
        results, failures = process_prompts(caller, prompts)
        elapsed = time.perf_counter() - start
        minutes, seconds = divmod(elapsed, 60)
        print(f"[build_caller] took {int(minutes)}m {seconds:.2f}s")
    except KeyboardInterrupt:
        print("\nInterrupted, writing what was processed so far",
              file=sys.stderr)
        return 1

    try:
        ResultWriter().write(arguments.output, results)
    except ResultWriterError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
