// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {

    // this will get initialized to 0
    uint256 favNum;

    struct People {
        uint256 favNum;
        string name;
    }

    People[] public people;
    mapping(string => uint256) public nameToFavNum;

     //People public person = People({ favNum: 2, name: "Abhijit"});

    function store (uint256 _favNum) public {
        favNum = _favNum;
    }

    // pure and view
    function retrieve() public view returns(uint256) {
        return favNum;
    }

    function addPerson(uint256 _favNum, string memory _name) public {
        people.push( People( _favNum, _name ) );
        nameToFavNum[ _name] = _favNum;
    }
}