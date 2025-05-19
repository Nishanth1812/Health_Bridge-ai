import requests
import os
from dotenv import load_dotenv

load_dotenv()

def mint_soulbound_nft(wallet_address, metadata_url):
    api_key = os.getenv("VERBWIRE_API_KEY")
    url = "https://api.verbwire.com/v1/nft/mint/mintFromMetadataUrl"
    payload = {
        "allowPlatformToOperateToken": "true",
        "chain": "ethereumSepolia",
        "name": "Health Passport NFT",
        "recipientAddress": wallet_address,
        "metadataUrl": metadata_url
    }
    headers = {
        "X-API-Key": api_key
    }
    response = requests.post(url, headers=headers, data=payload)
    return response.json()