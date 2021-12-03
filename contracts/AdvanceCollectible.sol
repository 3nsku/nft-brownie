// An NFT Contract
// Where the tokenURI can be one of 3 different dogs
// Randomly selected

// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvanceCollectible is ERC721, VRFConsumerBase {
    uint256 public fee;
    bytes32 public keyHash;
    uint256 public tokenCounter;
    enum BreedType {
        PUG,
        SHIBA_INU,
        ST_BERNARD
    }
    mapping(uint256 => BreedType) public tokenIdToBreed;
    mapping(bytes32 => address) public requestIdToSender;

    event requestedCollectible(bytes32 indexed requestId, address requester);
    event breedAssigned(uint256 indexed tokenId, BreedType breed);

    constructor(
        address _vrfCordinator,
        address _linkToken,
        uint256 _fee,
        bytes32 _keyHash
    )
        public
        VRFConsumerBase(_vrfCordinator, _linkToken)
        ERC721("Dogie", "DOG")
    {
        tokenCounter = 0;
        fee = _fee;
        keyHash = _keyHash;
    }

    function createCollectible() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyHash, fee);
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomNumber)
        internal
        override
    {
        BreedType breed = BreedType(_randomNumber % 3);
        tokenIdToBreed[tokenCounter] = breed;
        _safeMint(requestIdToSender[_requestId], tokenCounter);
        emit breedAssigned(tokenCounter, breed);
        tokenCounter += 1;
    }

    function setTokenURI(uint256 _tokenID, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), _tokenID),
            "ERC721: The caller is not owner nor approved!"
        );
        _setTokenURI(_tokenID, _tokenURI);
    }
}
