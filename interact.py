import json
import os

from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# connect to the provider and blockchain
w3 = Web3(Web3.HTTPProvider(os.getenv("PROVIDER_URL")))
chain_id = int(os.getenv("CHAIN_ID"))
my_address = os.getenv("MY_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

# get the count of the transaction for nonce
nonce = w3.eth.getTransactionCount(my_address)

# get the contract abi
with open("./compiled_contract.json", "r") as file:
    compiled_data = file.read()

json_data = json.loads(compiled_data)
contract_abi = json_data['contracts']['SimpleStorage.sol']['SimpleStorage']['abi']

# get the contract address
contract_address = os.getenv("CONTRACT_ADDRESS")

# create a contract instance
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# call
initial_retrieve = contract.functions.retrieve().call()
print(f"Initial retrieve: {initial_retrieve}")

# transact (build, sign and send)
transaction = contract.functions.store(3).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce
    }
)

# sign
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# send
send_txn = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(send_txn)

# call
updated_retrieve = contract.functions.retrieve().call()
print(f"Updated retrieve: {updated_retrieve}")
