from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator
import pandas as pd

from datetime import datetime

DAG_ID = "mssql_example_dag"

with DAG(dag_id="mssql_example_dag",
         start_date=datetime(2021,1,1),
         schedule_interval="@hourly",
         catchup=False) as dag:

                def mssql_func(**kwargs):
                    hook = MsSqlHook(conn_id='mssql_default')
                    df = hook.get_pandas_df(sql="SELECT * FROM dbo.RowCounts")
                    pivot = pd.crosstab(df["TableName"],df["DatabaseName"],df["RowCount"],aggfunc=sum)
                    print(pivot.to_csv("~/output.csv"))

                run_this = PythonOperator(
                    task_id='mssql_task',
                    python_callable=mssql_func,
                    dag=dag
                )


    