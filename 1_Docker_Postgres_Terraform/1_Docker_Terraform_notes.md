# Docker and Terraform Notes

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

Difference between "docker run" and "docker start"
docker run: Creates a new container from an image AND starts it
docker start: Starts an existing container that is stopped
docker ps -a: To check containers 
docker images -a: To check images


To create a docker network so that containers can communicate:
docker network create pg-network

### Connecting multiple containers to same docker network

running postgres with docker:
docker run -d --name postgres   -e POSTGRES_USER=root   -e POSTGRES_PASSWORD=root   -e POSTGRES_DB=ny_taxi   -p 5432:5432   postgres:16

running postgres with docker (in the network we created):
docker run -it --rm --name pg-database  --network=pg-network -e POSTGRES_USER=root   -e POSTGRES_PASSWORD=root   -e POSTGRES_DB=ny_taxi   -p 5432:5432   postgres:16

 --name pg-database: Also chnaged the name for the above, the name is important for other contaioners to reference it on the same network
--network=pg-network: Added this

 running our ingestion script with docker (in the network we created):
 docker run -it --rm --network=pg-network taxi_ingest:v001 --pg-host=pg-database

 Important: We chnaged the --pg-host=pg-database (default was localhost which was pointing to the localhost of the taxi_ingest:v001 containers localhost - see slides to visualise)

In another terminal, run pgAdmin on the same network
```
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```

### Running the Above with Docker Compose

created docker-compose.yaml file.
By default evertyhing run inside the docker-compose.yaml file runs on the same network.

After running docker compose up, the containers have started again from scratch so we need to re-run the ingestion script. We now check ```docker network ls ``` and see pipeline_deafult, which docker compose up automatically created. 

Run the ingestion script in that network:

```
docker run -it --rm --network=pipeline_default taxi_ingest:v001 --pg-host=pgdatabase
```
Dont Forget: --pg-host=pgdatabase has to be passed now so the ingestion script knows which host to go to
“When running the ingestion container inside a Docker network, I must tell the script to connect to Postgres using the container name, not localhost.”

## Terraform Notes

For local development and testing, we use Application Default Credentials (ADC) so the Terraform Google provider can authenticate and make changes to Google Cloud as our user during local development.

We could instead create a service account key and grant it permissions for Terraform to use, but this is less secure and not recommended for local development. ADC is safer because it uses short-lived OAuth tokens and no private keys.

#### Local setup (once per machine)
I installed the google sdk locally.
```
brew install --cask google-cloud-sdk
gcloud init
gcloud auth application-default login # For terraform to use
```

#### Terraform workflow

```
terraform fmt # to make .tf file code nicer
terraform init # Download providers & initialise backend
terraform plan # Show proposed changes
```

```
resource "<PROVIDER>_<THING>" "<TERRAFORM_NAME>" {
  real_cloud_settings_here
}
```