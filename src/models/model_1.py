import os
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "call_data_20251019_processed_v3.csv"

df = pd.read_csv(PROCESSED_DATA_PATH)