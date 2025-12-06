## Project Management Backend Setup

This project uses Docker Compose to run only the PostgreSQL database in a container. The Python backend runs locally on your machine.

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### How to Start the Database
1. Clone the repository:
	```sh
	git clone <repo-url>
	cd backend
	```
2. Start the PostgreSQL database:
	```sh
	docker-compose up
	```
	This will start the PostgreSQL database only.

### Connecting Your Local Backend
- Use these connection settings in your Python code:
  - `DB_NAME=cbon_db(name in general)`
  - `DB_HOST=db(connection)`
  - `DB_PORT=5432(connection)`
  - `DB_USER=cbonuser(connection)`
  - `DB_PASSWORD=cbonpass(connection)`

You can change these in `docker-compose.yml` if needed.

### Stopping the Database
```sh
docker-compose down
```

### Notes
- Database data is persisted in a Docker volume (`db_data`).
- Make sure your backend dependencies (e.g., psycopg2) are installed locally.
