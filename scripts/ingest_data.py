# Placeholder ingest script
import os
import shutil

RAW_DIR = "data/raw/"
EXTERNAL_DIR = "data/external/"

def ingest_files():
    for file_name in os.listdir(EXTERNAL_DIR):
        src = os.path.join(EXTERNAL_DIR, file_name)
        dest = os.path.join(RAW_DIR, file_name)
        shutil.copy(src, dest)
        print(f"Ingested: {file_name}")

if __name__ == "__main__":
    ingest_files()
