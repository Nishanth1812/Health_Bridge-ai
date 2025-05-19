from flask import Flask, request, jsonify
from encrypt_utils import encrypt_data
from ipfs_utils import upload_to_ipfs
from verbwire_utils import mint_soulbound_nft
from wallet_utils import generate_wallet

app = Flask(__name__)

@app.route("/generate_wallet", methods=["GET"])
def create_wallet():
    wallet = generate_wallet()
    return jsonify(wallet)

@app.route("/upload_record", methods=["POST"])
def upload_record():
    data = request.json
    wallet = data["wallet"]
    raw_text = data["record"]
    key = data["key"]

    encrypted = encrypt_data(raw_text, key)
    ipfs_link = upload_to_ipfs(encrypted.encode())

    nft = mint_soulbound_nft(wallet, metadata_url=ipfs_link)
    return jsonify(nft)

if __name__ == "__main__":
    app.run(port=5000)
