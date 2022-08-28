from scripts.heplful_scripts import get_account
from brownie import interface, web3

value = web3.toWei(0.1, "ether")


def main():
    account = get_account
    weth_token_address = "0xc778417E063141139Fce010982780140Aa0cD5Ab"
    weth_token = interface.IWeth(weth_token_address)
    tx = weth_token.deposit({"from": account, "value": value})
    tx.wait(1)
