FROM python:3.13.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code

COPY pyproject.toml .python-version uv.lock ./
RUN uv sync --locked

COPY ingest_data.py .

ENTRYPOINT ["uv", "run", "python", "ingest_data.py"]


# Version 1
# FROM python:3.13.11-slim

# RUN pip install pandas pyarrow

# WORKDIR /code

# COPY pipeline.py .

# ENTRYPOINT ["python", "pipeline.py", "12"]