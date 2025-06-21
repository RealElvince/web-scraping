FROM apache/airflow:slim-latest-python3.10

WORKDIR /opt/airflow

# Switch to root to install system dependencies
USER root

# Install git and gcc in one layer and clean up to reduce image size
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch back to airflow user (required by Airflow base image)
USER airflow

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
