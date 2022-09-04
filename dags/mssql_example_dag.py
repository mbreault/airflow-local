from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator
import pandas as pd
from datetime import datetime
import sys

import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

logging.basicConfig(level=logging.DEBUG)

azureLogHandler = AzureLogHandler(
    connection_string='InstrumentationKey=8cfabf88-a6e1-4956-9010-3c666c5ef516;IngestionEndpoint=https://southcentralus-0.in.applicationinsights.azure.com/;LiveEndpoint=https://southcentralus.livediagnostics.monitor.azure.com/'
    )

logging.getLogger("root").addHandler(azureLogHandler)
logging.getLogger("flask_appbuilder").addHandler(azureLogHandler)
logging.getLogger("airflow.processor").addHandler(azureLogHandler)
logging.getLogger("airflow.task").addHandler(azureLogHandler)

DAG_ID = "mssql_example_dag"

def mssql_func(**kwargs):
    hook = MsSqlHook(conn_id='mssql_default')
    df = hook.get_pandas_df(sql="SELECT * FROM dbo.RowCounts")
    pivot = pd.crosstab(df["TableName"],df["DatabaseName"],df["RowCount"],aggfunc=sum)
    print(pivot.to_csv("~/output.csv"))

dag = DAG(dag_id="mssql_example_dag",
         start_date=datetime(2021,1,1),
         schedule_interval="@daily",
         catchup=False) 

run_this = PythonOperator(
    task_id='mssql_task',
    python_callable=mssql_func,
    dag=dag,
)

run_next = BashOperator(
    task_id='bash_task',
    bash_command='echo Done',
    dag=dag,
)

run_this >> run_next

    