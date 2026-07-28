NAME		= push_swap

CC			= cc
CFLAGS		= -Wall -Wextra -Werror
RM			= rm -f

INC_DIR		= include
SRCS_DIR	= .
UTILS_DIR	= utils

SRCS		= push_swap.c \
			  utils/push_swap_index.c \
			  utils/push_swap_radix_sort.c \
			  utils/push_swap_instructions.c \
			  utils/push_swap_sort_cases.c \
			  utils/push_swap_util_main.c \
			  utils/push_swap_utils.c

OBJS		= $(SRCS:.c=.o)

HEADER		= $(INC_DIR)/push_swap.h

all: $(NAME)

$(NAME): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -I$(INC_DIR) -o $(NAME)

%.o: %.c $(HEADER)
	$(CC) $(CFLAGS) -I$(INC_DIR) -c $< -o $@

clean:
	$(RM) $(OBJS)

fclean: clean
	$(RM) $(NAME)

re: fclean all

.PHONY: all clean fclean re
