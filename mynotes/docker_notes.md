# Docker Notes

### Docker Container and terminal commands
```bash
docker run -it --entrypoint=bash -v $(pwd)/test:/app/test python:3.13.11-slim
```
This command starts a Docker container from the python:3.13.11-slim image, opens an interactive Bash shell inside the container, and mounts a local directory (./test) into the container at /app/test.
This allows files on the host machine to be accessed and modified from inside the container.

```--entrypoint=bash```
Overrides the default command of the image
Starts the container with a Bash shell instead of the default Python process
Useful for:
Debugging
Exploring the filesystem
Running commands manually inside the container

``` -v <host_path>:<container_path> ```

### Virtual Environment

```
pip install uv
uv init --python 3.13
uv run python -V
    Using CPython 3.13.11
    Creating virtual environment at: .venv
    Python 3.13.11

uv add pandas pyarrow - to install packages
```

Why uv ? Extremely fast installs (much faster than pip)

### Docker Image

```
FROM python:3.13.11-slim
RUN pip install pandas pyarrow
WORKDIR /code
COPY pipeline.py .
```

After creating the Dockerfile above we ran the code
```
docker build -t test:pandas .
```
I became confused about which is the image between 'python:3.13.11-slim' and 'test:pandas'
Is FROM python:3.13.11-slim the image?
Yes - but not your image.

FROM python:3.13.11-slim means “Start building my image from the existing image named python:3.13.11-slim.”
```
Docker Hub
└── python:3.13.11-slim  ← already exists

Your machine
└── docker build -t test:pandas .
    ├── starts from python:3.13.11-slim
    ├── adds pandas + pyarrow
    ├── copies piepline.py
    └── saves image as test:pandas
```

After building the image we run it:
```docker run -it --rm test:pandas ```