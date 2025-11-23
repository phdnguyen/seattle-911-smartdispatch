# Seattle 911 SmartDispatch
This project provides an interactive Streamlit dashboard for exploring Seattle’s 911 call and dispatch patterns. It uses lightweight machine-learning models and anomaly detection to help identify unusually slow response times, call-volume spikes, and other irregular operational patterns.

The app combines cleaned Seattle 911 open data with two analytical modules: an XGBoost model that predicts expected response time based on incident context, and an Isolation Forest that flags atypical hourly patterns. These results feed into visual tools such as temporal–spatial heatmaps, incident-flow timelines, and two “What-If” checkers that let users test hypothetical scenarios and see whether they would be considered anomalous.

A live demo version using data from Januanry to June 2025 is available at [Streamlit Cloud App](https://seattle-911.streamlit.app/).

## Dataset
The dataset is publicly available on the [Seattle Open Data Portal](https://data.seattle.gov/Public-Safety/Call-Data/33kz-ixgy).

Raw data used for this project is last updated on October 18th, 2025 and has 10.5M rows.

## Environment Set-up
conda create --name `<env>` --file environment.yml

## Directory Tree

```
.
├── data
│   ├── output
│   │   ├── burst_anomaly_table.csv
│   │   ├── burst_anomaly_table.parquet
│   │   ├── response_anomaly_table.csv
│   │   └── response_anomaly_table.parquet
│   ├── processed
│   │   ├── calldata_20251019_processed_v4_small.csv
│   │   └── calldata_20251019_processed_v4.csv
│   └── raw
│   │   └── Call_Data_20251019.csv
├── environment.yml
├── figures
│   ├── incident_flow_timeline_response_time_anomalies.png
│   └── xgb_feature_importance.png
├── README.md
└── src
    ├── 01_preprocessing
    │   └── preprocessing.sql
    ├── 02_models
    │   ├── anomaly_detection.ipynb
    │   └── xgb_response_time_prediction.ipynb
    └── 03_visualizations
        ├── visualization_1.py
        └── visualizations_2.ipynb
```