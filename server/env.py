import os

class Config:
    eth_gateway = ""
    eth_contract = ""
    ipfs_gateway = ""

def init_env() -> Config:
    cfg = Config()
    cfg.eth_gateway = os.getenv("ETH_GATEWAY")
    cfg.eth_contract = os.getenv("ETH_CONTRACT")
    cfg.ipfs_gateway = os.getenv("IPFS_GATEWAY")