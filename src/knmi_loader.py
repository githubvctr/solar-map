import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Load API token from .env file
load_dotenv()
API_TOKEN = os.getenv("KNMI_API_TOKEN")

BASE_URL = "https://api.dataplatform.knmi.nl/open-data/v1"
DATASET = "10-minute-in-situ-meteorological-observations"
VERSION = "1.0"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}"
}

def list_available_files():
    url = f"{BASE_URL}/datasets/{DATASET}/versions/{VERSION}/files"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()["files"]

def get_file_url(filename):
    url = f"{BASE_URL}/datasets/{DATASET}/versions/{VERSION}/files/{filename}/url"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()["temporaryDownloadUrl"]

def download_latest_dataframe():
    files = list_available_files()
    latest_file = sorted(files, key=lambda x: x["fileName"], reverse=True)[0]["fileName"]
    print(f"Latest file: {latest_file}")
    download_url = get_file_url(latest_file)
    return pd.read_csv(download_url, sep=";")
