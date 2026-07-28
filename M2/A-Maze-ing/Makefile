VENV    := .venv
PY      := $(VENV)/bin/python
PIP     := $(VENV)/bin/pip
CONFIG  := config.txt

MLX_SRC := mlx-2.2-py3-ubuntu-any.whl
MLX_PIP := build/mlx-2.2-py3-none-any.whl

MYPY_FLAGS := --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

.PHONY: install run debug clean lint lint-strict package test

install:
	python3 -m venv $(VENV)
	$(PIP) install --quiet --upgrade pip
	$(PIP) install --quiet build flake8 mypy pytest
	mkdir -p build
	cp $(MLX_SRC) $(MLX_PIP)
	$(PIP) install --quiet $(MLX_PIP)
	$(MAKE) package
	$(PIP) install --quiet --force-reinstall --no-deps \
		mazegen-1.0.0-py3-none-any.whl

package:
	$(PY) -m build --outdir dist
	cp dist/mazegen-1.0.0-py3-none-any.whl .
	cp dist/mazegen-1.0.0.tar.gz .

run:
	$(PY) a_maze_ing.py $(CONFIG)

debug:
	$(PY) -m pdb a_maze_ing.py $(CONFIG)

lint:
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . $(MYPY_FLAGS)

lint-strict:
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . --strict

test:
	$(VENV)/bin/pytest -q

clean:
	rm -rf build dist *.egg-info mazegen.egg-info
	rm -rf .mypy_cache
	find . -name __pycache__ -type d -not -path './.venv/*' \
		-exec rm -rf {} +
