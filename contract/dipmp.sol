// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DIPMP {

    // represents a stored package
    struct PackageIdentity {
        string IPFSHash;
        string idata;
        address by;
        uint32 version;
    }

    // maps (package => (version => identity))
    mapping(string => mapping(uint8 => PackageIdentity)) packages;

    // stores mapping counts (allow only 256 versions to be present)
    mapping(string => uint8) version_counts;

    // we don't have to do anything while deployment
    constructor() {}

    // check if the package with given name and version exists
    function checkExists(string memory name, uint32 version) external view returns(bool) {
        uint8 count = version_counts[name];
        for (uint8 i = 0; i < count; i++) {
            if (packages[name][i].version == version) {
                return true;
            }
        }

        return false;
    }

    // creates a new mapping
    function createIdentity(string memory name, uint32 version, string memory IPFSHash, string memory idata) external returns(bool) {
        require(!this.checkExists(name, version), "package with given name and version exists");

        // create a new package entry
        PackageIdentity memory identity;
        identity.by = msg.sender;
        identity.IPFSHash = IPFSHash;
        identity.idata = idata;
        identity.version = version;

        uint8 current_counter = version_counts[name];
        packages[name][current_counter] = identity;
        version_counts[name]++;

        return true;
    }

    // get the identity details
    function getAllIdentities(string memory name) external view returns(PackageIdentity[] memory) {

        uint8 current_counter = version_counts[name];
        if (current_counter == 0) {
            return new PackageIdentity[](0);
        }

        PackageIdentity[] memory identities = new PackageIdentity[](current_counter);
        for (uint8 i = 0; i < current_counter; i++) {
            identities[i] = packages[name][i];
        }

        return identities;
    }
}