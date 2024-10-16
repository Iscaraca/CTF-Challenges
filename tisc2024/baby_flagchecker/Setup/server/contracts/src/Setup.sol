// SPDX-License-Identifier: Unlicense
pragma solidity 0.8.19;

import "foundry-huff/HuffDeployer.sol";
import "forge-std/Test.sol";
import "forge-std/console.sol";

contract Setup {
    address adminPanel;
    address secret;

    constructor(address adminPanelAddr, address secretAddr) {
        adminPanel = adminPanelAddr;
        secret = secretAddr;
    }

    function checkPassword(bytes32 password) public returns (bool) {
        (bool success, bytes memory returnData) = adminPanel.call(abi.encodeWithSelector(0x54495343, 
            password, secret));

        return bytes32(returnData) == 0x0000000000000000000000000000000000000000000000000000000000000001;
    }
}

interface AdminPanel {
}

interface Secret {
    function secretP1ssp00r() external returns (bytes32);
}