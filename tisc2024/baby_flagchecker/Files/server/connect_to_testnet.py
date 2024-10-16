import json
import os
import re
import logging

from web3 import Web3

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ANVIL_URL = os.environ['NETWORK_RPC_URL']
CALLER = os.environ['CALLER_ADDR']
PRIVATE_KEY = os.environ['PRIVATE_KEY']

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
    # Initialise setup contract, relies on deploy_contract
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
        "contract_address": setup_contract.address,
        "setup_contract_bytecode": os.environ['SETUP_BYTECODE'],
        "adminpanel_contract_bytecode": os.environ['ADMINPANEL_BYTECODE'],
        "secret_contract_bytecode": os.environ['SECRET_BYTECODE'],
        "gas": gas
    }