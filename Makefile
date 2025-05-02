format:
	uv run ruff format src
	uv run isort src

dev:
	uv run fastapi dev src/main.py
	
prod:
	uv run fastapi run src/main.py
