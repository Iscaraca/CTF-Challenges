import json
from web3 import Web3
import re
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ANVIL_URL = "http://testnet:8545"
CALLER = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

def connect_to_anvil():
    # Connect to anvil network
    web3_client = Web3(Web3.HTTPProvider(ANVIL_URL))
    if web3_client.is_connected():
        logger.info("Connected to Anvil")
    else:
        logger.error("Failed to connect to Anvil")
        raise RuntimeError("Failed to connect to Anvil")

    return web3_client


def init_setup_contract(web3_client):
    # Initialise setup contract
    with open("/contracts/out/Setup.sol/Setup.json", 'r') as f:
        contract_data = json.load(f)
    abi = contract_data["abi"]

    with open('/output.log', 'r') as f:
        content = f.read()
    pattern = r'Setup contract deployed to:\s+(\b0x[A-Fa-f0-9]{40}\b)'
    match = re.search(pattern, content)
    if match:
        setup_contract_address = match.group(1)
        logger.info(f'Setup contract address: {setup_contract_address}')
    else:
        logger.error('Setup contract address not found.')

    setup_contract = web3_client.eth.contract(address=setup_contract_address, abi=abi)

    return setup_contract


def call_check_password(setup_contract, password):
    # Call checkPassword function
    passwordEncoded = '0x' + bytes(password.ljust(32, '\0'), 'utf-8').hex()

    # Get result and gas used
    try:
        gas = setup_contract.functions.checkPassword(passwordEncoded).estimate_gas()
        output = setup_contract.functions.checkPassword(passwordEncoded).call()
        logger.info(f'Gas used: {gas}')
        logger.info(f'Check password result: {output}')
    except Exception as e:
        logger.error(f'Error calling checkPassword: {e}')

    # Return debugging information
    return {
        "output": output,
        "setup_contract_address": setup_contract.address,
        "setup_contract_bytecode": "0x608060405234801561001057600080fd5b5060405161027838038061027883398101604081905261002f9161007c565b600080546001600160a01b039384166001600160a01b031991821617909155600180549290931691161790556100af565b80516001600160a01b038116811461007757600080fd5b919050565b6000806040838503121561008f57600080fd5b61009883610060565b91506100a660208401610060565b90509250929050565b6101ba806100be6000396000f3fe608060405234801561001057600080fd5b506004361061002b5760003560e01c8063410eee0214610030575b600080fd5b61004361003e366004610115565b610057565b604051901515815260200160405180910390f35b6000805460015460408051602481018690526001600160a01b0392831660448083019190915282518083039091018152606490910182526020810180516001600160e01b0316635449534360e01b17905290518493849316916100b99161012e565b6000604051808303816000865af19150503d80600081146100f6576040519150601f19603f3d011682016040523d82523d6000602084013e6100fb565b606091505b50915091508061010a9061015d565b600114949350505050565b60006020828403121561012757600080fd5b5035919050565b6000825160005b8181101561014f5760208186018101518583015201610135565b506000920191825250919050565b8051602080830151919081101561017e576000198160200360031b1b821691505b5091905056fea2646970667358221220e0f8333be083b807f8951d4868a6231b41254b2f6157a9fb62eff1bcefafd84e64736f6c63430008130033",
        "adminpanel_contract_bytecode": "0x60858060093d393df35f358060d81c64544953437b148160801b60f81c607d1401600214610022575f5ffd5b6004356098636b35340a6060526020606020901b186024356366fbf07e60205260205f6004603c845af4505f515f5f5b82821a85831a14610070575b9060010180600d146100785790610052565b60010161005e565b81600d1460405260206040f3",
        "secret_contract_bytecode": "0xREDACTED",
        "gas": gas
    }