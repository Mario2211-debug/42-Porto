# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mafonso <mafonso@student.42porto.com>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/12/03 02:07:53 by mafonso           #+#    #+#              #
#    Updated: 2025/12/10 15:22:17 by mafonso          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

SRCS = ft_printf.c \
       ft_handle_print.c \
       ft_putchar.c \
       ft_putstr.c \
       ft_putnbr.c \
       ft_puthex.c \
       ft_putnbr_unsigned.c \
       ft_putptr.c

OBJS = $(SRCS:.C=.O)
NAME= libftprintf.a

OBJS = $(SRCS:.c=.o)

# Flags de compilação
CC = gcc
CFLAGS = -Wall -Wextra -Werror

# Regra padrão: compila a lib
$(NAME): $(OBJS)
	ar rcs $(NAME) $(OBJS)

all: $(NAME)

%.o: %.c ft_printf.h
	$(CC) $() -c $< -o $@

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
