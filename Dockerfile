FROM apache/airflow:slim-latest-python3.10

WORKDIR /opt/airflow

USER root

RUN apt-get update && apt-get install -y gcc



USER airflow
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt