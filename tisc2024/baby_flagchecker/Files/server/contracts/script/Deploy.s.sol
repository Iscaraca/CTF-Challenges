// SPDX-License-Identifier: Unlicense
pragma solidity 0.8.19;

import "foundry-huff/HuffDeployer.sol";
import "forge-std/Script.sol";
import { Setup } from "../src/Setup.sol";

interface AdminPanel {
}

interface Secret {
}

contract Deploy is Script {
  function run() public {
    // Deploy both AdminPanel and Secret
    AdminPanel adminPanel;
    adminPanel = AdminPanel(HuffDeployer.broadcast("AdminPanel"));
    console2.log("AdminPanel contract deployed to: ", address(adminPanel));

    Secret secret;
    secret = Secret(HuffDeployer.broadcast("Secret"));
    console2.log("Secret contract deployed to: ", address(secret));

    // Deploy Setup contract
    uint256 deployerPrivateKey = DEPLOYER_PRIVATE_KEY;
    vm.startBroadcast(deployerPrivateKey);
    Setup setup = new Setup(address(adminPanel), address(secret));
    console2.log("Setup contract deployed to: ", address(setup));
    vm.stopBroadcast();
  }
}
