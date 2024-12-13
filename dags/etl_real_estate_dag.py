from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import sqlalchemy

# Configurations MySQL
MYSQL_DATA_CONN = "mysql+pymysql://airflow:airflow@mysql-data:3306/real_estate_data"
MYSQL_ANOMALIES_CONN = "mysql+pymysql://airflow:airflow@mysql-anomalies:3306/anomaly_data"

# Source open source
DATA_SOURCE = "https://raw.githubusercontent.com/ageron/handson-ml/master/datasets/housing/housing.csv"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Détection des anomalies
def detect_anomalies(data):
    anomalies = data[(data["median_income"] > 15) | (data["housing_median_age"] > 100)]
    valid_data = data.drop(anomalies.index)
    return valid_data, anomalies

# Extraction des données
def extract_data():
    data = pd.read_csv(DATA_SOURCE)
    return data

# Transformation et détection des anomalies
def transform_data(**kwargs):
    ti = kwargs["ti"]
    data = ti.xcom_pull(task_ids="extract_data")
    valid_data, anomalies = detect_anomalies(data)
    return {"valid_data": valid_data.to_dict(), "anomalies": anomalies.to_dict()}

# Chargement des données
def load_data(**kwargs):
    ti = kwargs["ti"]
    result = ti.xcom_pull(task_ids="transform_data")
    valid_data = pd.DataFrame(result["valid_data"])
    anomalies = pd.DataFrame(result["anomalies"])

    # Connexion MySQL
    valid_engine = sqlalchemy.create_engine(MYSQL_DATA_CONN)
    anomaly_engine = sqlalchemy.create_engine(MYSQL_ANOMALIES_CONN)

    valid_data.to_sql("real_estate", valid_engine, if_exists="replace", index=False)
    anomalies.to_sql("real_estate_anomalies", anomaly_engine, if_exists="replace", index=False)

with DAG(
    "etl_real_estate",
    default_args=default_args,
    description="ETL avec détection des anomalies",
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    extract = PythonOperator(
        task_id="extract_data",
        python_callable=extract_data,
    )

    transform = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data,
        provide_context=True,
    )

    load = PythonOperator(
        task_id="load_data",
        python_callable=load_data,
        provide_context=True,
    )

    extract >> transform >> load
