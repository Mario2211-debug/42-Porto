*This project has been created as part of the 42 curriculum by mafonso.*

# Call Me Maybe

## Description

`call me maybe` turns natural language requests into structured function
calls. Given `"What is the sum of 40 and 2?"` it does **not** answer `42`; it
answers *which* function should be called and *with which arguments*:

```json
{"prompt": "What is the sum of 40 and 2?",
 "name": "fn_add_numbers",
 "parameters": {"a": 40.0, "b": 2.0}}
```

The model doing the work is `Qwen/Qwen3-0.6B`, a 0.6 billion parameter model
that, if simply asked nicely to "reply in JSON", gets the format wrong a large
fraction of the time. The output here is nevertheless **always** valid JSON
and **always** matches the declared schema, because the format is not left to
the model at all: it is enforced during decoding.

The program reads two input files — the function definitions and the prompts
to process — and writes one output file with the resulting calls.

## Instructions

### Install

```bash
uv sync
```

That is the only setup step: it creates the virtual environment, installs
`numpy`, `pydantic` and the provided `llm_sdk` (with PyTorch and
Transformers), and resolves everything from `uv.lock`. The model weights
themselves are downloaded from the Hugging Face Hub on the first run.

> On a 42 machine, keep the project and the `uv` cache in `/sgoinfre`; PyTorch
> alone will not fit in a home directory. See `notes.md`.

### Run

```bash
uv run python -m src
```

By default this reads `data/input/functions_definition.json` and
`data/input/function_calling_tests.json`, and writes
`data/output/function_calling_results.json`. All three can be overridden:

```bash
uv run python -m src \
    --functions_definition data/input/functions_definition.json \
    --input data/input/function_calling_tests.json \
    --output data/output/function_calls.json
```

`--model <hf-id>` selects a different model; the default is
`Qwen/Qwen3-0.6B`.

### Make targets

| Target | What it does |
| --- | --- |
| `make install` | `uv sync` |
| `make run` | Runs the program on the default files |
| `make debug` | Runs it under `pdb` |
| `make test` | Runs the test suite |
| `make lint` | `flake8 .` and `mypy .` with the required flags |
| `make lint-strict` | `flake8 .` and `mypy . --strict` |
| `make clean` | Removes `__pycache__`, `.mypy_cache`, `.pytest_cache` |
| `make fclean` | `clean` plus the generated `data/output/` |

## Algorithm: constrained decoding

A language model generates one token at a time. At each position it outputs a
*logit* — an unnormalised score — for every one of the ~151k tokens in its
vocabulary, and the next token is normally the highest scoring one.
Constrained decoding intervenes between those two moments: before choosing,
every token that would break the required structure is masked out, so the
model can only pick from continuations that keep the output valid.

### The grammar as a cursor

`SchemaGrammar` describes the only document we are willing to produce:

```
{"name": "<one of the declared functions>", "parameters": {<declared params>}}
```

as an ordered list of steps, of three kinds:

| Step | Example | Decided by |
| --- | --- | --- |
| `LITERAL` | `{"name": "`, `", "parameters": {`, `, "b": `, `}}` | nobody — it is fixed |
| `FUNCTION_NAME_CHOICE` | `fn_add_numbers` | the model |
| `PARAM_VALUE` | `2`, `"shrek"`, `true` | the model |

Only the first two steps exist up front. The moment the function name is
complete, the steps for *that* function's parameters are spliced in, in
declaration order — which is what makes the argument names, their order and
their types impossible to get wrong.

The grammar exposes two operations to the decoder:

* `is_token_valid(text)` — feeds the candidate token character by character
  into a *throwaway copy* of the cursor and reports whether every character
  was legal. Working on a copy is what makes validation free of side effects,
  and working character by character is what lets a single token straddle a
  step boundary: `, "b": ` legitimately ends the value of `a` and opens `b`.
* `advance(text)` — the same walk, on the real cursor.

### Per-type rules

* **Strings** are validated with a real JSON string scanner: an escape must be
  one of `\" \\ \/ \b \f \n \r \t` or a complete `\uXXXX`, raw control
  characters are refused, and only an *unescaped* quote closes the value. This
  is what allows a regex argument such as `"\\d+"` to be produced without ever
  risking a malformed string.
* **Numbers** follow the JSON number grammar, not "digits and dots": no
  leading zeros (`01`), no bare leading dot (`.5`), no trailing dot (`1.`).
  All three parse fine in Python and none of them is valid JSON.
* **Integers** are numbers without a fractional part.
* **Booleans** may only ever spell `true` or `false`.
* Numbers and strings also carry a **length cap**. Digits and string content
  are always *locally* legal, so a model that kept picking them would never
  close the document; once the cap is reached only the closing token is
  accepted. This is what makes termination a guarantee rather than a hope.
  The cap has to leave room for what a value still *owes*: a trailing `1.`
  owes a digit and a dangling `\` owes the rest of its escape, so both are
  refused one character early rather than stranding the decoder with a value
  it can neither extend nor finish.

### The decoding loop

For each position, `GenerationLoop`:

1. **Emits everything that is already determined, in one piece.** The grammar
   returns the whole run of settled text (`forced_prefix`) — consecutive
   literal steps *plus* the opening quote of a string value — for example
   `", "parameters": {"name": "`. It has exactly one legal form, so asking a
   neural network about it is pure waste, and encoding it as one string keeps
   the tokenizer's natural boundaries. Roughly two thirds of the characters in
   the output cost nothing at all.
2. **Ranks a narrowed candidate pool** at real decision points. The grammar
   reports which characters could legally start the next token
   (`possible_next_first_chars`), and `VocabMap` keeps tokens pre-grouped by
   first character, so ranking usually happens over a few thousand tokens
   instead of 151k. Inside a string value there is no narrowing: the closing
   quote comes packed into tokens like `",` and `"}}`, and excluding those was
   a bug worth its own paragraph below.
3. **Falls back to the full vocabulary** if nothing in the narrowed pool was
   accepted. The narrowing is an optimisation; it is never allowed to be the
   reason a valid token is missed.
4. Walks the pool in descending logit order and takes the first token the
   grammar accepts — which is exactly "mask the invalid tokens to minus
   infinity, then take the argmax".

The prompt still matters, but only for *content*: which function, and which
values. It is rendered with Qwen3's `<|im_start|>` chat template (an
instruction-tuned model behaves noticeably worse when fed raw text) and lists
the functions as compact signatures rather than nested JSON schemas.

## Design decisions

**The grammar owns validity, the prompt owns meaning.** These are kept
strictly apart. The prompt cannot make the output invalid, and the grammar
cannot make it *correct* — it only rules out the impossible. That split is
also why the prompt could be rewritten freely while tuning accuracy, with no
risk of breaking the output format.

**Validation is a pure function.** `is_token_valid` runs on a copy of the
cursor. The alternative — advance, inspect, roll back — is where this kind of
code usually goes wrong, and it would have to be exercised thousands of times
per prompt.

**Filter the vocabulary once, at load time.** Qwen's `vocab.json` is byte-level
BPE: a leading space is `Ġ`, and every byte outside printable ASCII maps to a
character above U+00FF. None of those tokens can appear in our output, so they
are dropped when the vocabulary is loaded rather than re-examined at every
step. That removes a large share of the vocabulary permanently.

**Function names are not matched greedily.** If a definition file declares both
`fn_add` and `fn_add_numbers`, closing the name at `fn_add` would make the
longer one unreachable. The name step therefore only closes on its own when no
other declared name extends it; otherwise the closing quote decides.

**Errors are values, not crashes.** Every module raises its own exception type
(`ParserError`, `VocabMapError`, `OutputParserError`, `ResultWriterError`,
`FunctionCallerError`), and `main` turns them into a message and an exit code.
A prompt that fails does not abort the run: the remaining prompts are still
processed and the results file is still written.

**Steps are built from the schema, never hardcoded.** Nothing in the code
knows about `fn_add_numbers`; a different definition file simply produces a
different step list.

## Performance analysis

Measured on the provided input files (11 prompts, 5 functions), CPU only,
`Qwen/Qwen3-0.6B`:

| | |
| --- | --- |
| Valid JSON | 11/11 — structurally guaranteed, not merely observed |
| Schema compliance | 11/11 — argument names, order and types |
| Function selection | 11/11 correct |
| Argument extraction | 11/11 correct |
| Total runtime | ~20 s, against a 5 minute budget |

**Where the time goes.** The cost is entirely forward passes, and the SDK
exposes no key/value cache — every pass re-reads the whole context. Three
things keep the count down: determined text costs zero passes, the whole
structural run is emitted in one go, and ranking happens in numpy over a
narrowed pool rather than in a Python loop over 151k tokens.

The first working version took **4m13s** for the same 11 prompts. Emitting
each structural literal as its own step was most of that difference; merging
them into a single run cut the number of forward passes sharply, and — for
the reason described under *Challenges* — it also fixed most of the wrong
answers at the same time.

**Where errors would show up.** Never in the structure: no prompt, however
strange, can make the output unparseable or off-schema, because no invalid
token is ever selectable. What a 0.6B model can still get wrong is the
*meaning* of an argument — paraphrasing a value instead of copying it, or
putting the replacement text where a pattern belongs. Constrained decoding
cannot help there: `"'hello'"` and `"hello"` are both perfectly valid
strings, so nothing in the grammar can prefer one. That part lives in the
prompt, and it is what the wording and the worked examples in
`prompt_builder.py` are for.

## Challenges faced

**Believing that "valid JSON" was the easy half.** The first numeric rule
accepted anything matching `-?\d*\.?\d*`, which happily produces `.5` and
`1.` — neither is valid JSON, and both slip through unnoticed until something
tries to parse them. A fuzz test over the decoding loop, driven by *random*
logits, is what surfaced it: with random scores the decoder eventually tries
every legal path, including the ones a well-behaved model would never take.
The same test also caught unbounded numbers looping forever, which is why the
length caps exist.

**Tokens do not respect structure.** Token boundaries have nothing to do with
JSON boundaries: a single token can be `, "b": `, ending one value and opening
the next field. Validating tokens as atomic units fails on those; feeding them
character by character through the cursor is what handles them naturally.

**The same mismatch, from the other side — and it was expensive.** Two
symptoms that looked unrelated turned out to be one bug each, both about
token boundaries:

* Emitting each literal step separately produced answers like
  `{"name": "description of shrek"}`, while the *same prompt with no
  constraint at all* produced `{"name": "shrek"}` perfectly. The constraint
  was making the model worse, which should be impossible if the masking is
  right. It was: a tokenizer encodes `{"` as one token, so emitting `{` and
  then `"name` handed the model a sequence it had essentially never seen
  during training. Emitting the whole determined run — including the opening
  quote of a string value — in a single encode call fixed it.
* Values then still rambled on instead of ending: `"cat\\s+\\w+\\s+\\w+"` where
  `"cat"` was wanted. The candidate pool inside a string excluded any token
  with a quote before its last character — which is exactly `",` and `"}}`,
  the tokens a model actually reaches for to close a value. Left with only a
  lone `"`, which scores far lower, it kept writing. The pool inside a string
  is now the full vocabulary.

The lesson worth keeping: constrained decoding is not only about *what is
legal*. If the legal path is one the model has never walked, it will still be
legal and still be wrong.

**Speed.** Scanning 151k tokens in Python at every position was far too slow.
Grouping tokens by first character at load time and ranking with numpy, rather
than looping in Python, is what brought the run down.

**Prompting a 0.6B model.** The first version dumped the raw function schemas
into a plain-text prompt, and the model answered with placeholders such as
`"user_input_value"`, or echoed the schema back as an argument. Switching to
the model's own chat template and to compact signatures fixed most of it.

## Testing strategy

`make test` (or `uv run pytest`) runs the suite in `tests/`. Four angles:

1. **Grammar unit tests** — the happy path for each parameter type, and every
   rejection that matters: unknown function names, letters where a number
   belongs, `.5`, `01`, `1.`, a bare `-`, unescaped quotes, invalid escapes,
   raw control characters, and both length caps. Also that validation leaves
   no trace on the cursor, and that prefix-ambiguous names stay reachable.
2. **A JSON string scanner table** — parametrised over pending escapes,
   `\uXXXX` in every stage of completion, and trailing content.
3. **Fuzzing the decoding loop** — a fake model returns *random* logits over a
   synthetic vocabulary. Whatever it picks, the output still parses and still
   matches the schema of whichever function it landed on. If the structure
   survives random scores, it is the masking producing it, not the model. The
   same fake also asserts that structural text costs no forward passes.
4. **I/O error paths** — missing files, malformed JSON, a JSON object where an
   array is required, an empty function list, duplicate names, unsupported
   parameter types, prompts without a `prompt` key, and an unwritable
   destination.

The real model is deliberately not part of the suite: it would make the tests
slow and non-deterministic. It is exercised by running the program.

## Example usage

```console
$ uv run python -m src
[1/11] fn_add_numbers {'a': 2.0, 'b': 3.0}
[2/11] fn_add_numbers {'a': 265.0, 'b': 345.0}
[3/11] fn_greet {'name': 'shrek'}
[4/11] fn_greet {'name': 'john'}
[5/11] fn_reverse_string {'s': 'hello'}
[6/11] fn_reverse_string {'s': 'world'}
[7/11] fn_get_square_root {'a': 16.0}
[8/11] fn_get_square_root {'a': 144.0}
[9/11] fn_substitute_string_with_regex {'source_string': "Hello 34 I'm 233 years old", 'regex': '\\d+', 'replacement': 'NUMBERS'}
[10/11] fn_substitute_string_with_regex {'source_string': 'Programming is fun', 'regex': 'a|e|i|o|u', 'replacement': '*'}
[11/11] fn_substitute_string_with_regex {'source_string': 'The cat sat on the mat with another cat', 'regex': 'cat', 'replacement': 'dog'}

Wrote 11/11 function calls to data/output/function_calling_results.json
Total time: 0m 19s
```

Excerpt of the resulting `data/output/function_calling_results.json`:

```json
[
  {
    "prompt": "Question: What is the sum of 2 and 3?",
    "name": "fn_add_numbers",
    "parameters": {
      "a": 2.0,
      "b": 3.0
    }
  },
  {
    "prompt": "Reverse the string 'hello'",
    "name": "fn_reverse_string",
    "parameters": {
      "s": "hello"
    }
  }
]
```

Errors are reported, never raised:

```console
$ uv run python -m src --input data/input/missing.json
Error: Input file not found: data/input/missing.json

$ uv run python -m src --functions_definition README.md
Error: README.md: invalid JSON: Expecting value: line 1 column 1 (char 0)
```

## Resources

Documentation and articles used:

* [JSON specification (RFC 8259)](https://www.rfc-editor.org/rfc/rfc8259) —
  the number and string grammars implemented in `schema_grammar.py`.
* [Efficient Guided Generation for Large Language Models](https://arxiv.org/abs/2307.09702)
  — Willard & Louf, the paper behind `outlines`; the finite-state view of
  constrained decoding.
* [Hugging Face: text generation strategies](https://huggingface.co/docs/transformers/generation_strategies)
  — how logits, logit processors and token selection fit together.
* [Qwen3 documentation](https://qwenlm.github.io/blog/qwen3/) — the chat
  template and the non-thinking mode used in the prompt.
* [Byte-level BPE](https://huggingface.co/learn/nlp-course/chapter6/5) — why
  `vocab.json` is full of `Ġ` and `Ċ`.
* [Pydantic documentation](https://docs.pydantic.dev/) — model validation.
* [PEP 257](https://peps.python.org/pep-0257/) — docstring conventions.

### Use of AI

AI was used as a reviewer and as a rubber duck, not as an author:

* **Understanding the topic.** Working through what constrained decoding does
  to logits, and why a 0.6B model needs it, before writing anything.
* **Reviewing the grammar.** Asking for edge cases against the JSON number and
  string rules is what exposed that `.5` and `1.` were being accepted, and
  that a token may span two grammar steps.
* **Prompt iteration.** Comparing phrasings of the system prompt, and
  confirming the exact shape of Qwen3's chat template.
* **Test design.** The idea of fuzzing the loop with random logits — proving
  the structure comes from the masking rather than from the model — came out
  of that discussion.

Everything in `src/` was reviewed line by line and is understood well enough
to be defended, modified and explained on the spot.