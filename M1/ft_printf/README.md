*Th*This project has been created as part of the 42 curriculum by mafonso.*

# ft_printf

## Description

The **ft_printf** project consists of recreating the standard C library function
`printf`.  
The goal is to understand how formatted output works internally, including
parsing, variadic functions, and low-level writing to standard output.

This project focuses on:
- Handling **variadic arguments** using `<stdarg.h>`
- Parsing a format string character by character
- Implementing multiple format specifiers
- Returning the exact number of characters printed, just like the original `printf`

The result is a reusable static library (`libftprintf.a`) that provides a custom
implementation of `printf` called `ft_printf`.

---

## Instructions

### Compilation

To compile the library, simply run:

```bash
make
````

This will generate the static library:

```text
libftprintf.a
```

To clean object files:

```bash
make clean
```

To clean everything (objects + library):

```bash
make fclean
```

To recompile from scratch:

```bash
make re
```

---

### Usage

Include the header in your project:

```c
#include "ft_printf.h"
```

Compile your program linking the library:

```bash
gcc main.c libftprintf.a
```

Example usage:

```c
ft_printf("Hello %s, value = %d\n", "world", 42);
```

---

## Supported Format Specifiers

The `ft_printf` function supports the following conversions:

| Specifier | Description                             |
| --------- | --------------------------------------- |
| `%c`      | Print a single character                |
| `%s`      | Print a string                          |
| `%d`      | Print a signed decimal integer          |
| `%i`      | Print a signed decimal integer          |
| `%u`      | Print an unsigned decimal integer       |
| `%x`      | Print a number in lowercase hexadecimal |
| `%X`      | Print a number in uppercase hexadecimal |
| `%p`      | Print a pointer address in hexadecimal  |
| `%%`      | Print a literal `%` character           |

---

## Library Description

This project produces a static library containing the following core functions:

### Main function

* `int ft_printf(const char *format, ...);`
  Parses the format string, processes variadic arguments, writes output to
  standard output, and returns the number of characters printed.

### Helper functions (examples)

* `ft_handle_print` — dispatches format specifiers
* `ft_putchar` — writes a single character
* `ft_putstr` — writes a string
* `ft_putnbr` — writes a signed integer
* `ft_putnbr_uns` — writes an unsigned integer
* `ft_puthex` — writes hexadecimal values
* `ft_putptr` — writes pointer addresses

All output is performed using the `write` system call, as required by the project.

---

## Technical Choices

* Variadic arguments are handled using `va_list`, `va_start`, `va_arg`, and `va_end`
* Recursive implementations are used for number printing
* Pointer values are converted internally to `unsigned long` for hexadecimal output
* All helper functions return the number of characters printed to ensure accurate
  return values from `ft_printf`

---

## Resources

### Documentation & References

* `man 3 printf`
* `man 3 stdarg`
* GNU C Library Documentation
* cppreference.com — printf and variadic functions
* 42 intra documentation

### AI Usage

AI tools were used during the development of this project for:

* Clarifying the behavior of variadic functions
* Understanding edge cases related to `%p` formatting
* Reviewing logic and identifying bugs
* Improving code structure and readability

All code was written, tested, and validated by the student, with AI used strictly
as a learning and debugging assistant.

---is project has been created as part of the 42 curriculum by mafonso.*

# ft_printf

## Description

The **ft_printf** project consists of recreating the standard C library function
`printf`.  
The goal is to understand how formatted output works internally, including
parsing, variadic functions, and low-level writing to standard output.

This project focuses on:
- Handling **variadic arguments** using `<stdarg.h>`
- Parsing a format string character by character
- Implementing multiple format specifiers
- Returning the exact number of characters printed, just like the original `printf`

The result is a reusable static library (`libftprintf.a`) that provides a custom
implementation of `printf` called `ft_printf`.

---

## Instructions

### Compilation

To compile the library, simply run:

```bash
make
````

This will generate the static library:

```text
libftprintf.a
```

To clean object files:

```bash
make clean
```

To clean everything (objects + library):

```bash
make fclean
```

To recompile from scratch:

```bash
make re
```

---

### Usage

Include the header in your project:

```c
#include "ft_printf.h"
```

Compile your program linking the library:

```bash
gcc main.c libftprintf.a
```

Example usage:

```c
ft_printf("Hello %s, value = %d\n", "world", 42);
```

---

## Supported Format Specifiers

The `ft_printf` function supports the following conversions:

| Specifier | Description                             |
| --------- | --------------------------------------- |
| `%c`      | Print a single character                |
| `%s`      | Print a string                          |
| `%d`      | Print a signed decimal integer          |
| `%i`      | Print a signed decimal integer          |
| `%u`      | Print an unsigned decimal integer       |
| `%x`      | Print a number in lowercase hexadecimal |
| `%X`      | Print a number in uppercase hexadecimal |
| `%p`      | Print a pointer address in hexadecimal  |
| `%%`      | Print a literal `%` character           |

---

## Library Description

This project produces a static library containing the following core functions:

### Main function

* `int ft_printf(const char *format, ...);`
  Parses the format string, processes variadic arguments, writes output to
  standard output, and returns the number of characters printed.

### Helper functions (examples)

* `ft_handle_print` — dispatches format specifiers
* `ft_putchar` — writes a single character
* `ft_putstr` — writes a string
* `ft_putnbr` — writes a signed integer
* `ft_putnbr_uns` — writes an unsigned integer
* `ft_puthex` — writes hexadecimal values
* `ft_putptr` — writes pointer addresses

All output is performed using the `write` system call, as required by the project.

---

## Technical Choices

* Variadic arguments are handled using `va_list`, `va_start`, `va_arg`, and `va_end`
* Recursive implementations are used for number printing
* Pointer values are converted internally to `unsigned long` for hexadecimal output
* All helper functions return the number of characters printed to ensure accurate
  return values from `ft_printf`

---

## Resources

### Documentation & References

* `man 3 printf`
* `man 3 stdarg`
* GNU C Library Documentation
* cppreference.com — printf and variadic functions
* 42 intra documentation

### AI Usage

AI tools were used during the development of this project for:

* Clarifying the behavior of variadic functions
* Understanding edge cases related to `%p` formatting
* Reviewing logic and identifying bugs
* Improving code structure and readability

All code was written, tested, and validated by the student, with AI used strictly
as a learning and debugging assistant.

---
