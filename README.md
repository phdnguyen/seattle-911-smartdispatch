# Seattle 911 SmartDispatch
Predictive modeling and visual analytics of Seattle 911 call data for dispatch efficiency.

## Dataset
The dataset is publicly available on the [Seattle Open Data Portal](https://data.seattle.gov/Public-Safety/Call-Data/33kz-ixgy).

Data used for this project is last updated on October 18th, 2025 and has 10.5M rows.

## Environment Set-up
conda create --name <env> --file environment.yml

## Directory Tree

```
.
├── data
│   ├── processed
│   └── raw
│       └── Call_Data_20251019.csv
├── environment.yml
├── notebooks
│   ├── 01_exploration.ipynb
│   ├── 02_modeling.ipynb
│   └── 03_visualization.ipynb
├── README.md
├── reports
│   ├── progress_report
│   └── proposal
│       └── team102proposal.pdf
└── src
    ├── config.py
    ├── modeling.py
    ├── preprocessing.py
    └── visualization.py
```