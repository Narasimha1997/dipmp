import os

class Config:
    eth_gateway = ""
    ipfs_gateway = ""
    host_url=""

def init_env() -> Config:
    cfg = Config()
    cfg.eth_gateway = os.getenv("ETH_GATEWAY")
    cfg.ipfs_gateway = os.getenv("IPFS_GATEWAY")
    cfg.host_url = os.getenv("HOST_URL")
    return cfg
