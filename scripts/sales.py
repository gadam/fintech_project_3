#---------------------------------#
# Display the events available    # 
#   for sale and transact a sale  #
#                                 #
# By Fintech Project Group 4:     #
#   Guy Adam                      #
#   Sreeni Patnaik                #
#   Venkata Nagothi               #
#---------------------------------#

import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
import psycopg2

#---------------------------------#
# Setup                           #
#---------------------------------#
load_dotenv()

# Get DB config
host = os.getenv("DBHOST")
db_name = os.getenv("DBNAME")
db_user = os.getenv("DBUSER")
db_password = os.getenv("DBPASSWORD")

st.set_page_config(layout="wide")

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# Set the contract address (this is the address of the deployed contract)
# Get a list of all available accounts from Ganache
#  and use the first account as contract owner address
accounts = w3.eth.accounts
owner_address = accounts[0]

# @st.cache(allow_output_mutation=True)
# @st.cache_resource

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
        address=owner_address,
        abi=contract_abi
    )

    return contract

#---------------------------------#
# Retrieve events list from db    #
# and update balance              #
#---------------------------------#
def load_events():
    '''Retrieve the events collected in the events table 
       and display in streamlit web page'''

    # Connect to db
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
            "total_no_of_tkts", 
            "tkts_remaining"
        ]
    )

    # Close connection
    cur.close()
    conn.close()
    return df

def update_event(event_id, quantity, tx_hash):
    '''Update the remaining tickets balance of
       event record in `events` table
       and record a sale in the `event_sales` table'''
    # Connect to db
    conn = psycopg2.connect(host=host, database=db_name, user=db_user, password=db_password)

    # Open a cursor to perform DB operations
    cur = conn.cursor()

    # Get the current ticket balance for the event and update it
    sql = "SELECT tkts_remaining FROM nftix.events WHERE event_id = %s;"
    cur.execute(sql, (event_id,))
    ticket_balance = cur.fetchone()[0]
    ticket_balance -= quantity
    if ticket_balance < 0:
        ticket_balance = 0
    sql = "UPDATE nftix.events SET tkts_remaining = %s WHERE event_id = %s;"
    cur.execute(sql, (ticket_balance, event_id))
    sql = "INSERT INTO nftix.events_sales (event_id, contract_address) VALUES (%s, %s)"
    cur.execute(sql, (event_id, tx_hash))
    conn.commit()
    # Close connection
    cur.close()
    conn.close()


#---------------------------------#
# Display list of events for sale #
#---------------------------------#
def display_events(events_df):
    '''Display available events in a table and allow user to buy'''

    st.markdown("## Available events")
    display_events_df = pd.DataFrame()
    display_events_df["Event"] = events_df["event_name"]
    display_events_df["Date"] = events_df["event_date"]
    display_events_df["Venue"] = events_df["venue"]
    display_events_df["Price"] = events_df["tkt_price_aud"]
    display_events_df["Tickets_Available"] = events_df["tkts_remaining"]
    st.dataframe(display_events_df, use_container_width=True)


#---------------------------------#
# Transact the sale               #
#---------------------------------#
def buy(contract, events_df):
    '''Capture buyer name and address and
       Mint a new block for a ticket purchase'''
    with st.sidebar:
            
        with st.form("buyer_details"):
            st.markdown("## Buy tickets for:")
            selection = st.selectbox(
                "### Tickets for", 
                options=list(events_df["event_name"]),
                key="event_selector"
            )
            quantity = st.number_input("Quantity:", min_value=1)
            buyer_name = st.text_input("Name:")
            buyer_address = st.selectbox("Wallet account address:", accounts[1:])
            if  st.form_submit_button("Purchase ticket", type="primary"):
                # Calculate price
                cost = int(events_df.loc[events_df["event_name"]==selection]["tkt_price_aud"])  * quantity
                event_id = int(events_df.loc[events_df["event_name"]==selection]["event_id"])

                # Mint a new block for the transaction
                tx_hash = contract.functions.registerTicket(
                    event_id,
                    buyer_name,
                    buyer_address, 
                    quantity
                ).transact({"from": owner_address, "gas": 100000})
                tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

                # Display receipt
                success_message = f"Buyer: {buyer_name}\nWallet: {buyer_address}\nPurchased: {quantity}\nEvent: {selection}\nTotal: ${cost}\nTransaction hash: {tx_hash.hex()}"
                st.success(success_message)
                # Update `events` table with remaining tickets balance
                update_event(event_id, quantity, tx_hash)
                return tx_receipt
            else:
                return False
    

#---------------------------------#
# Main entry point                #
#---------------------------------#
st.title("NFTix - Anti-scalping event ticketing system")

# Retrieve and display the events from the events table
events_df = load_events()
display_events(events_df)

# Prepare a smartcontract to record the sale in a ledger
tickets_contract = load_contract()

# User has chosen to buy tickets for an event
tx_receipt = buy(tickets_contract, events_df)

