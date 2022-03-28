from brownie import accounts, config, SimpleStorage, network

def deploy_simple_storage():
    
    # this method works only for local ganache chains 
    # this takes the first address given by our local ganache-cli. 
    # we don't need to get the private key. 
    # brownie does that behind the scenes for us
    
    account = get_account()  
    simple_storage = SimpleStorage.deploy({"from": account})
    stored_value = simple_storage.retrieve()
    print(stored_value)

    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)

    # we can also create an account via encrypted command-line 
    # by running.. brownie accounts new [account_name]
    # then we provide a private key and password
    # then load it as follows
    # this is a more secure way of handling keys

    # account = accounts.load("solidity-practice-account")
    # print(account)

    # third method of adding addresses. 
    # first we set a .env file with our private key. 
    # then we add it to brownie-config. 
    # then we get the env variable
    # account = accounts.add(os.getenv("PRIVATE_KEY"))
    # print(account)

    # improvement to the third method
    # account = accounts.add(config["wallets"]["from_key"])
    # print(account)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()