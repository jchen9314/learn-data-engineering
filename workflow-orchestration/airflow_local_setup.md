# Airflow Setup (local, connect to GCP)

## Pre-req

- create a GCP project, create a service account and download the key (.json file), rename it and store it in `.~/.google/credentials/google_credentials.json`
- docker-compose version to v2.x+, and set the memory for your Docker Engine to minimum 5GB
(ideally 8GB). If enough memory is not allocated, it might lead to airflow-webserver continuously restarting.
- Python 3.7+

## Setup

1. create a dir called `airflow`
2. set the airflow user

   ```shell
   mkdir -p ./dags ./logs ./plugins ./scripts
   echo -e "AIRFLOW_UID=$(id -u)" > .env
   ```

3. create a customized [Dockerfile](airflow/Dockerfile):

   - install libraries specified in [requirements.txt](airflow/requirements.txt) via pip install
   - install gcloud SDK

4. docker compose

   - download docker-compose.yaml official file

     ```shell
     wget https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml
     ```

   - modify it, final version is [here](airflow/docker-compose.yaml):
     - remove `redis`, `worker`, `trigger`, `flower` services
     - move all env variables to `.env`
     - add `GCP_PROJECT_ID`, `GCP_GCS_BUCKET` variables to `.env` as well

5. build the image (~30mins for me, but only need to run it once if Dockerfile is not modified)

   ```shell
   docker-compose build
   ```

6. initialize airflow scheduler, db, ...

   ```shell
   docker-compose up airflow-init
   ```

7. launch the services from the container

   ```shell
   docker-compose up
   ```
