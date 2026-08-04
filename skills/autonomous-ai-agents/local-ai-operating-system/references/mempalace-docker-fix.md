# MemPalace Docker Fix - NumPy/ChromaDB ABI Compatibility

## Problem

MemPalace requires ChromaDB which has strict NumPy version dependencies. On Windows with Python 3.13/3.14, the default NumPy 2.x ABI is incompatible with ChromaDB's compiled extensions (built for NumPy 1.x ABI).

**Error:**
```
ImportError: numpy._core._multiarray_umath not found
The following compiled module files exist, but seem incompatible with either python 'cpython-314' or the platform 'win32':
  * _multiarray_umath.cp311-win_amd64.pyd
```

## Root Cause

1. ChromaDB 0.4.x wheels are built against NumPy 1.24.x ABI
2. Python 3.13+ ships with NumPy 2.x by default
3. ABI mismatch causes import failure
4. uv/pip installs latest NumPy 2.x, breaking ChromaDB

## Solution: Docker with Pinned Versions

### Dockerfile (E:/_Dev_Tools/mempalace/Dockerfile)
```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install uv for fast package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files
COPY pyproject.toml uv.lock ./
COPY mempalace/ ./mempalace/
COPY scripts/ ./scripts/

# Install dependencies with uv (handles numpy/chromadb correctly)
RUN uv sync --frozen --no-dev

# Create data directories
RUN mkdir -p /app/data /app/config /app/logs

# Expose API port
EXPOSE 8001

# Set environment
ENV PYTHONPATH=/app
ENV MEMPALACE_DATA_DIR=/app/data
ENV MEMPALACE_CONFIG_DIR=/app/config
ENV MEMPALACE_LOG_DIR=/app/logs

# Default command
CMD ["uv", "run", "mempalace", "serve"]
```

### Docker Compose (E:/_Dev_Tools/mempalace/docker-compose.yml)
```yaml
version: '3.8'

services:
  # ChromaDB Vector Database
  chromadb:
    image: chromadb/chroma:0.4.24
    container_name: jarvis-chromadb
    restart: unless-stopped
    volumes:
      - mempalace_chroma:/data
    ports:
      - "8000:8000"
    environment:
      - CHROMA_SERVER_HOST=0.0.0.0
      - CHROMA_SERVER_HTTP_PORT=8000
      - ANONYMIZED_TELEMETRY=False
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/heartbeat"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - jarvis-network

  # MemPalace API Server
  mempalace-api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: jarvis-mempalace
    ports:
      - "8001:8001"
    volumes:
      - mempalace_data:/app/data
      - ./config:/app/config:ro
    environment:
      - CHROMA_HOST=chromadb
      - CHROMA_PORT=8000
      - MEMPALACE_DATA_DIR=/app/data
      - MEMPALACE_API_PORT=8001
      - OLLAMA_HOST=http://host.docker.internal:11434
      - PYTHONUNBUFFERED=1
    depends_on:
      chromadb:
        condition: service_healthy
    restart: unless-stopped
    networks:
      - jarvis-network

volumes:
  mempalace_chroma:
  mempalace_data:

networks:
  jarvis-network:
    driver: bridge
```

## Key Version Pins

| Package | Version | Reason |
|---------|---------|--------|
| Python | 3.11 | NumPy 1.24.x support, ChromaDB compatibility |
| NumPy | 1.24.4 | Last 1.x release, ChromaDB ABI compatible |
| ChromaDB | 0.4.22 | Last version with NumPy 1.x ABI |
| chromadb/chroma 0.4.24 | Container image | Matches ChromaDB client version |

## Verification

```bash
# Build and start
cd E:/_Dev_Tools/mempalace
docker-compose up -d --build

# Check health
curl http://localhost:8001/health
# {"status": "ok", "chromadb": "connected"}

# Test from host
python -c "
import chromadb
client = chromadb.HttpClient(host='localhost', port=8000)
print('ChromaDB:', client.heartbeat())
"

# Test MemPalace API
curl -X POST http://localhost:8001/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Justice Party", "limit": 5}'
```

## Alternative: Native Fix (If Docker Unavailable)

```bash
# Create isolated venv with pinned versions
python -m venv .venv-mempalace
.venv-mempalace/Scripts/activate
pip install numpy==1.24.4 chromadb==0.4.22
pip install -e .
```

**Note**: This works but requires manual activation each time. Docker is preferred for production.

## Lessons Learned

1. **Always pin NumPy < 2.0** when using ChromaDB or similar ML libraries with compiled extensions
2. **Use Docker for ML stacks** on Windows - isolates ABI issues completely
3. **Python 3.11** is the sweet spot for 2024 ML tooling compatibility
4. **ChromaDB 0.4.x** is the last series with NumPy 1.x ABI; 0.5+ may support NumPy 2.x
5. **Ollama host.docker.internal** works for local LLM access from containers