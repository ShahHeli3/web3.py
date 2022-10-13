import json
import os

from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# read the data from the compiled file
with open("./compiled_contract.json", "r") as file:
    compiled_data = file.read()

# load the json data
json_data = json.loads(compiled_data)

# get the bytecode
bytecode = json_data['contracts']['SimpleStorage.sol']['SimpleStorage']['evm']['bytecode']['object']

# get the abi
abi = json_data['contracts']['SimpleStorage.sol']['SimpleStorage']['abi']

# connect to the blockchain
# here, we will be connecting to ganache
w3 = Web3(Web3.HTTPProvider(os.getenv("PROVIDER_URL")))
chain_id = int(os.getenv("CHAIN_ID"))
my_address = os.getenv("MY_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

# create an instance of the contract
contract = w3.eth.contract(abi=abi, bytecode=bytecode)

# get the count of the transaction for nonce
nonce = w3.eth.getTransactionCount(my_address)

# build a transaction
transaction = contract.constructor().build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce
    }
)

# sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key)

# send the signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# it is a good practice to wait for the transaction receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
