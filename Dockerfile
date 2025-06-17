FROM apache/airflow:slim-latest-python3.10

WORKDIR /opt/airflow

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt