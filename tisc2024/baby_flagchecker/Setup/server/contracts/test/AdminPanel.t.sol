// SPDX-License-Identifier: Unlicense
pragma solidity 0.8.19;

import "foundry-huff/HuffDeployer.sol";
import "forge-std/Test.sol";
import "forge-std/console.sol";
import "../src/Setup.sol";

contract AdminPanelTest is Test {
    AdminPanel public adminPanel;
    Secret public secret;
    Setup public setupObj;
    
    /// @dev Setup the testing environment.
    function setUp() public {
        adminPanel = AdminPanel(HuffDeployer.deploy("AdminPanel"));
        secret = Secret(HuffDeployer.deploy("Secret"));
        setupObj = new Setup(address(adminPanel), address(secret));
    }

    /// @dev Debugging.
    function testCheckPassword(uint256 value) public {
        setupObj.checkPassword("{g@s_Ga5_94S}");
    }
}