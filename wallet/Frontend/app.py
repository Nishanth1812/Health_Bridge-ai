import streamlit as st
import requests

st.title("🩺 Decentralized Health Wallet")

if st.button("Generate New Wallet"):
    wallet_res = requests.get("http://localhost:5000/generate_wallet")
    wallet_data = wallet_res.json()
    st.session_state["wallet_address"] = wallet_data["address"]
    st.session_state["private_key"] = wallet_data["private_key"]
    st.success("Wallet generated!")
    st.write("Address:", wallet_data["address"])
    st.write("Private Key:", wallet_data["private_key"])

wallet = st.text_input("Enter your wallet address:", value=st.session_state.get("wallet_address", ""))
record = st.text_area("Health Record (e.g., 'Jayani received flu vaccine')")
key = st.text_input("Secret key (to encrypt your data)", type="password")

if st.button("Submit & Mint NFT"):
    res = requests.post("http://localhost:5000/upload_record", json={
        "wallet": wallet,
        "record": record,
        "key": key
    })
    st.json(res.json())