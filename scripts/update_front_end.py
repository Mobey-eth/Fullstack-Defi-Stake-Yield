from scripts.deploy import update_front_end
from scripts.heplful_scripts import get_account, get_contract
from brownie import TokenFarm


def to_add_allowed_tokens():
    account = get_account()
    token_farm_contract = TokenFarm[-1]
    weth_token = get_contract("weth_token")
    fau_token = get_contract("fau_token")
    dict_of_allowed_tokens = {
        fau_token: get_contract("dai_usd_price_feed"),
        weth_token: get_contract("eth_usd_price_feed"),
    }

    for token in dict_of_allowed_tokens:
        add_tx = token_farm_contract.addAllowedTokens(token.address, {"from": account})
        add_tx.wait(1)
        set_tx = token_farm_contract.setPriceFeedContract(
            token.address, dict_of_allowed_tokens[token], {"from": account}
        )
        set_tx.wait(1)


def update_my_frontend():
    update_front_end()


def main():
    to_add_allowed_tokens()
