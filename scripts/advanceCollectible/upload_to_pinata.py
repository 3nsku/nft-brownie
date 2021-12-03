import os
from pathlib import Path
import requests

PINATA_BASE_URL = "https://api.pinata.cloud"
PIN_FILE_TO_IPFS_ENDPOINT = "/pinning/pinFileToIPFS"

filepath = "./img/shiba-inu.png"
filename = filepath.split("/")[-1:][0]

headers = {
    "pinata_api_key": os.getenv("PINATA_API_PUBLIC_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_API_SECRET_KEY"),
}


def main():
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()

        response = requests.post(
            PINATA_BASE_URL + PIN_FILE_TO_IPFS_ENDPOINT,
            files={"file": (filename, image_binary)},
            headers=headers,
        )
        print(response.json())
