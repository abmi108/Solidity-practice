// SPDX-License-Identifier: MIT

pragma solidity >=0.6.6 < 0.9.0;

contract FundMe {

    mapping(address => uint256) public addressToAmountFunded;

    function fund() public payable {
        addressToAmountFunded[msg.sender] += msg.value;
        // Eth to USD conversion rate
    }

}