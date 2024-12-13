import streamlit as st
import pandas as pd
import sqlalchemy

# Configurations MySQL
MYSQL_DATA_CONN = "mysql+pymysql://airflow:airflow@mysql-data:3306/real_estate_data"
MYSQL_ANOMALIES_CONN = "mysql+pymysql://airflow:airflow@mysql-anomalies:3306/anomaly_data"

def fetch_data(query, connection_string):
    engine = sqlalchemy.create_engine(connection_string)
    return pd.read_sql(query, engine)

st.title("Visualisation des Données Immobilières")

# Afficher les données valides
st.subheader("Données Valides")
valid_data = fetch_data("SELECT * FROM real_estate", MYSQL_DATA_CONN)
st.write(valid_data)

# Afficher les anomalies
st.subheader("Anomalies")
anomalies = fetch_data("SELECT * FROM real_estate_anomalies", MYSQL_ANOMALIES_CONN)
st.write(anomalies)
