import requests
import os
from dotenv import load_dotenv

load_dotenv()

def upload_to_ipfs(file_bytes, filename="health_record.txt"):
    api_key = os.getenv("IPFS_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    files = {
        'file': (filename, file_bytes)
    }
    response = requests.post("https://api.nft.storage/upload", files=files, headers=headers)
    response.raise_for_status()
    cid = response.json()["value"]["cid"]
    return f"https://{cid}.ipfs.nftstorage.link/{filename}"
