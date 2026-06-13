# Docker Deployment Guide

This guide explains how to run the Quantum Search project using Docker.

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+

Install from: https://www.docker.com/products/docker-desktop

## Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up -d

# Access services:
# - Streamlit Dashboard: http://localhost:8501
# - Jupyter Notebook:    http://localhost:8888 (if enabled)
```

### Option 2: Manual Docker Build

```bash
# Build image
docker build -t quantum-search:latest .

# Run Streamlit dashboard
docker run -p 8501:8501 -v $(pwd)/data:/app/data quantum-search:latest

# Run CLI with custom command
docker run -it quantum-search:latest python main.py --help

# Run Jupyter notebook
docker run -p 8888:8888 quantum-search:latest jupyter notebook --ip=0.0.0.0 --allow-root
```

## Services

### Quantum Search Dashboard (streamlit)

```bash
docker-compose up -d quantum-search
```

**Access**: http://localhost:8501

**Features:**
- Interactive graph exploration
- Classical vs quantum search comparison
- Real-time performance visualization
- Export results

### Jupyter Notebook Server (optional)

```bash
docker-compose up -d jupyter
```

**Access**: http://localhost:8888

**Features:**
- Interactive tutorials
- Code experimentation
- Benchmark analysis
- Circuit visualization

## Useful Commands

```bash
# View logs
docker-compose logs -f quantum-search

# Stop all services
docker-compose down

# Remove volumes (clean data)
docker-compose down -v

# Rebuild images
docker-compose build --no-cache

# Run one-off command
docker-compose run quantum-search python main.py --demo

# Execute interactive shell
docker-compose exec quantum-search bash
```

## Volume Mounting

The docker-compose.yml mounts:

```yaml
volumes:
  - ./data:/app/data          # Results and data files
  - ./results:/app/results    # Benchmark outputs
  - ./notebooks:/app/notebooks # Jupyter notebooks
```

Any files created in containers are saved locally.

## Environment Variables

Configure in `docker-compose.yml`:

```yaml
environment:
  - PYTHONUNBUFFERED=1      # Real-time logs
  - QT_QPA_PLATFORM=offscreen # Headless display
```

## Performance Considerations

### Resource Limits

```yaml
services:
  quantum-search:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

### Caching

Docker layers are cached automatically. Rebuild only when needed:

```bash
docker-compose build --no-cache
```

## Troubleshooting

### Port Already in Use

```bash
# Find and stop conflicting container
docker ps
docker stop <container-id>

# Or use different port
docker run -p 8502:8501 quantum-search:latest
```

### Permission Denied

```bash
# Run Docker without sudo
sudo usermod -aG docker $USER
newgrp docker
```

### Out of Memory

```bash
# Increase Docker memory limit
# Settings → Resources → Memory (Docker Desktop)

# Or limit container memory
docker run -m 4g quantum-search:latest
```

### Jupyter Token/Password

Access Jupyter without authentication (current config):

```
http://localhost:8888
```

For security, set token:

```bash
docker exec quantum-search-jupyter jupyter notebook --generate-config
docker exec quantum-search-jupyter jupyter notebook password
```

## Deployment Examples

### Production Deployment (Kubernetes)

```bash
# Create image
docker build -t quantum-search:1.0 .

# Push to registry
docker tag quantum-search:1.0 myregistry/quantum-search:1.0
docker push myregistry/quantum-search:1.0

# Deploy with kubectl
kubectl create deployment quantum-search \
  --image=myregistry/quantum-search:1.0 \
  --port=8501
```

### Local Development

```bash
# Keep container running with mounted code
docker-compose up quantum-search

# Edit files locally
nano main.py

# Changes auto-reload in Streamlit
```

### CI/CD Integration

```yaml
# GitHub Actions example
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: docker/build-push-action@v2
        with:
          context: .
          push: true
          tags: myregistry/quantum-search:${{ github.sha }}
```

## Health Checks

```bash
# Check service health
docker-compose ps

# Manual health check
curl http://localhost:8501

# View health history
docker inspect quantum-search-app --format='{{.State.Health}}'
```

## Cleaning Up

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Full cleanup
docker system prune -a
```

## Advanced Configuration

### Custom Dockerfile

For development with hot-reload:

```dockerfile
FROM python:3.12-slim

WORKDIR /app
RUN pip install -e .

# Mount source code as volume
ENTRYPOINT ["python"]
CMD ["main.py"]
```

### Multi-Stage Build

The provided Dockerfile uses multi-stage build to minimize final image size (~1.2 GB).

## Support

For issues or questions:

1. Check container logs: `docker-compose logs`
2. Verify ports are accessible: `netstat -an | grep 8501`
3. Ensure sufficient disk space: `docker system df`
4. Review Dockerfile comments for configuration options

## References

- Docker Documentation: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/
- Best Practices: https://docs.docker.com/develop/dev-best-practices/
