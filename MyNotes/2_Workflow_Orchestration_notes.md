## What is Kestra

- Build with Flow code (YAML), No-code or with the AI Copilot - flexibility in how you build your workflows.
- Language agnostic
- Scheduled or event driven

### Running Kestra from docker-compose.yaml

Kestra exposes two ports (can be seen in the docker compose file) because it has two roles:
- 8080 = UI + API
- 8081 = worker / orchestration traffic

We create 2 services, one kestra and the other kestra_postgres.
kestra_postgres is the metadata database. It stores:
- workflows
- executions
- logs
- task state
- queues
--
- Is not your data warehouse
- Is not your taxi data
- Exists only to support Kestra

Why not bundle Postgres inside the Kestra container?
Because that would be bad architecture:
❌ No persistence if container dies
❌ Can’t scale

### ETL vs ELT

We have done an etl pipeline by downloading data from github, storing it in postgres,
creating unique id column, also learned about backfilling and using triggers to automatically load new data each month. Howwever doing this in postgres can be slow when we load full dataset (i.e creating unique_id column for millions of rows etc) so we will use the cloud now.

We will make an ELT pipeline (extract-load-transform), by loading the dataset into a google cloud srtorage bucket (the data lake with all the raw data), and then use google bigquery (the data warehouse) for transformations.

BigQuery allows us to either reference data directly from GCS using external tables or load it into native BigQuery tables for faster, columnar, distributed processing. This ELT approach leverages BigQuery’s serverless architecture and parallel execution, making large scale transformations significantly faster and more efficient than running them in Postgres.