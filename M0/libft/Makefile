# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mafonso <mafonso@student.42porto.com>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/10/16 21:46:00 by mafonso           #+#    #+#              #
#    Updated: 2025/11/11 19:56:46 by mafonso          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# **************************************************************************** #
#                                   LIBFT                                      #
# **************************************************************************** #

# Nome final da biblioteca (arquivo .a)
NAME = libft.a

# Compilador e flags
CC = cc
CFLAGS = -Wall -Wextra -Werror

# Pasta dos arquivos
SRC_DIR = .
OBJ_DIR = obj


SRC = ft_isalnum.c \
      ft_memcmp.c \
      ft_memset.c \
      ft_memcpy.c \
      ft_isalpha.c \
      ft_isdigit.c \
      ft_isascii.c \
      ft_strlen.c \
      ft_isprint.c \
      ft_toupper.c \
      ft_tolower.c \
      ft_strchr.c \
      ft_memmove.c \
      ft_strncmp.c \
      ft_strlcpy.c \
      ft_strlcat.c \
      ft_atoi.c \
      ft_bzero.c \
      ft_memchr.c \
      ft_putnbr_fd.c \
      ft_putchar_fd.c \
      ft_putstr_fd.c \
      ft_putendl_fd.c \
      ft_strrchr.c \
      ft_strdup.c \
      ft_substr.c \
      ft_strjoin.c \
      ft_strnstr.c \
      ft_strtrim.c \
      ft_striteri.c \
      ft_split.c \
      ft_calloc.c \
      ft_strmapi.c \
      ft_itoa.c \


# Gera lista dos objetos (.o) automaticamente
OBJ = $(SRC:%.c=$(OBJ_DIR)/%.o)

# **************************************************************************** #
#                                   REGRAS                                     #
# **************************************************************************** #

# Regra padrão (executada quando chamamos apenas 'make')
all: $(NAME)

# Regra para criar a biblioteca
$(NAME): $(OBJ)
	@ar rcs $(NAME) $(OBJ)
	@echo "✅ Biblioteca criada: $(NAME)"

# Compila cada arquivo .c em .o (guardado dentro de /obj)
$(OBJ_DIR)/%.o: %.c | $(OBJ_DIR)
	@$(CC) $(CFLAGS) -c $< -o $@
	@echo "🧱 Compilado: $<"

# Cria o diretório /obj se não existir
$(OBJ_DIR):
	@mkdir -p $(OBJ_DIR)

# Limpa apenas os objetos
clean:
	@rm -rf $(OBJ_DIR)
	@echo "🧹 Objetos removidos!"

# Limpa tudo (objetos + biblioteca)
fclean: clean
	@rm -f $(NAME)
	@echo "🧽 Biblioteca removida!"

# Recompila tudo do zero
re: fclean all

# Marca as regras que não criam ficheiros (boas práticas)
.PHONY: all clean fclean re
