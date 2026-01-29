# Docker Files Organization

This directory contains all Docker-related files for the project.

## Files

### `Dockerfile.dev`
Development environment Dockerfile used by:
- `.devcontainer/devcontainer.json` (VS Code/Antigravity dev containers)
- `.devcontainer/docker-compose.yml` (standalone Docker Compose)

**Base Image:** `arm64v8/debian:latest`

**Includes:**
- Node.js 22.x
- Git
- Python 3
- Development user: `builduser` (UID: 20001)

### `Dockerfile.prod` (Future)
Production-optimized Dockerfile (to be created when needed)

## Usage

### Build Development Image
```bash
docker build -f docker/Dockerfile.dev -t ai-business-assistant:dev .
```

### Use with DevContainer
The `.devcontainer/` configuration automatically references this Dockerfile.

### Use with Docker Compose
```bash
cd .devcontainer
docker-compose up -d
```

## Notes

- All Dockerfiles use the project root as build context
- Build arguments are defined in `.devcontainer/docker-compose.yml`
- See `.dockerignore` in project root for excluded files
