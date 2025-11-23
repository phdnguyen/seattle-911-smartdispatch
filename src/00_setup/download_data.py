import os
import gdown
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

RAW_FILES = {
    ROOT / "data/raw/Call_Data_20251019.csv": "15t0l4uik1-QLTu2lVjKJ6xiOsNqhFdG7",
    ROOT / "data/processed/calldata_20251019_processed_v4.csv": "1B8q53jodSzsQ3h1hE93bFRqax2DBZk57",
}

OUTPUT_FILES = {
    ROOT / "data/output/calldata_20251019_processed_v4.parquet": "1AGf8FO7J4CCsokGEGUlN2Vq8nxWkSXXT",
    ROOT / "data/output/burst_anomaly_table.parquet": "1MZcqJe4D_zLmcwaFGiV_bMqjQFv5ZALx",
    ROOT / "data/output/response_anomaly_table.parquet": "1MomO8_UcOT1aK8XHYNMyWYiBIYqjpRw4",
}

def download_group(files: dict):
    for local_path, file_id in files.items():
        local_path = Path(local_path)
        os.makedirs(local_path.parent, exist_ok=True)
        url = f"https://drive.google.com/uc?id={file_id}"

        print(f"\nDownloading to {local_path} ...")
        gdown.download(url, str(local_path), quiet=False)


def main():
    print("Seattle 911 SmartDispatch – data downloader\n")
    print("1) Download RAW data (full pipeline)")
    print("2) Download PROCESSED output files (Streamlit only)")
    choice = input("\nSelect option [1/2]: ").strip()

    if choice == "1":
        download_group(RAW_FILES)
    elif choice == "2":
        download_group(OUTPUT_FILES)
    else:
        print("Invalid choice — nothing downloaded.")


if __name__ == "__main__":
    main()