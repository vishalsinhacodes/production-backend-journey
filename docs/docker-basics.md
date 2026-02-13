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
