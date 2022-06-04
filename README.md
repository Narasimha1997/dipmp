## dipmp (decentralized, immutable package manager for python)
 A decentralized package registry for python built on top of IPFS and Ethereum - using python, solidity and pinata. dipmp provides APIs compatible with the default python package manager - pip. 

Packages are stored on IPFS p2p network (like bit-torrent) and are available globally with no single point of control, the index of these packages are stored in a smart contract deployed on ethereum blockchain. A community of developers/users can deploy their own contract to maintain their own index. Developers submit packages using `dipmp` client tool to the index by spending some gas and signing them (ECDSA) using their private keys and can be verified using the publically known wallet address. Users can download packages using `pip` by pointing them to any of the available registry servers and contract address.

### Components
1. Package server: The package server interacts with IPFS and Ethereum contracts to fetch the packages easily by providing a PIP compatible API. 
2. `dipmp-pkg`: This is the client tool used to push packages by publishers.
3. Contract: This is the smart contract code that stores the index, can be used by those who wish to deploy their own contract.

### Setup package server:
You can use the `Dockerfile` provided in the repository to build the package server. Run the following command from the project root:
```
docker build . -t dipmp-server:latest
```
Now run the container:
```
docker run --rm -ti --net=host --env="ETH_GATEWAY=https://rinkeby.infura.io/v3/22b23b601d364f999c0a7cdeb7bad4" --env="IPFS_GATEWAY=https://ipfs.io/ipfs" --env="HOST_URL=http://localhost:5000" dipmp-server:latest
```
We have to pass the `GATEWAY_URL` used to interact with the ethereum blockchain and `IPFS_GATEWAY` URL from where the packages will be fetched. `HOST_URL` is the domain name of the server.

Once the server is running, you can try pulling `dipmp-pkg` - the client tool which is hosted on decentralized web for testing purposes.
```
pip3 install dipmp-pkg --index-url=http://localhost:5000/simple/0xb9d99e1235FDA780bef7198cE2bb4321BBe8Fea6
```
The address `0xb9d99e1235FDA780bef7198cE2bb4321BBe8Fea6` points to the test contract deployed on Rinkeby. Now `pip` should be able to download and install `dipmp-pkg`.

### Client tool for pushing packages
To download and get started with the client tool checkout the README.md of the client tool [here](./dipmp_pkg/README.md).

### Deploying your own contract
You can copy `contract/dipmp.sol` to an online editor like Remix to deploy the contract with your own wallet address. Try using testnets.

### Some caveats
1. We are using pinata as of now, because the IPFS public network is unstable and the packages will be garbage collected if not pinned.
2. Packages might not be immediately available after pushing because it takes some time for the package to propagate and settle on IPFS network.
3. Package manager can be error prone, because it is not much tested yet.
4. Consider this as a POC of a decentralized package manager.

### Contributing
If you like this idea, please feel to raise issues, make PRs and suggest new features/changes.
