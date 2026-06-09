# Ratchet MCP server image. Slim Python base, install the package, run over stdio.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install package first, then the data directory is bind-mounted by compose
# (or copied in for the standalone image).
COPY pyproject.toml ./
COPY ratchet_mcp ./ratchet_mcp
RUN pip install .

# Default data location inside the container; compose overrides with a bind mount.
COPY data /app/data
ENV RATCHET_DATA_DIR=/app/data

# MCP over stdio.
ENTRYPOINT ["ratchet-mcp"]
