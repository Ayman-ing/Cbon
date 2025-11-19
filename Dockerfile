FROM python:3.11-slim

# Install uv
RUN pip install uv

WORKDIR /app

# Copy lockfiles first for cache
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen  # Installs from lockfile, super fast

# Copy code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]