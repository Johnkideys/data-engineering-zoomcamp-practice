FROM python:3.13.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code

COPY pyproject.toml .python-version uv.lock ./
RUN uv sync --locked

COPY pipeline.py .

ENTRYPOINT ["uv", "run", "python", "pipeline.py", "12"]


# Version 1
# FROM python:3.13.11-slim

# RUN pip install pandas pyarrow

# WORKDIR /code

# COPY pipeline.py .

# ENTRYPOINT ["python", "pipeline.py", "12"]