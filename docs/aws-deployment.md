# AWS EC2 Deployment – Production Backend

## Objective

Deploy Dockerized FastAPI application to AWS EC2 instance using:

- Docker Hub image
- Version tagging
- PostgreSQL container
- Custom Docker network

---

## Infrastructure Setup

### 1. EC2 Configuration

- OS: Ubuntu Server 24.04 LTS
- Instance Type: t3.micro
- Storage: 8GB
- Security Group Rules:
  - SSH (22) → My IP
  - Custom TCP (8000) → 0.0.0.0/0

---

## SSH Access (Windows)

Key permission fix:

icacls backend-key.pem /inheritance:r
icacls backend-key.pem /remove "NT AUTHORITY\\Authenticated Users"
icacls backend-key.pem /remove "BUILTIN\\Users"
icacls backend-key.pem /grant:r "${env:USERNAME}:R"

SSH Command:
ssh -i backend-key.pem ubuntu@<public-ip>
<public-ip> means here EC2 public IPv4

---

## Docker Setup on EC2

sudo apt update && sudo apt upgrade -y
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu

---

## Multi-Container Deployment

### 1. Create Docker Network

docker network create backend-network

---

### 2. Run PostgreSQL Container

docker run -d \
 --name postgres-db \
 --network backend-network \
 -e POSTGRES_USER=postgres \
 -e POSTGRES_PASSWORD=<password> \
 -e POSTGRES_DB=backend_db \
 postgres:15

---

### 3. Run Backend Container

docker run -d \
 --name backend-prod \
 --network backend-network \
 -p 8000:8000 \
 -e DATABASE_URL=postgresql://postgres:<password>@postgres-db:5432/backend_db \
 <dockerhub-username>/production-backend-app:<commit-tag>

---

## Deployment Verification

1. docker ps
2. curl http://localhost:8000/health
3. http://<public-ip>:8000/health

---

## Production Lessons Learned

- Docker Compose locally ≠ docker run in cloud
- Environment variables must be passed explicitly
- Containers require shared network for service discovery
- Public port must be allowed in security group
- Retry logic prevents startup crashes
- Version tagging allows stable deployment
- Always terminate EC2 after testing to prevent charges

---

## Financial Safety Steps

- Terminate EC2 instance
- Verify running instances = 0
- Confirm instance state = Terminated
