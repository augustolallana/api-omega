format:
	uv run ruff format src
	uv run isort src
dev:
	uv run uvicorn src.main:app --reload
prod:
	uv run uvicorn src.main:app