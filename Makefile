PYTHON := python
POETRY := poetry
APP := src.main:app
UVICORN := uvicorn

.PHONY: install format lint test typecheck run dev clean

install:
	$(POETRY) install --no-root

format:
	$(POETRY) run black .

lint:
	$(POETRY) run flake8 ai_agent_system/src

typecheck:
	$(POETRY) run mypy --strict ai_agent_system/src

test:
	$(POETRY) run pytest -q --disable-warnings --maxfail=1 --cov=ai_agent_system/src --cov-report=term-missing ai_agent_system/src/tests

run:
	$(POETRY) run $(UVICORN) $(APP) --reload --host 0.0.0.0 --port 8000

dev:
	$(POETRY) run $(UVICORN) $(APP) --reload --host 0.0.0.0 --port 8000

clean:
	rm -rf .mypy_cache .pytest_cache htmlcov
