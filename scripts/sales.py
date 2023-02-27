# Display the events available for sale

import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
import psycopg2

# Setup

load_dotenv()
st.set_page_config(layout="wide")
# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# Set the contract address (this is the address of the deployed contract)
owner_address = os.getenv("SMART_CONTRACT_OWNER_ADDRESS")
@st.cache(allow_output_mutation=True)


def load_contract():
    '''Load the Tickets smartcontract 
       to register tickets'''
    # Load the contract ABI
    with open(Path("./compiled/tickets_abi.json")) as f:
        contract_abi = json.load(f)


    # Get the contract
    contract = w3.eth.contract(
        address=owner_address,
        abi=contract_abi
    )

    return contract

def load_events():
    '''Retrieve the events collected in the events table 
       and display in streamlit web page'''

    # Connect to db
    host = os.getenv("DBHOST")
    db_name = os.getenv("DBNAME")
    db_user = os.getenv("DBUSER")
    db_password = os.getenv("DBPASSWORD")
    conn = psycopg2.connect(host=host, database=db_name, user=db_user, password=db_password)

    # Open a cursor to perform DB operations
    cur = conn.cursor()

    # Query the database and obtain data as a dataframe
    cur.execute("SELECT * FROM nftix.events;")
    df = pd.DataFrame(
        cur.fetchall(), 
        columns=[
            "event_id", 
            "event_name", 
            "event_date", 
            "venue", 
            "tkt_price_aud", 
            "total_no_tkts", 
            "tkts_remaining"
        ]
    )

    # Close connection
    cur.close()
    conn.close()
    return df

def display_events(events_df):
    '''Display available events in a table and allow user to buy'''
    cols = st.columns((2, 1, 1, 1, 1))
    col_headings = ["Event", "Date", "Venue", "Remaining Tickets", "Action"]
    for col, heading in zip(cols, col_headings):
        col.write(f"##### {heading}")
    st.markdown("---")
    for index, row in events_df.iterrows():
        col1, col2, col3, col4, col5 = st.columns((2, 1, 1, 1, 1))
        col1.write(row["event_name"])
        col2.write(row["event_date"])
        col3.write(row["venue"])
        col4.write(row["tkts_remaining"])
        button_phold = col5.empty() # Create a placeholder
        buy = button_phold.button("Buy", key=row["event_id"])
        if buy:
            # button_phold.empty()
            return row["event_id"]

def buy(contract, eventId, buyerName, buyerAddress):
    '''Mint a new block for a ticket purchase'''
    tx_hash = contract.functions.registerTicket(
        eventId,
        buyerName,
        buyerAddress
    ).transact({"from": owner_address, "gas": 100000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return dict(receipt)

# Entry point
st.title("NFTix - Anti-scalping event ticketing system")
st.markdown("## Available events")

events_df = load_events()
event_id = display_events(events_df)
tickets_contract = load_contract()

if event_id:
    buyerName = "Mel Trump"
    buyerAddress = "0x8fee7A777cCA7E86Cdfb4531186a4A71Fa3f58B8"
    tokenId = buy(tickets_contract, event_id, buyerName, buyerAddress)
    st.write(f"Returned token: {tokenId}")

#     buyerName = "Eric Trump"
#     buyerAddress = "0x0D110FcfE2cF010D0086756C953eD355b117197B"
#     tokenId = buy(tickets_contract, 5, buyerName, buyerAddress)
#     st.write(f"Returned token: {tokenId}")
# else:
#     st.write("No tokens returned")