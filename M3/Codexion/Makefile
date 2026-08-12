# Compilador e flags
CC = cc
CFLAGS = -Wall -Wextra -Werror -pthread -I.
LDFLAGS = -lm

# Diretórios
SRC_DIR = .
LIB_DIR = lib
OBJ_DIR = obj
BIN_DIR = .

# Arquivos fonte
SRCS = $(SRC_DIR)/main.c
LIB_SRCS = $(LIB_DIR)/coder.c \
           $(LIB_DIR)/dongle.c \
           $(LIB_DIR)/init.c \
           $(LIB_DIR)/log.c \
           $(LIB_DIR)/monitor.c \
           $(LIB_DIR)/priority_queue.c \
		   $(LIB_DIR)/pq_utils.c \
		   $(LIB_DIR)/coder_utils.c \
		   $(LIB_DIR)/time_utils.c \
           $(LIB_DIR)/utils.c

# Objetos
OBJS = $(SRCS:$(SRC_DIR)/%.c=$(OBJ_DIR)/%.o)
LIB_OBJS = $(LIB_SRCS:$(LIB_DIR)/%.c=$(OBJ_DIR)/%.o)

# Executável
TARGET = $(BIN_DIR)/codexion

GREEN = \033[0;32m
RED = \033[0;31m
NC = \033[0m

# Regra padrão
all: $(TARGET)

# Linkagem
$(TARGET): $(OBJ_DIR) $(OBJS) $(LIB_OBJS)
	@echo "$(GREEN)Linking...$(NC)"
	$(CC) $(CFLAGS) $(OBJS) $(LIB_OBJS) -o $@ $(LDFLAGS)
	@echo "$(GREEN)✅ Build successful!$(NC)"
	@echo "$(GREEN)Executable: $(TARGET)$(NC)"

# Compilação dos objetos principais
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c $(SRC_DIR)/libcodexion.h
	@mkdir -p $(OBJ_DIR)
	@echo "$(GREEN)Compiling $<...$(NC)"
	$(CC) $(CFLAGS) -c $< -o $@

# Compilação dos objetos da lib
$(OBJ_DIR)/%.o: $(LIB_DIR)/%.c $(SRC_DIR)/libcodexion.h
	@mkdir -p $(OBJ_DIR)
	@echo "$(GREEN)Compiling $<...$(NC)"
	$(CC) $(CFLAGS) -c $< -o $@

# Criar diretório de objetos
$(OBJ_DIR):
	@mkdir -p $(OBJ_DIR)

# Limpeza
clean:
	@echo "$(RED)Cleaning object files...$(NC)"
	rm -rf $(OBJ_DIR)
	@echo "$(GREEN)✅ Clean complete!$(NC)"

fclean: clean
	@echo "$(RED)Removing executable...$(NC)"
	rm -f $(TARGET)
	@echo "$(GREEN)✅ Full clean complete!$(NC)"

re: fclean all

# Regras de teste (com exemplos)
test: $(TARGET)
	@echo "$(GREEN)Running tests...$(NC)"
	@echo "\n=== Test 1: FIFO scheduler ==="
	./$(TARGET) 5 3000 200 200 200 10 400 fifo
	@echo "\n=== Test 2: EDF scheduler ==="
	./$(TARGET) 5 3000 200 200 200 10 400 fifo
	@echo "\n=== Test 3: Invalid arguments (should fail) ==="
	./$(TARGET) 5 10 20 || true
	@echo "\n=== Test 4: Invalid scheduler (should fail) ==="
	./$(TARGET) 5 10 20 15 30 3 5 roundrobin || true

# Debug build
debug: CFLAGS += -g -DDEBUG
debug: re

# Valgrind build (para memória)
valgrind: $(TARGET)
valgrind:
	valgrind --tool=memcheck \
		--leak-check=full \
		--show-leak-kinds=all \
		--track-origins=yes \
		--error-exitcode=1 \
		$(TARGET) 3 20 5 5 5 1 1 fifo
# Help
help:
	@echo "Available targets:"
	@echo "  all       - Build the program (default)"
	@echo "  clean     - Remove object files"
	@echo "  fclean    - Remove object files and executable"
	@echo "  re        - Rebuild everything"
	@echo "  test      - Run test cases"
	@echo "  debug     - Build with debug symbols"
	@echo "  valgrind  - Run with valgrind memory checker"
	@echo "  help      - Show this help"

.PHONY: all clean fclean re test debug valgrind help
