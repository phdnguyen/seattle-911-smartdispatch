import gdown
import os

# make sure the output directory exists
os.makedirs("data/output", exist_ok=True)

file_id = "1MomO8_UcOT1aK8XHYNMyWYiBIYqjpRw4"
url = f"https://drive.google.com/uc?id={file_id}"

output_path = "data/output/response_anomaly_table.parquet"

gdown.download(url, output_path, quiet=False)