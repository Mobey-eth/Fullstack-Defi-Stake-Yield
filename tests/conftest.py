import pytest
from brownie import web3


@pytest.fixture
def amount_staked():
    return web3.toWei(1, "ether")
