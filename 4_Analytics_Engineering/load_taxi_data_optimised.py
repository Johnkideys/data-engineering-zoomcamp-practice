import os
import sys
import time
import urllib.request
from google.cloud import storage
from concurrent.futures import ThreadPoolExecutor


# =====================
# CONFIG
# =====================


PROJECT_ID = "zoomcamp-mod3-datawarehouse"
BUCKET_NAME = "jkdys_dezoomcamp_week3"


TAXI_TYPES = ["yellow", "green"]
YEARS = ["2019", "2020"]
MONTHS = [f"{i:02d}" for i in range(1, 13)]


BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download"


DOWNLOAD_DIR = "."
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


# Folder mapping
FOLDER_MAP = {
    "yellow": "yellow_19_20",
    "green": "green_19_20"
}


# =====================
# GCS Client
# =====================


client = storage.Client(project=PROJECT_ID)
bucket = client.bucket(BUCKET_NAME)


# =====================
# Download Function
# =====================


def download_file(taxi_type, year, month):


    file_name = f"{taxi_type}_tripdata_{year}-{month}.csv.gz"
    url = f"{BASE_URL}/{taxi_type}/{file_name}"
    file_path = os.path.join(DOWNLOAD_DIR, file_name)

    # CHECK: Does the file exist locally?
    if os.path.exists(file_path):
        print(f"Local file already exists: {file_path}. Skipping download.")
        return file_path


    try:
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, file_path)
        print(f"Downloaded: {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None


# =====================
# Upload Function
# =====================


def upload_to_gcs(taxi_type, year, month, max_retries=3):
    file_name = f"{taxi_type}_tripdata_{year}-{month}.csv.gz"
    file_path = os.path.join(DOWNLOAD_DIR, file_name)
    
    # Define the blob path with folder structure
    blob_path = f"{FOLDER_MAP[taxi_type]}/{file_name}"
    blob = bucket.blob(blob_path)

    blob.chunk_size = 5 * 1024 * 1024  # 5MB chunks
    
    for attempt in range(max_retries):
        try:
            print(f"Uploading {file_path} to gs://{BUCKET_NAME}/{blob_path} (Attempt {attempt + 1})...")
            blob.upload_from_filename(file_path)
            print(f"Uploaded: gs://{BUCKET_NAME}/{blob_path}")
            return True
        except Exception as e:
            print(f"Failed to upload {file_path} to GCS: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in 5 seconds...")
                time.sleep(5)
    
    print(f"Giving up on {file_path} after {max_retries} attempts.")
    return False


# =====================
# Download + Upload Combined
# =====================


def download_and_upload(taxi_type, year, month):
    """Download file and then upload to GCS"""

    
    file_path = download_file(taxi_type, year, month)
    
    if file_path:
        upload_to_gcs(taxi_type, year, month)
        
        # Optional: Delete local file after successful upload
        # os.remove(file_path)
        # print(f"Deleted local file: {file_path}")


# =====================
# MAIN
# =====================


if __name__ == "__main__":


    tasks = [
        (taxi, year, month)
        for taxi in TAXI_TYPES
        for year in YEARS
        for month in MONTHS
    ]


    # Test with just the first file
    #tasks = tasks[:1]


    # Option 1: Test single file
    # download_and_upload("yellow", "2019", "02")
    # download_and_upload("yellow", "2019", "03")
    # download_and_upload("yellow", "2019", "04")
    # download_and_upload("yellow", "2019", "05")
    
    # Option 2: Run all tasks with ThreadPoolExecutor (uncomment when ready)
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(lambda args: download_and_upload(*args), tasks)


    print("All uploads finished.")
