import argparse
from ast import arg
import signal
import os

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

def sig_handle():
    print('Bye! Thanks for using this tool')
    os._exit(0)

signal.signal(signal.SIGINT, sig_handle)


parser = argparse.ArgumentParser(
    description="This is the client tool for dipmp - decentralized, immutable package manager for python."
)

parser.add_argument("config", type=str, help="path of the config toml file to use", required=False, default='.')
parser.add_argument("wheel", type=str, help="wheel file path to upload", required=True)

if __name__ == "__main__":
    args = parser.parse_args()
