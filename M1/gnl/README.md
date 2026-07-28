*This project has been created as part of the 42 curriculum by mafonso.*

# get_next_line

## Description

The **get_next_line** project aims to implement a C function capable of reading a file descriptor line by line, returning one line per function call.  
The main challenge of this project is handling buffered input correctly, managing memory safely, and supporting arbitrary buffer sizes while preserving unread data between calls.

This function is particularly useful when processing large files or streams, as it avoids loading the entire content into memory at once.

The project strengthens understanding of:
- File descriptors and the `read()` system call
- Static variables
- Memory allocation and management
- String manipulation
- Edge case handling (EOF, newlines, invalid FDs)

---

## Instructions

### Compilation

Compile your project using `gcc` with the required flags:

```bash
gcc -Wall -Wextra -Werror get_next_line.c get_next_line_utils.c
````

To test with a custom `BUFFER_SIZE`:

```bash
gcc -Wall -Wextra -Werror -D BUFFER_SIZE=42 get_next_line.c get_next_line_utils.c
```

### Usage Example

```c
#include "get_next_line.h"
#include <fcntl.h>
#include <stdio.h>

int main(void)
{
    int fd = open("example.txt", O_RDONLY);
    char *line;

    while ((line = get_next_line(fd)))
    {
        printf("%s", line);
        free(line);
    }
    close(fd);
    return 0;
}
```

---

## Algorithm Explanation and Justification

### High-Level Overview

The algorithm is based on **incremental reading** using a fixed-size buffer and a **static accumulator** to store leftover data between function calls.

Each call to `get_next_line()`:

1. Reads from the file descriptor into a temporary buffer.
2. Appends the read content to an accumulator string.
3. Searches for a newline character (`'\n'`).
4. If found, extracts and returns the line up to the newline.
5. Stores the remaining content for the next call.
6. If EOF is reached, returns the remaining data (if any).

---

### Key Design Choices

#### 1. Static Accumulator

A `static char *` is used to persist unread data between calls.
This is required because `get_next_line()` must remember partial reads without relying on global variables.

#### 2. Buffered Reading

The `read()` system call reads `BUFFER_SIZE` bytes at a time.
This ensures efficiency and compliance with the project constraints.

#### 3. Line Extraction

When a newline is detected:

* Memory is allocated for the line to be returned.
* The accumulator is updated to keep only the remaining data.

This guarantees that:

* Each call returns exactly one line
* No data is lost or duplicated

#### 4. Memory Safety

All allocations are checked for failure.
Allocated memory is freed appropriately to prevent leaks.
The function returns `NULL` only when no more data is available or on error.

---

### Why This Algorithm?

* **Efficiency:** Avoids unnecessary reads and memory allocations.
* **Scalability:** Works with any `BUFFER_SIZE`.
* **Correctness:** Handles edge cases such as:

  * Files without a trailing newline
  * Very small or very large buffers
  * Empty files
* **Compliance:** Fully respects the project rules (no forbidden functions, no global variables).

---

## Resources

### Technical References

* `man read`
* `man open`
* `man close`
* GNU C Library Documentation
* The Linux Programming Interface — Michael Kerrisk

### Tutorials & Articles

* File descriptors and buffering in Unix systems
* Memory management in C
* Static variables in C

### AI Usage Disclosure

AI tools were used **only as a learning and support aid**, specifically for:

* Clarifying how `read()` behaves with different buffer sizes
* Reviewing algorithm logic and edge cases
* Improving code readability and documentation quality

All code logic, structure, and implementation decisions were fully understood and manually written by the author.
