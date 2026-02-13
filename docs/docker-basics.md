# Docker Basics – Week 1

## Build Image

docker build -t backend-app .

Explanation:

- docker build → builds image from Dockerfile
- -t → tag (name of image) -> here backend-app is name of image
- . → current directory as build context

---

## Run Container (Foreground)

docker run -p 8000:8000 backend-app

- Maps container port 8000 to host port 8000

---

## Run Container (Detached Mode)

docker run -d -p 8000:8000 --name backend-container backend-app

- -d → runs in background
- --name → assign container name

---

## Check Running Containers

docker ps

---

## Check All Containers

docker ps -a

---

## Stop Container

docker stop backend-container

---

## Start Existing Container

docker start backend-container

---

## Remove Container

docker rm backend-container

---

## Remove Image

docker rmi backend-app

---

# Multi-Container Setup with Docker Compose

## Why Docker Compose?

Docker Compose allows us to run multiple services (app + database) together using a single configuration file.

---

## docker-compose.yml Overview

We defined two services:

1. db → PostgreSQL container
2. app → FastAPI container

They communicate using Docker's internal network via service name.

Example:
DATABASE_URL=postgresql://postgres:<password>@db:5432/backend_db

Note:
Inside Docker, 'localhost' does NOT refer to the host machine.
Containers communicate using service names (e.g., db).

---

## Important Commands

Start services (with rebuild):
docker compose up --build

Start services (without rebuild):
docker compose up

Stop services:
docker compose down

Check running services:
docker compose ps

---

## Environment Variables

We moved credentials into a `.env` file for better practice.

`.env` is excluded from Git using `.gitignore`.

This prevents secret leakage.

---

## Volume Persistence

PostgreSQL uses a named volume:
postgres_data:/var/lib/postgresql/data

This ensures database data is not lost when containers restart.

---

## Networking Concept

- Each service runs in its own container.
- Services communicate using service names.
- `localhost` inside container refers to the container itself.

---

## Architecture Overview

- FastAPI application (Dockerized)
- PostgreSQL database (Dockerized)
- Multi-container orchestration using Docker Compose
- Environment variable configuration using .env
- Persistent database volume

# Docker Deep Dive – Container Inspection

## Viewing Running Containers

Command:
docker ps

Shows:

- Container ID
- Image name
- Port mappings
- Running status

---

## Viewing Container Logs

Command:
docker logs <container_name>

Examples:
docker logs backend-app
docker logs postgres-db

Logs help debug:

- Startup errors
- Database connection failures
- Runtime exceptions

---

## Executing Commands Inside a Container

Command:
docker exec -it <container_name> sh

Example:
docker exec -it backend-app sh

This opens an interactive shell inside the container.

Use cases:

- Inspect file structure
- Debug environment variables
- Check installed packages
- Run internal commands

Exit container shell:
exit

---

## Docker Networks

List networks:
docker network ls

Inspect network:
docker network inspect <network_name>

Docker Compose automatically creates a private network.
All services inside docker-compose.yml share this network.

Containers communicate using service names.

Example:
Database hostname = db
Not localhost.

---

## Docker Volumes

List volumes:
docker volume ls

Inspect volume:
docker volume inspect postgres_data

Volumes store persistent data outside containers.

In our setup:
postgres_data → stores PostgreSQL data

This ensures data survives container restarts.

## Operational Knowledge Gained

- Container lifecycle management
- Multi-container networking
- Service-to-service communication
- Volume persistence handling
- Container inspection and debugging
