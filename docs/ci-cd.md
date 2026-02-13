# CI/CD Pipeline – GitHub Actions

## What is CI/CD?

CI (Continuous Integration):
Automatically tests and builds code whenever changes are pushed.

CD (Continuous Delivery/Deployment):
Automatically prepares the application for deployment.

In our project:
We implemented CI using GitHub Actions.

---

## Workflow Location

Path:
.github/workflows/ci.yml

GitHub automatically detects workflows placed in this directory.

---

## Trigger Configuration

Current setup:

on:
push:
pull_request:

This means:

- The pipeline runs on every push.
- The pipeline runs on every pull request.

---

## Pipeline Steps

1. Checkout Code
   Uses: actions/checkout

2. Setup Python
   Python 3.11 environment

3. Install Dependencies
   pip install -r requirements.txt

4. Build Docker Image
   docker build -t backend-app .

If any step fails → pipeline fails.

---

## Why This Is Important

- Ensures code always builds successfully.
- Detects breaking changes early.
- Verifies Docker image integrity.
- Builds automation discipline.

---

## Learning Outcomes

- Understanding GitHub Actions structure
- YAML indentation sensitivity
- Branch-based triggering
- CI failure detection
- Automated Docker builds
