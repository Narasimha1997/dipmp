### dipmp_pkg
This is the client tool for pushing packages to decentralized package registry. Check the parent repository [here](https://github.com/Narasimha1997/dipmp).

#### To install
```
cd dipmp_pkg
pip3 install -e .
```

Once installed, the command `dipmp` will be available. Run `dipmp` from command line:
```
$dipmp
```
You should see the following output:
```
usage: dipmp [-h] [--config CONFIG] wheel
dipmp: error: the following arguments are required: wheel
```

### Configuration
`dipmp_pkg` requires the following configuration file to be written in TOML
```
[chain]
address="0x<address of the contract used for storing the index>"
private_key="<private key of the signer account>"
gateway="<gateway used for interacting with the ethereum blockchain>"
account="<address of the signer account>"

[ipfs]
url="https://api.pinata.cloud/pinning/pinFileToIPFS"
key="<api key of the pinata gateway>"
secret="<api secret of the pinata gateway>"
```

### Pushing packages
Once you have a wheel of the python package available, you can use `dipmp` to push the wheel to the registry.
```
dipmp wheel_file.whl
```
The above command will look for `config.toml` in the current working directory, to manually provide the path:
```
dipmp --config=<config.toml file path> wheel_file.whl
```
