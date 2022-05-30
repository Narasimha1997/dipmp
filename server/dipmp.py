from distutils.command.config import config
import web3 as w
from web3.middleware import geth_poa_middleware
import logging

from .env import Config

logging = logging.getLogger("MainLogger")

ABI = [{
    'inputs': [],
    'stateMutability': 'nonpayable',
    'type': 'constructor'
}, {
    'inputs': [{
        'internalType': 'string',
        'name': 'name',
        'type': 'string'
    }, {
        'internalType': 'string',
        'name': 'version',
        'type': 'string'
    }],
    'name':
    'checkExists',
    'outputs': [{
        'internalType': 'bool',
        'name': '',
        'type': 'bool'
    }],
    'stateMutability':
    'view',
    'type':
    'function'
}, {
    'inputs': [{
        'internalType': 'string',
        'name': 'name',
        'type': 'string'
    }, {
        'internalType': 'string',
        'name': 'version',
        'type': 'string'
    }, {
        'internalType': 'string',
        'name': 'IPFSHash',
        'type': 'string'
    }, {
        'internalType': 'string',
        'name': 'idata',
        'type': 'string'
    }],
    'name':
    'createIdentity',
    'outputs': [{
        'internalType': 'bool',
        'name': '',
        'type': 'bool'
    }],
    'stateMutability':
    'nonpayable',
    'type':
    'function'
}, {
    'inputs': [{
        'internalType': 'string',
        'name': 'name',
        'type': 'string'
    }, {
        'internalType': 'string',
        'name': 'version',
        'type': 'string'
    }],
    'name':
    'getIdentity',
    'outputs': [{
        'components': [{
            'internalType': 'bool',
            'name': '_entry',
            'type': 'bool'
        }, {
            'internalType': 'string',
            'name': 'IPFSHash',
            'type': 'string'
        }, {
            'internalType': 'string',
            'name': 'idata',
            'type': 'string'
        }, {
            'internalType': 'address',
            'name': 'by',
            'type': 'address'
        }],
        'internalType':
        'struct DIPMP.PackageIdentity',
        'name':
        '',
        'type':
        'tuple'
    }],
    'stateMutability':
    'view',
    'type':
    'function'
}]

GETTER = "getIdentity"

# unpack 24-bit semantic version representation to string
def decode_version(version):
    c1 = version & 0xff0000
    c2 = version & 0x00ff00
    c3 = version & 0x0000ff

    return  "{:02d}.{:02d}.{:02d}".format(c1, c2, c3)

# get the contract instance from gateway and address
def get_contract_instance(gateway: str, address: str):
    connection = w.Web3(w.Web3.HTTPProvider(gateway))
    connection.middleware_onion.inject(geth_poa_middleware, layer=0)
    contract = connection.eth.contract(address, abi=ABI)
    return contract

# get the package details
def get_package_details(env: Config, package_name: str, version: str) -> dict:
    try:
        contract = get_contract_instance(env.eth_gateway, env.eth_contract)
        fn = contract.get_function_by_name(GETTER)
        return fn.call(package_name, version)

    except Exception as e:
        logging.error("contract error" + str(e))
        return None

# the main function that will be called from the API
def resolve_package(env: Config):
    pass