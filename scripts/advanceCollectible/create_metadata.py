from brownie import AdvanceCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.metadata_template import metadata_template
from pathlib import Path
import requests
import json
import os


def main():
    advanced_collectible = AdvanceCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} Advanced Collectibles!")

    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(
                f"Metadata file: {metadata_file_name} already created. Delete it to Ovewrite!"
            )
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An Aborable {breed} pup!"
            image_path = f"./img/{breed.lower().replace('_','-')}.png"
            image_uri = upload_to_ipfs(image_path)
            collectible_metadata["image"] = image_uri

            # create a new json file, and save inside the metadata
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            upload_to_ipfs(metadata_file_name)


def upload_to_ipfs(filepath):
    # open the image file in binary and upload it to IPFS
    with Path(filepath).open("rb") as open_file:
        image_binary = open_file.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"files": image_binary})
        ipfs_hash = response.json()["Hash"]
        # "./img/PUG.png" -> [".", "img", "PUG.png"] -> "[PUG.png]" -> "PUG.png"
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
