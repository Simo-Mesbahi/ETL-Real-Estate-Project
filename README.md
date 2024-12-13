# ETL Real Estate Project

## Description

Ce projet est un pipeline **ETL (Extract, Transform, Load)** complet qui :
- **Extrait** des données immobilières open source (dataset public sur les prix de l'immobilier).
- **Détecte les anomalies** dans les données extraites.
- **Stocke** les données valides dans une base MySQL.
- **Stocke les anomalies** dans une base MySQL dédiée.
- **Visualise les données et anomalies** à l'aide de **Streamlit**.

## Fonctionnalités principales
1. **Extraction des données** :
   - Source : [Dataset public sur les prix de l'immobilier](https://raw.githubusercontent.com/ageron/handson-ml/master/datasets/housing/housing.csv).

2. **Transformation** :
   - Détection des anomalies selon des conditions définies :
     - Revenus médians (`median_income`) > 15.
     - Âge médian des maisons (`housing_median_age`) > 100.

3. **Chargement** :
   - Les données valides sont chargées dans une base MySQL appelée `real_estate_data`.
   - Les anomalies sont chargées dans une base MySQL appelée `anomaly_data`.

4. **Visualisation avec Streamlit** :
   - Tableaux des données valides et des anomalies.


