#!bin/bash

# Load .env file
set -o allexport
source .env
set +o allexport



# start up podman
if ! podman machine info &> /dev/null; then
  echo "Podman machine is not running. Starting it now..."
  podman machine start
else
  echo "Podman machine already running"
fi


podman run -d \
  --name airflow-postgres \
  -e POSTGRES_USER=airflow \
  -e POSTGRES_PASSWORD=airflow \
  -e POSTGRES_DB=airflow \
  -v ~/podman-volumes/airflow-postgres-data:/var/lib/postgresql/data \
  -p 5438:5432 \
  postgres:15

# log path for airflow
mkdir -p /Users/mathieucardinal/airflow-logs

podman run -d --env-file .env my-airflow airflow db migrate
podman run -d --env-file .env \
        -v ~/airflow-logs:/opt/airflow/logs \
        -v /Users/mathieucardinal/repos/pga/dags:/opt/airflow/dags \
        -v /Users/mathieucardinal/repos/pga/plugins:/opt/airflow/plugins \
        -p 8080:8080 \
        --name airflow-webserver \
        my-airflow airflow webserver 
podman run -d --env-file .env \
        -v ~/airflow-logs:/opt/airflow/logs \
        -v /Users/mathieucardinal/repos/pga/dags:/opt/airflow/dags \
        -v /Users/mathieucardinal/repos/pga/plugins:/opt/airflow/plugins \
        --name airflow-scheduler \
        my-airflow airflow scheduler 


