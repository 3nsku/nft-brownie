from scripts.helpful_scripts import (
    get_account,
    OPENSEA_URL,
    get_contract,
    fund_with_link,
)
from brownie import AdvanceCollectible, config, network


def deploy_and_create():
    account = get_account()
    advance_collectible = AdvanceCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["key_hash"],
        {"from": account},
    )
    fund_with_link(advance_collectible.address)

    creating_tx = advance_collectible.createCollectible({"from": account})
    creating_tx.wait(1)
    print("New Token Has Been Created!")
    return advance_collectible, creating_tx


def main():
    deploy_and_create()
