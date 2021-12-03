from brownie import network, AdvanceCollectible
from scripts.helpful_scripts import get_account, OPENSEA_URL, get_breed

dog_metadata_dic = {
    "PUG": "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmdryoExpgEQQQgJPoruwGJyZmz6SqV4FRTX1i73CT3iXn?filename=1-SHIBA_INU.json",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmbBnUjyHHN7Ytq9xDsYF9sucZdDJLRkWz7vnZfrjMXMxs?filename=2-ST_BERNARD.json",
}


def main():
    print(f"Working from Network {network.show_active()}")
    advance_collectible = AdvanceCollectible[-1]

    for tokenId in range(advance_collectible.tokenCounter()):
        breed = get_breed(advance_collectible.tokenIdToBreed(tokenId))
        if not advance_collectible.tokenURI(tokenId).startswith("https://"):
            print(f"Settings tokenURI of {tokenId}")
            set_tokenURI(tokenId, advance_collectible, dog_metadata_dic[breed])


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! you can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
    print("Please wait for 20 minutes and hit metadata refresh button")
