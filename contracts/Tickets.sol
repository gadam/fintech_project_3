// SPDX-License-Identifier: MIT
pragma solidity ^0.5.5;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

// import "@openzeppelin/contracts/token/ERC721/ERC721Full.sol";

contract TicketToken is ERC721Full {
    constructor() public ERC721Full("EventTicketToken", "TIX") {}

    struct Ticket {
        uint256 eventId;
        string buyerName;
        address payable buyerAddress;
        uint256 quantity;
    }

    mapping(uint256 => Ticket) public eventTicket;

    // Should we consider using events?
    // event Appraisal(uint256 tokenId, uint256 appraisalValue, string reportURI);

    function registerTicket(
        // address owner,
        uint256 eventId,
        string memory buyerName,
        address payable buyerAddress,
        uint256 quantity
    ) public returns (uint256) {
        uint256 tokenId = totalSupply();
        // address owner = msg.sender;

        _mint(buyerAddress, tokenId);

        eventTicket[tokenId] = Ticket(eventId, buyerName, buyerAddress, quantity);

        return tokenId;
    }

    function getBuyerName(uint256 tokenId) public view returns (string memory) {
        return eventTicket[tokenId].buyerName;
    }

    function getBuyerAddress(uint256 tokenId) public view returns (address) {
        return eventTicket[tokenId].buyerAddress;
    }
}
