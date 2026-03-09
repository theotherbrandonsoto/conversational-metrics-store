import os
import zipfile
from pathlib import Path
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()
os.environ["KAGGLE_USERNAME"] = os.getenv("KAGGLE_USERNAME")
os.environ["KAGGLE_KEY"] = os.getenv("KAGGLE_KEY")

import kaggle  # must be imported AFTER env vars are set

DATASET = "jayjoshi37/customer-subscription-churn-and-usage-patterns"
RAW_DIR = Path("data/raw")

def download_dataset():
    print(f"Downloading latest version of: {DATASET}")
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(
        DATASET,
        path=RAW_DIR,
        unzip=True,
        force=True  # always pull the latest version
    )
    print(f"✅ Download complete. Files saved to {RAW_DIR}/")
    list_files()

def list_files():
    files = list(RAW_DIR.glob("*"))
    print(f"\nFiles in {RAW_DIR}:")
    for f in files:
        size_kb = f.stat().st_size / 1024
        print(f"  {f.name}  ({size_kb:.1f} KB)")

if __name__ == "__main__":
    download_dataset()