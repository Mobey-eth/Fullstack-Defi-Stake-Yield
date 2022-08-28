from brownie import network, exceptions
from scripts.heplful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
from scripts.deploy import deploy_token_farm_and_dapp_token
import pytest


def test_set_pricefeed_contract():
    # ARRANGE
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!!")
    account = get_account()
    non_owner = get_account(index=1)
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    # We set the pricefeed address as follows.
    pricefeed_address = get_contract("eth_usd_price_feed")
    # ACT
    token_farm.setPriceFeedContract(
        dapp_token.address, pricefeed_address, {"from": account}
    )
    # assert
    assert token_farm.tokenPriceFeedMapping(dapp_token.address) == pricefeed_address
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.setPriceFeedContract(
            dapp_token.address, pricefeed_address, {"from": non_owner}
        )


def test_stake_tokens(amount_staked):
    # ARRANGE
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!!")
    account = get_account()
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    # ACT
    dapp_token.approve(token_farm.address, amount_staked, {"from": account})
    token_farm.stakeTokens(amount_staked, dapp_token.address, {"from": account})
    # ASSERT
    assert (
        token_farm.stakingBalance(dapp_token.address, account.address) == amount_staked
    )
    assert token_farm.uniqueTokensStaked(account.address) == 1
    assert token_farm.stakers(0) == account.address
    return token_farm, dapp_token


def test_issue_tokens(amount_staked):
    # ARRANGE
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!!")
    account = get_account()
    token_farm, dapp_token = test_stake_tokens(amount_staked)
    starting_balance = dapp_token.balanceOf(account.address)
    # ACT
    token_farm.issueTokens({"from": account})
    """
        We are staking 1DAPP token == 1ETH in price
        so we sgould get 2,000 DAPP tokens in reward
        since the price of ETH is $2000... 
    """
    # ASSERT
    assert (
        dapp_token.balanceOf(account.address)
        == starting_balance + 2000000000000000000000
    )


# FINISH THE REST OF THE TESTS!!
