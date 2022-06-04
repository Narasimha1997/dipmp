import argparse
from distutils.command.config import config
import toml
import requests
import os
from pprint import pprint
import json

import web3 as w
from web3.middleware import geth_poa_middleware

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

CHECK_FUNCTION = "checkExists"
CREATE_FUNCTION = "createIdentity"

parser = argparse.ArgumentParser(
    description="This is the client tool for dipmp - decentralized, immutable package manager for python."
)

parser.add_argument("--config", type=str, help="path of the config toml file to use", default='./config.toml')
parser.add_argument("wheel", type=str, help="wheel file path to upload")

def exit_with_code(msg: str, code: int):
    print('Error: ', msg, code)
    os._exit(code)

def load_config(path: str) -> dict:
    if not os.path.exists(path):
        exit_with_code(f'config file {path} not found', -1)
    
    return toml.load(open(path))

def create_contract_connection(gateway: str, address: str):
    try:
        connection = w.Web3(w.Web3.HTTPProvider(gateway))
        connection.middleware_onion.inject(geth_poa_middleware, layer=0)
        contract = connection.eth.contract(address, abi=ABI)
        return contract, connection
    except Exception as e:
        exit_with_code(f'failed to find contract at address: {address}, error: {e}', -2)


def check_exists(contract, name: str, version: int) -> bool:
    try:
        fn = contract.get_function_by_name(CHECK_FUNCTION)
        return fn(name, version).call()
    except Exception as e:
        exit_with_code(f'failed to check for package {name}, error: {e}', -3)


def create_entry(connection: w.Web3, contract, name: str, version: int, i_name: str, hash: str, config: dict):
    try:
        user_address = config['chain']['account']
        fn = contract.get_function_by_name(CREATE_FUNCTION)
        tx = fn(name, version, hash, i_name).buildTransaction({"nonce": connection.eth.getTransactionCount(user_address)})

        signed_tx = connection.eth.account.signTransaction(tx, private_key=config['chain']['private_key'])
        tx_hash = connection.eth.sendRawTransaction(signed_tx.rawTransaction)

        tx_receipt = connection.eth.wait_for_transaction_receipt(tx_hash)
        pprint(tx_receipt)

    except Exception as e:
        exit_with_code(f'failed to create index for package: {name}, ipfs_hash: {hash}, error: {e}', -4)


def parse_wheel(file_name: str):

    if not os.path.exists(file_name):
        exit_with_code(f'file {file_name} does not exit', -5)
    
    file_name = file_name.split("/")[-1]

    if not file_name.endswith('.whl'):
        exit_with_code(f'file {file_name} is not a python package wheel', -6)
    # get name, version etc
    splits = file_name.split("-")
    version = None
    package_name = ""

    for item in splits:
        # all are numerics?
        version_splits = item.split(".")
        if len(version_splits) == 3:
            # most probably this is the version
            for x in version_splits:
                if not x.isnumeric():
                    break
            else:
                version = version_splits
                break
        if not version:
            package_name += item
    
    if not version:
        exit_with_code(f'no version found in the file {file_name}')
    # replace all '_' to '-' in package name
    package_name = package_name.replace("_", "-")
    # convert version to 24-bit representation
    v = 0
    for idx, split in enumerate(version):
        v = v | (int(split) << (24 - (idx + 1) * 8)) 
    
    return (package_name, v, file_name)


def upload_to_pinata(file_name: str, config: dict):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
            'pinata_api_key': config['ipfs']['key'],
            'pinata_secret_api_key': config['ipfs']['secret']
        }

        f_name = file_name.split("/")[-1]
        file_data = [
            ('pinataMetadata', (None, json.dumps({"name": f_name}))),
            ('file', (f_name, open(file_name, 'rb')))
        ]

        request = requests.Request('POST', config['ipfs']['url'], headers=headers, files=file_data).prepare()
        response = requests.Session().send(request)
        
        # print response
        print(f'uploaded to IPFS - {response.json()}')
        return response.json()['IpfsHash']
    except Exception as e:
        exit_with_code(f'ipfs push error: {e}', -7)


def main():
    args = parser.parse_args()
    config = load_config(args.config)
    package, version, iname = parse_wheel(args.wheel)

    contract, connection = create_contract_connection(config['chain']['gateway'], config['chain']['address'])
    
    # check if exists
    if check_exists(contract, package, version):
        exit_with_code(f'package with name {package} already exists.', -8)
    
    # push the index:
    ipfs_hash = upload_to_pinata(args.wheel, config)

    # push to index
    create_entry(connection, contract, package, version, iname, ipfs_hash, config)