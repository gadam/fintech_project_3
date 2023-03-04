#--------------------------#
# Retrive blockchain data
#--------------------------#

import os
import json
import pandas as pd
from web3 import Web3 
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

#---------------------------------#
# Setup                           #
#---------------------------------#
load_dotenv()
st.set_page_config(layout="wide", page_title="NFT Event Ticketing", page_icon=":ticket:")

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# Set the contract address (this is the address of the deployed contract)
# Get a list of all available accounts from Ganache
#  and use the first account as contract owner address
accounts = w3.eth.accounts
contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
owner_address = accounts[0]

#---------------------------------#
# Load contract in preparation for#
#   sale                          #
#---------------------------------#
def load_contract():
    '''Load the `Tickets` smartcontract 
       to register tickets'''
    # Load the contract ABI
    with open(Path("./compiled/tickets_abi.json")) as f:
        contract_abi = json.load(f)    

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract

#---------------------------------#
# Main entry point                #
#---------------------------------#
st.title("NFTix - Anti-Scalping Blockchain-Based Event Ticketing System")
st.header("Tickets on the Blockchain")

contract = load_contract()

# Get number of tokens available
total_token_supply = contract.functions.totalSupply().call()
if total_token_supply > 0:
    df = pd.DataFrame(
         columns=[
            "Event_Id", 
            "Buyer_Name", 
            "Buyer_Address", 
            "Quantity"
        ],
    )
    for tokenId in range(total_token_supply):
        df2 = pd.DataFrame(
            {
                "Event_Id": [contract.functions.getEventId(tokenId).call()],
                "Buyer_Name": [contract.functions.getBuyerName(tokenId).call()],
                "Buyer_Address": [contract.functions.getBuyerAddress(tokenId).call()],
                "Quantity": [contract.functions.getQuantity(tokenId).call()]
            }
        )
        df = df.append(df2)
    st.dataframe(df, use_container_width=True)
else:
    st.write("No tickets have been sold yet!")