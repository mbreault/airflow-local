#!/bin/bash

# Airflow needs a home. `~/airflow` is the default, but you can put it
# somewhere else if you prefer (optional)
source .venv/bin/activate
export AIRFLOW_HOME=~/airflow
export AIRFLOW_CONFIG=$AIRFLOW_HOME/airflow.cfg
export PYTHONASYNCIODEBUG=1

# Install Airflow using the constraints file
AIRFLOW_VERSION=2.3.4
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
# For example: 3.7
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example: https://raw.githubusercontent.com/apache/airflow/constraints-2.3.4/constraints-3.7.txt
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
pip install apache-airflow-providers-microsoft-mssql[common.sql]
pip install apache-airflow-providers-common-sql[pandas]
pip install pandas
pip install pymssql

airflow standalone 
