# Omega REST API

This is a Fastapi project that connects with Google AppSheets.

## Database Setup

The project uses PostgreSQL as the database. You can deploy it using Docker:

1. Create a `.env` file in the project root with your database credentials:
   ```env
   POSTGRES_USER=<username>
   POSTGRES_PASSWORD=<password>
   POSTGRES_DB=<db-name>
   POSTGRES_HOST=<host>
   POSTGRES_PORT=<port>
   ```

   For host and port it is recommended to use `localhost` and port `5432`.
2. Start the database container:
   ```bash
   make deploy-db
   ```

The database will be accessible at:
- Host: <host>
- Port: <port>
- Database: <db-name>
- Username: <username>
- Password: <password>

## Project Deployment

1. Clone the repository
2. Download [uv](https://docs.astral.sh/uv/) if necessary.
3. Run uv sync to download the dependencies.
4. Run make prod to deploy the server. The terminal will show the host and port.

## Development

Make sure to test in development mode. To do so run make dev. 
Once the changes are sufficient format your files with make format. 

In the near future pull requests will be a must before merging to main.

## Database Management

### Start Database
To start the database:
```bash
make deploy-db
```

### Reset Database
To reset the database (stops containers and removes all data):
> [!WARNING]
> This will delete all data!
```bash
make reset-db
```

### Stop Database
To stop the database:
```bash
make shutdown-db
```

### View Logs
To view database logs:
```bash
docker-compose logs db
```

### Backup
To backup your database:
```bash
docker-compose exec db pg_dump -U ${POSTGRES_USER} ${POSTGRES_DB} > backup.sql
```

### Restore
To restore from a backup:
```bash
docker-compose exec -T db psql -U ${POSTGRES_USER} ${POSTGRES_DB} < backup.sql
```