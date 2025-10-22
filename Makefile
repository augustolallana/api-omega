format:
	uv run ruff format src
	uv run isort src
dev:
	uv run uvicorn src.main:app --reload
prod:
	uv run uvicorn src.main:app
reset-db:
	docker-compose down -v 
	docker-compose up -d
deploy-db:
	docker-compose up -d
shutdown-db:
	docker-compose down