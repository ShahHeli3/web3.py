//SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract SimpleStorage {

    // this will get initialized to 0!
    uint256 favoriteNumber;
    bool favoriteBool;

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }
}
