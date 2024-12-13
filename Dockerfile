# Utiliser l'image de base Airflow
FROM apache/airflow:2.5.0

# Mettre à jour pip
RUN pip install --upgrade pip

# Copier les dépendances
COPY requirements.txt /requirements.txt

# Installer les dépendances
RUN pip install -r /requirements.txt

# Copier les dossiers nécessaires
COPY dags/ /opt/airflow/dags/
COPY plugins/ /opt/airflow/plugins/
COPY visualizations/ /opt/airflow/visualizations/

# Définir le répertoire de travail
WORKDIR /opt/airflow

# Commande par défaut
CMD ["airflow", "webserver"]
