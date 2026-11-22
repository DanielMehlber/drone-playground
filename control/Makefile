.PHONY: help lock upgrade sync format lint typecheck check run notebook

help:
	@echo "lock       regenerate requirements/*.txt from pyproject.toml"
	@echo "upgrade    lock with the newest versions allowed"
	@echo "sync       make the venv match requirements/dev.txt"
	@echo "format     ruff format and autofix"
	@echo "lint       ruff check and format check"
	@echo "typecheck  mypy --strict"
	@echo "check      lint, typecheck"
	@echo "run        start the controller node"
	@echo "notebook   JupyterLab on port 8888"

lock:
	pip-compile --output-file=requirements/base.txt pyproject.toml
	pip-compile --extra=dev --output-file=requirements/dev.txt pyproject.toml

upgrade:
	pip-compile --upgrade --output-file=requirements/base.txt pyproject.toml
	pip-compile --upgrade --extra=dev --output-file=requirements/dev.txt pyproject.toml

sync:
	pip-sync requirements/dev.txt
	pip install --no-deps --editable .

format:
	ruff format .
	ruff check --fix .

lint:
	ruff check .
	ruff format --check .

typecheck:
	mypy

check: lint typecheck

run:
	drone-control

notebook:
	jupyter lab --ip=0.0.0.0 --port=8888 --no-browser \
		--ServerApp.token='' --ServerApp.password='' \
		--notebook-dir=notebooks
