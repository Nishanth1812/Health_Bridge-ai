from eth_account import Account
import secrets

Account.enable_unaudited_hdwallet_features()

def generate_wallet():
    acct = Account.create(secrets.token_hex(32))
    return {
        "address": acct.address,
        "private_key": acct.key.hex()
    }