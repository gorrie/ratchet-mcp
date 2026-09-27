# Tradecraft Lens backend — /grade-text + serves the UI. Build context = evil-robots-series root
# (needs the tradecraft engine + the ratchet_mcp package + the lens).
FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir requests feedparser pyyaml

# tradecraft engine + lens taxonomies (the detectors/ dir)
COPY tradecraft/ /app/tradecraft/
# ratchet_mcp package (lens imports its _import_tradecraft helpers) + the lens server/UI
COPY research/ratchet-mcp/server/ /app/server/
COPY research/ratchet-mcp/lens/ /app/lens/

ENV PYTHONPATH=/app/server:/app
ENV TRADECRAFT_PATH=/app/tradecraft
ENV LENS_PORT=8770
EXPOSE 8770
CMD ["python", "/app/lens/lens_server.py"]
