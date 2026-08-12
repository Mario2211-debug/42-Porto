"""Builds the prompt handed to the model.

The grammar already guarantees the *shape* of the answer, so the prompt is not
responsible for producing valid JSON — it only has to give the model enough
context to pick the right function and to copy the right values out of the
request. Two things matter for that:

* the chat template. Qwen3 is instruction tuned; feeding it raw text instead
  of its ``<|im_start|>`` turns measurably degrades its choices;
* a compact, signature-like function list, which a 0.6B model follows far
  better than a nested JSON schema dump.
"""

from ..models import FunctionDefinition

_SYSTEM_PROMPT = """\
You are a function calling engine. You do not answer questions and you do \
not perform the task yourself: you only report which function should be \
called and with which arguments.

Available functions:
{functions}

Rules:
- Pick exactly one function from the list above.
- Provide every parameter that function declares.
- Copy argument values literally from the request: remove surrounding \
quotes, keep the original spelling, never translate or summarise.
- Never answer with a placeholder such as "value", "string" or "user_input".
- Numbers are written as bare numbers, text as a quoted string.

- A parameter that describes a pattern takes a regular expression matching \
what the request asks for, not the words of the request.

Examples, using functions that are NOT available here:
Request: Convert the text 'Good Morning' to upper case
Answer: {{"name": "fn_upper", "parameters": {{"text": "Good Morning"}}}}
Request: Multiply 7 by 6
Answer: {{"name": "fn_multiply", "parameters": {{"x": 7, "y": 6}}}}
Request: In 'a1 b2 c3' replace every digit with #
Answer: {{"name": "fn_sub", "parameters": {{"text": "a1 b2 c3", \
"pattern": "\\\\d", "with": "#"}}}}\
"""

_CHAT_TEMPLATE = (
    "<|im_start|>system\n{system}<|im_end|>\n"
    "<|im_start|>user\n{user}<|im_end|>\n"
    "<|im_start|>assistant\n<think>\n\n</think>\n\n"
)


class PromptBuilder:
    """Renders the system and user turns for a single request."""

    def build(self, user_prompt: str,
              functions: list[FunctionDefinition]) -> str:
        """Returns the full prompt text for *user_prompt*.

        Args:
            user_prompt: The natural language request to translate.
            functions: Functions the model may choose from.

        Returns:
            The prompt including chat template markers, ending right where
            the assistant answer begins.
        """
        system = _SYSTEM_PROMPT.format(
            functions=self._describe_functions(functions)
        )
        return _CHAT_TEMPLATE.format(system=system, user=user_prompt.strip())

    @staticmethod
    def _describe_functions(functions: list[FunctionDefinition]) -> str:
        """Renders each function as a signature plus its description."""
        lines: list[str] = []
        for function in functions:
            params = ", ".join(
                f"{name}: {schema.type.value}"
                for name, schema in function.parameters.items()
            )
            returns = (function.returns.type.value
                       if function.returns is not None else "null")
            lines.append(f"- {function.name}({params}) -> {returns}")
            if function.description:
                lines.append(f"    {function.description}")
        return "\n".join(lines)
