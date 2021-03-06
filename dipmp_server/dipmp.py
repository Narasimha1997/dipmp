import requests
import web3 as w
from web3.middleware import geth_poa_middleware
import logging

from env import Config

logging = logging.getLogger("MainLogger")

ABI = [{
    "inputs": [],
    "stateMutability": "nonpayable",
    "type": "constructor"
}, {
    "inputs": [{
        "internalType": "string",
        "name": "name",
        "type": "string"
    }, {
        "internalType": "uint24",
        "name": "version",
        "type": "uint24"
    }],
    "name":
    "checkExists",
    "outputs": [{
        "internalType": "bool",
        "name": "",
        "type": "bool"
    }],
    "stateMutability":
    "view",
    "type":
    "function"
}, {
    "inputs": [{
        "internalType": "string",
        "name": "name",
        "type": "string"
    }, {
        "internalType": "uint24",
        "name": "version",
        "type": "uint24"
    }, {
        "internalType": "string",
        "name": "IPFSHash",
        "type": "string"
    }, {
        "internalType": "string",
        "name": "idata",
        "type": "string"
    }],
    "name":
    "createIdentity",
    "outputs": [{
        "internalType": "bool",
        "name": "",
        "type": "bool"
    }],
    "stateMutability":
    "nonpayable",
    "type":
    "function"
}, {
    "inputs": [{
        "internalType": "string",
        "name": "name",
        "type": "string"
    }],
    "name":
    "getAllIdentities",
    "outputs": [{
        "components": [{
            "internalType": "string",
            "name": "IPFSHash",
            "type": "string"
        }, {
            "internalType": "string",
            "name": "idata",
            "type": "string"
        }, {
            "internalType": "address",
            "name": "by",
            "type": "address"
        }, {
            "internalType": "uint24",
            "name": "version",
            "type": "uint24"
        }],
        "internalType":
        "struct DIPMP.PackageIdentity[]",
        "name":
        "",
        "type":
        "tuple[]"
    }],
    "stateMutability":
    "view",
    "type":
    "function"
}]

GETTER = "getAllIdentities"

TEMPLATE = """
<!DOCTYPE html>
<html>
  <body>
    <h1>Links for {}</h1>
    {}
  </body>
</html>
"""


# unpack 24-bit semantic version representation to string
def decode_version(version):
    c1 = (version >> 16) & 0xff
    c2 = (version >> 8) & 0xff
    c3 = version & 0xff

    return "{}.{}.{}".format(c1, c2, c3)


# get the contract instance from gateway and address
def get_contract_instance(gateway: str, address: str):
    connection = w.Web3(w.Web3.HTTPProvider(gateway))
    connection.middleware_onion.inject(geth_poa_middleware, layer=0)
    contract = connection.eth.contract(address, abi=ABI)
    return contract


# get the package details
def get_package_details(env: Config, package_name: str, address: str) -> dict:
    try:
        contract = get_contract_instance(env.eth_gateway, address)
        fn = contract.get_function_by_name(GETTER)
        return fn(package_name).call()

    except Exception as e:
        logging.error("contract error" + str(e))
        return None


# the main function that will be called from the API
def resolve_package(env: Config, name: str, address: str) -> str:

    logging.info("resolving package name " + name)
    packages = get_package_details(env, name, address)
    anchors = []

    # generate HTML 5 doc
    for package in packages:
        # TODO: parse metadata string
        ipfs, meta, _, v = package
        v = decode_version(v)
        ipfs_uri = "{}/serve/{}/{}".format(env.host_url, ipfs, meta)
        anchor = '<a href="{}">{}</a></br>'.format(ipfs_uri, meta)
        anchors.append(anchor)

    data = TEMPLATE.format(name, "\n".join(anchors))

    return data


def yield_chunks_from_ipfs(config: Config, hash: str):
    url = "{}/{}".format(config.ipfs_gateway, hash)
    # create a streaming connection
    getter = requests.get(url, stream=True)
    for chunk in getter.iter_content(chunk_size=8192):
        yield chunk