format:
	uv run ruff format src
	uv run isort src
dev:
	uv run uvicorn src.main:app --reload
prod:
	uv run uvicorn src.main:app
reset-db:
	sudo docker-compose down -v 
	sudo docker-compose up -d
deploy-db:
	sudo docker-compose up -d
shutdown-db:
	sudo docker-compose down