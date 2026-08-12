# Variables
VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
MYPY := $(VENV)/bin/mypy
FLAKE8 := $(VENV)/bin/flake8

# Default map file (can be overridden)
MAP ?= maps/easy/01_linear_path.txt

.PHONY: install run debug clean lint lint-strict help

# ============ Installation ============
install:
	@echo "🔧 Creating virtual environment..."
	python3 -m venv $(VENV)
	@echo "📦 Installing dependencies..."
	$(PIP) install --quiet -r requirements.txt
	@echo "✅ Installation complete!"
	@echo "   To activate: source $(VENV)/bin/activate"

# ============ Execution ============
run:
	@echo "🚀 Running simulation with $(MAP)..."
	$(PY) app.py $(MAP)

# Run with visualization (pygame)
visualize:
	@echo "🎮 Launching visualization with $(MAP)..."
	$(PY) app.py $(MAP) --visualize

# Run with no summary (terminal only)
run-nosummary:
	@echo "📊 Running simulation without summary..."
	$(PY) app.py $(MAP) --no-summary

# ============ Debug ============
debug:
	@echo "🐛 Debugging with pdb..."
	$(PY) -m pdb app.py $(MAP)

# ============ Linting ============
lint:
	@echo "🔍 Running flake8..."
	$(FLAKE8) . --exclude=.venv,.mypy_cache
	@echo "🔍 Running mypy..."
	$(MYPY) . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs
	@echo "✅ Lint passed!"

# Strict linting (optional)
lint-strict:
	@echo "🔍 Running flake8 (strict)..."
	$(FLAKE8) . --exclude=.venv,.mypy_cache
	@echo "🔍 Running mypy (strict)..."
	$(MYPY) . --strict
	@echo "✅ Strict lint passed!"

# ============ Testing ============
test:
	@echo "🧪 Running tests..."
	$(PY) -m pytest tests/ -v --tb=short

test-coverage:
	@echo "📊 Running tests with coverage..."
	$(PY) -m pytest tests/ --cov=. --cov-report=html --cov-report=term

# ============ Cleanup ============
clean:
	@echo "🧹 Cleaning up..."
	rm -rf $(VENV)
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name ".DS_Store" -delete 2>/dev/null || true
	@echo "✅ Clean complete!"

# ============ Run all benchmarks ============
benchmark:
	@echo "📊 Running all benchmark maps..."
	@echo "--- Easy Maps ---"
	@echo "01_linear_path:"
	@$(PY) app.py maps/easy/01_linear_path.txt --no-summary
	@echo ""
	@echo "02_simple_fork:"
	@$(PY) app.py maps/easy/02_simple_fork.txt --no-summary
	@echo ""
	@echo "03_basic_capacity:"
	@$(PY) app.py maps/easy/03_basic_capacity.txt --no-summary
	@echo ""
	@echo "--- Medium Maps ---"
	@echo "01_dead_end_trap:"
	@$(PY) app.py maps/medium/01_dead_end_trap.txt --no-summary
	@echo ""
	@echo "02_circular_loop:"
	@$(PY) app.py maps/medium/02_circular_loop.txt --no-summary
	@echo ""
	@echo "03_priority_puzzle:"
	@$(PY) app.py maps/medium/03_priority_puzzle.txt --no-summary
	@echo ""
	@echo "--- Hard Maps ---"
	@echo "01_maze_nightmare:"
	@$(PY) app.py maps/hard/01_maze_nightmare.txt --no-summary
	@echo ""
	@echo "02_capacity_hell:"
	@$(PY) app.py maps/hard/02_capacity_hell.txt --no-summary
	@echo ""
	@echo "03_ultimate_challenge:"
	@$(PY) app.py maps/hard/03_ultimate_challenge.txt --no-summary

# =============== Error =================
errors:
	@echo "❌ Running invalid map tests..."
	@echo ""

	@echo "01_missing_start:"
	-@$(PY) app.py maps/errors/01_missing_start.txt --no-summary
	@echo ""

	@echo "02_missing_end:"
	-@$(PY) app.py maps/errors/02_missing_end.txt --no-summary
	@echo ""

	@echo "03_duplicate_zone:"
	-@$(PY) app.py maps/errors/03_duplicate_zone.txt --no-summary
	@echo ""

	@echo "04_duplicate_coordinates:"
	-@$(PY) app.py maps/errors/04_duplicate_coordinates.txt --no-summary
	@echo ""

	@echo "05_unknown_zone_connection:"
	-@$(PY) app.py maps/errors/05_unknown_zone_connection.txt --no-summary
	@echo ""

	@echo "06_self_connection:"
	-@$(PY) app.py maps/errors/06_self_connection.txt --no-summary
	@echo ""

	@echo "07_invalid_capacity:"
	-@$(PY) app.py maps/errors/07_invalid_capacity.txt --no-summary
	@echo ""

	@echo "08_invalid_zone_type:"
	-@$(PY) app.py maps/errors/08_invalid_zone_type.txt --no-summary
	@echo ""

	@echo "09_negative_coordinates:"
	-@$(PY) app.py maps/errors/09_negative_coordinates.txt --no-summary
	@echo ""

	@echo "10_disconnected_graph:"
	-@$(PY) app.py maps/errors/10_disconnected_graph.txt --no-summary
	@echo ""

	@echo "11_no_path:"
	-@$(PY) app.py maps/errors/11_no_path.txt --no-summary
	@echo ""

	@echo "12_two_starts:"
	-@$(PY) app.py maps/errors/12_two_starts.txt --no-summary
	@echo ""

	@echo "13_two_ends:"
	-@$(PY) app.py maps/errors/13_two_ends.txt --no-summary
	@echo ""

	@echo "14_invalid_drone_count:"
	-@$(PY) app.py maps/errors/14_invalid_drone_count.txt --no-summary
	@echo ""

	@echo "15_empty_file:"
	-@$(PY) app.py maps/errors/15_empty_file.txt --no-summary
# ============ Help ============
help:
	@echo "╔══════════════════════════════════════════════════════════╗"
	@echo "║              Fly-In Drone Simulator                     ║"
	@echo "╚══════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "📌 Basic Commands:"
	@echo "  make install         - Create virtualenv and install dependencies"
	@echo "  make run             - Run simulation (default map)"
	@echo "  make visualize       - Run with Pygame visualization"
	@echo "  make debug           - Run with Python debugger (pdb)"
	@echo "  make clean           - Remove virtualenv and cache files"
	@echo ""
	@echo "📌 Linting:"
	@echo "  make lint            - Run flake8 and mypy (standard)"
	@echo "  make lint-strict     - Run flake8 and mypy (strict)"
	@echo ""
	@echo "📌 Testing:"
	@echo "  make test            - Run unit tests with pytest"
	@echo "  make test-coverage   - Run tests with coverage report"
	@echo ""
	@echo "📌 Custom Map:"
	@echo "  make run MAP=path/to/map.txt"
	@echo "  make visualize MAP=path/to/map.txt"
	@echo ""
	@echo "📌 Benchmarks:"
	@echo "  make benchmark       - Run all benchmark maps"
	@echo ""
	@echo "📌 Examples:"
	@echo "  make run MAP=maps/medium/02_circular_loop.txt"
	@echo "  make visualize MAP=maps/hard/03_ultimate_challenge.txt"