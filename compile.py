import json

from solcx import install_solc, compile_standard

# read the contract
with open("./SimpleStorage.sol", "r") as file:
    contract_file = file.read()

# install the solidity version before compiling
install_solc('0.8.0')

# compile the solidity contract
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "SimpleStorage.sol": {"content": contract_file}
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ['abi', 'metadata', 'evm.bytecode', 'evm.sourceMap']
                }
            }
        }
    },
    solc_version='0.8.0'
)

# store the compiled contract in another file
with open("compiled_contract.json", "w") as file:
    json.dump(compiled_sol, file)
