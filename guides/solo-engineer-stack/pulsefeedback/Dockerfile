FROM python:3.12-slim

WORKDIR /app
ENV STACK_ROOT=/app
ENV PYTHONUNBUFFERED=1

COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY artifacts/ ./artifacts/
COPY examples/ ./examples/
COPY n8n/ ./n8n/
COPY orchestrator/ ./orchestrator/

WORKDIR /app/backend
EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
