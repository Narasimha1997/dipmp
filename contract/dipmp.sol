// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DIPMP {

    // represents a stored package
    struct PackageIdentity {
        bool _entry;
        string IPFSHash;
        string idata;
    }

    // maps (package => (version => identity))
    mapping(string => mapping(string => PackageIdentity)) packages;

    // we don't have to do anything while deployment
    constructor() {}

    // creates a new mapping
    function createIdentity(string memory name, string memory version, string memory IPFSHash, string memory idata) external returns(bool) {
        require(!packages[name][version]._entry, "package with given (name, version) already exists");
        PackageIdentity memory identity;
        identity.idata = idata;
        identity.IPFSHash = IPFSHash;
        identity._entry = true;

        packages[name][version] = identity;

        return true;
    }

    // get the identity details
    function getIdentity(string memory name, string memory version) external view returns(PackageIdentity memory) {
        require(packages[name][version]._entry, "package with given (name, version) does not exist");
        return packages[name][version];
    }

    // check if the identity exists
    function checkExists(string memory name, string memory version) external view returns(bool) {
        return packages[name][version]._entry;
    }
}