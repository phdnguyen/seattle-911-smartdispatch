1. DESCRIPTION
Seattle 911 SmartDispatch is a streamlined analytic toolkit and dashboard for exploring emergency-response patterns in Seattle’s 911 system. It combines cleaned CAD (Computer-Aided Dispatch) data with lightweight machine-learning models to help users spot unusually slow responses, call-volume spikes, routing irregularities, and other operational anomalies.

Two core analytical components power the system:
• An XGBoost response-time model that estimates how long a unit is expected to take based on call type, priority, and spatial–temporal context.
• An Isolation Forest anomaly detector that highlights dispatch hours exhibiting abnormal service times or volume patterns.

These outputs integrate into a Streamlit dashboard featuring heatmaps, incident-flow timelines, and two context-aware “What-If” checkers that let users test hypothetical scenarios (for example: “Would a 12-minute response at this hour in this sector be considered abnormal?”). A public demo (Jan–Jun 2025 data) is available online at:
https://seattle-911.streamlit.app/


2. INSTALLATION
Create the environment using the provided environment.yml file:

conda env create -f environment.yml
conda activate <env>

This installs Streamlit, PySpark, Pandas, gdown, and all required dependencies.

To download data, run the downloader script:

cd src/00_setup
python download_data.py

You will see:

Seattle 911 SmartDispatch – data downloader
1) Download RAW data (full pipeline)
2) Download PROCESSED output files (Streamlit only)
Select option [1/2]:

Option 1 = Downloads raw CSV and intermediate processed CSV.
Option 2 = Downloads only the final parquet files required by Streamlit.


3. EXECUTION

A. Running the Full Pipeline (RAW → SQL → Models → Dashboard)

1) Download raw data using Option 1 in download_data.py.

2) Preprocess the raw CAD data using SQL Server:
   – Import data/raw/Call_Data_20251019.csv into SQL Server.
   – Run the script at: src/01_preprocessing/preprocessing.sql
   – Export the processed output to:
     data/processed/calldata_20251019_processed_v4.csv

3) Run the modeling notebooks in order:
   – XGBoost response-time model:
     src/02_models/xgb_response_time_prediction.ipynb
   – Anomaly detection:
     src/02_models/anomaly_detection.ipynb

   Note: Several plotting cells are commented out in order to save notebook size.
   If running locally, search for “Please uncomment to plot” and remove the comment marker.

4) The notebooks automatically generate:
   data/output/calldata_20251019_processed_v4.parquet
   data/output/burst_anomaly_table.parquet
   data/output/response_anomaly_table.parquet

5) Launch the Streamlit dashboard:
   streamlit run src/03_visualizations/visualization_1.py


B. Running Only the Streamlit Dashboard

1) Run download_data.py and select option 2 to download only the processed parquet files.

2) Ensure the following files exist:
   data/output/calldata_20251019_processed_v4.parquet
   data/output/burst_anomaly_table.parquet
   data/output/response_anomaly_table.parquet

3) Launch Streamlit:
   streamlit run src/03_visualizations/visualization_1.py

This mode does not require Spark, SQL Server, or the model notebooks.