# Seattle 911 SmartDispatch
Predictive modeling and visual analytics of Seattle 911 call data for dispatch efficiency.

## Dataset
The dataset is publicly available on the [Seattle Open Data Portal](https://data.seattle.gov/Public-Safety/Call-Data/33kz-ixgy).

Data used for this project is last updated on October 18th, 2025 and has 10.5M rows.

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