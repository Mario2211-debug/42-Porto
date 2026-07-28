*This project has been created as part of the 42 curriculum by mafonso.*

# push_swap

## Description

`push_swap` is a sorting project from the 42 curriculum.  
The goal is to sort a stack of integers using a limited set of allowed operations and to output the smallest possible sequence of instructions.

This implementation uses:

- index compression, so each value is mapped to its sorted position
- dedicated sorting for very small inputs
- radix sort for larger inputs

The project focuses on algorithmic thinking, data structures, input validation, memory safety, and clean C code under strict coding rules.

## How it works

The program:

1. parses and validates all input arguments
2. rejects invalid numbers, duplicates, empty arguments, and integer overflows
3. stores the values in stack `A`
4. assigns an index to each node based on sorted order
5. applies:
   - `sort_2` for 2 numbers
   - `sort_3` for 3 numbers
   - `sort_5` for up to 5 numbers
   - `radix_sort` for larger inputs
6. prints the operations required to sort the stack

Allowed operations include:

- `sa`, `sb`, `ss`
- `pa`, `pb`
- `ra`, `rb`, `rr`
- `rra`, `rrb`, `rrr`

## Instructions

### Compilation

```bash
make
````

### Recompilation

```bash
make re
```

### Cleanup

```bash
make clean
make fclean
```

### Execution

```bash
./push_swap 3 2 1
```

Example output:

```bash
sa
rra
```

You can also test random inputs:

```bash
./push_swap $(shuf -i 1-100 -n 100)
```

To count the number of operations:

```bash
./push_swap $(shuf -i 1-100 -n 100) | wc -l
```

## Validation examples

Valid input:

```bash
./push_swap 3 2 1
./push_swap +42 -42
./push_swap 10 -5 3 -2 0
```

Invalid input:

```bash
./push_swap ""
./push_swap " "
./push_swap 1 2 a
./push_swap 1 2 2
./push_swap 2147483648
./push_swap -2147483649
./push_swap 03 3
```

All invalid cases must print:

```bash
Error
```

## Technical choices

### Data structure

The project uses a linked list to represent each stack.

Each node stores:

* the original value
* its sorted index
* a pointer to the next node

### Sorting strategy

For small inputs, dedicated case-based sorting is more efficient than radix.

For larger inputs, radix sort is used because it is simple, deterministic, and reliable once indexing is done correctly.

### Parsing

The parser checks:

* empty arguments
* invalid characters
* malformed signs
* integer overflow / underflow
* duplicate numeric values

### Memory management

All allocated memory is freed before exit, including error paths.

Valgrind was used to verify that:

* no leaks remain
* no invalid reads/writes occur
* no uninitialized memory is used

## Project structure

Example structure:

```text
.
├── Makefile
├── README.md
├── include
│   └── push_swap.h
├── push_swap.c
├── push_swap_index.c
├── push_swap_instructions.c
├── push_swap_radix_sort.c
├── push_swap_sort_cases.c
├── push_swap_util_main.c
└── push_swap_utils.c
```

Adjust this section if your actual repository layout differs.

## Testing

Basic tests:

```bash
./push_swap 1
./push_swap 1 2
./push_swap 2 1
./push_swap 3 2 1
./push_swap 5 4 3 2 1
```

Performance tests:

```bash
./push_swap $(shuf -i 1-100 -n 100) | wc -l
./push_swap $(shuf -i 1-500 -n 500) | wc -l
```

Valgrind tests:

```bash
valgrind --track-origins=yes --leak-check=full --show-leak-kinds=all ./push_swap 3 2 1
valgrind --track-origins=yes --leak-check=full --show-leak-kinds=all ./push_swap ""
valgrind --track-origins=yes --leak-check=full --show-leak-kinds=all ./push_swap 1 2 a
valgrind --track-origins=yes --leak-check=full --show-leak-kinds=all ./push_swap 1 2 2
```

## Resources

Classic references related to the topic:

* The 42 push_swap subject
* Linux manual pages:

  * `write(2)`
  * `malloc(3)`
  * `free(3)`
* Valgrind documentation
* General references on:

  * linked lists
  * radix sort
  * stack-based sorting

## AI usage

AI was used as a support tool during development, mainly for:

* understanding and comparing sorting strategies
* reviewing algorithm logic
* identifying parsing and indexing issues
* improving edge-case handling
* suggesting test cases
* reviewing memory management and Valgrind output
* helping reorganize functions to satisfy Norminette constraints

AI was not used as a substitute for implementation, debugging, or final verification.
All final integration, adaptation, testing, and validation were done manually in the project codebase.

## Notes

This project is not only about sorting correctly.
It is also about:

* producing a valid sequence of allowed operations
* handling invalid input safely
* writing clean and maintainable C
* respecting 42 project constraints
* managing memory properly
