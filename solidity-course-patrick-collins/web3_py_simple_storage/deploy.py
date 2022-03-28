from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

install_solc("0.6.0")

# Compile our Solidity     

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0"
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

#get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

#for connecting to ganache
w3 =  Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/fd2264ddb335446cb4d2b7fea79f2abf"))
chain_id = 4
my_address = "0x420e6B3EC0aF152b3dB653D11A45a7d2a76fC470"
private_key = os.getenv("PRIVATE_KEY")

# create the contract in python
SimpleStorage = w3.eth.contract(abi = abi, bytecode = bytecode)

# get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# build transaction
# sign transaction
# send transaction

# building transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address, 
        "nonce": nonce
    })

# signing transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key = private_key)

# sending the signed transaction
print("Deploying Contract ...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")

# working with a contract
simple_storage = w3.eth.contract(address = tx_receipt.contractAddress, abi = abi)
print("Updating Contract ...")
print(simple_storage.functions.retrieve().call())

# making a transaction to store number
store_transaction = simple_storage.functions.store(5).buildTransaction({
    "chainId": chain_id,
    "gasPrice": w3.eth.gas_price,
    "from": my_address,
    "nonce": nonce + 1 
})

signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key = private_key)

send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

print("Updated!")
#simple_storage.functions.store(5).transact()

print(simple_storage.functions.retrieve().call())
