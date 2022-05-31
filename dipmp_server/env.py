import os

class Config:
    eth_gateway = ""
    eth_contract = ""
    ipfs_gateway = ""
    host_url=""

def init_env() -> Config:
    cfg = Config()
    cfg.eth_gateway = os.getenv("ETH_GATEWAY")
    cfg.eth_contract = os.getenv("ETH_CONTRACT")
    cfg.ipfs_gateway = os.getenv("IPFS_GATEWAY")
    cfg.host_url = os.getenv("HOST_URL")

    print(cfg.eth_contract, cfg.eth_gateway)

    return cfg
