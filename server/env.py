import os

class Config:
    eth_gateway = ""
    eth_account = ""
    eth_contract = ""
    pinata_uri = ""
    pinata_key = ""

def init_env() -> Config:
    cfg = Config()
    cfg.eth_account = os.getenv("ETH_ACCOUNT")
    cfg.eth_gateway = os.getenv("ETH_GATEWAY")
    cfg.eth_contract = os.getenv("ETH_CONTRACT")
    cfg.pinata_uri = os.getenv("PINATA_URI")
    cfg.pinata_key = os.getenv("PINATA_KEY")