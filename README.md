# Production Backend Journey

Goal:
To build production-ready backend systems with Docker, CI/CD, and Cloud deployment.

Week 1:

- FastAPI basic app
- Health endpoint

## Architecture Overview

- FastAPI application (Dockerized)
- PostgreSQL database (Dockerized)
- Multi-container orchestration using Docker Compose
- Environment variable configuration using .env
- Persistent database volume
- Container lifecycle management
- Multi-container networking
- Service-to-service communication
- Volume persistence handling
- Container inspection and debugging
- Optimized Docker image using .dockerignore and layered builds

## CI/CD

- Automated CI pipeline using GitHub Actions
- Docker image automatically built on each push
- Ensures build integrity

## Cloud Deployment

- Deployed Dockerized backend to AWS EC2
- Pulled image from Docker Hub (CI-built)
- Multi-container deployment with PostgreSQL
- Public endpoint verification
- Infrastructure cleanup verification

## Documentation

- See docs/docker-basics.md
