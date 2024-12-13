from airflow.plugins_manager import AirflowPlugin
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import pandas as pd
import logging

class AnomalyDetectionOperator(BaseOperator):
    """
    Opérateur personnalisé pour détecter les anomalies dans un dataset.
    """

    @apply_defaults
    def __init__(self, data: pd.DataFrame, anomaly_conditions: list, *args, **kwargs):
        super(AnomalyDetectionOperator, self).__init__(*args, **kwargs)
        self.data = data
        self.anomaly_conditions = anomaly_conditions

    def execute(self, context):
        logging.info("Détection des anomalies dans les données...")
        anomalies = self.data.copy()
        for condition in self.anomaly_conditions:
            anomalies = anomalies.query(condition)

        logging.info(f"Nombre d'anomalies détectées : {len(anomalies)}")
        return anomalies


# Enregistrer le plugin
class AnomalyDetectionPlugin(AirflowPlugin):
    name = "anomaly_detection_plugin"
    operators = [AnomalyDetectionOperator]
