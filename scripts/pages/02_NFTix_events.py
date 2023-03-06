# NFTix Streamlit app
# Imports
import streamlit as st
from dataclasses import dataclass
import datetime as datetime
import psycopg2


# Create a Record Data Class that consists of the event_name, event_date, venue, ticket_price, total_no_of_tickets, tickets_remaining
@dataclass
class Record:
    event_name: str
    event_date: datetime.datetime
    venue: str
    ticket_price: float
    total_no_of_tickets: int
    tickets_remaining: int


# Streamlit app
def main():
    # Set the page title and icon
    st.set_page_config(page_title="NFT Event Ticketing", page_icon=":ticket:")

    # Set the app title
    st.title("NFTix - Add Records for Events")

    # Get user input for event_name
    event_name = st.text_input("Event Name")

    # Get user input for event_date
    event_date = st.date_input("Event Date")

    # Get user input for venue
    venue = st.text_input("Venue")

    # Get user input for ticket_price
    ticket_price = st.number_input("Ticket Price", min_value=0.0)

    # Get user input for total_no_of_tickets
    total_no_of_tickets = st.number_input("Total Number of Tickets", min_value=0, step=1)

    # Get user input for tickets_remaining
    tickets_remaining = st.number_input("Tickets Remaining", min_value=0, step=1)

    # Create a record object with the user inputs
    new_record = Record(event_name, event_date, venue, ticket_price, total_no_of_tickets, tickets_remaining)

    # Connect to the nftix database
    conn = psycopg2.connect(host='localhost', dbname='nftix', user='postgres', port='5432', password='postgres')

    # Define the cursor object
    cur = conn.cursor()

    # Add a button to add the new record to the database
    if st.button("Add Record"):
        # insert the record into the database
        cur.execute(f"INSERT INTO nftix.events (event_name, event_date, venue, tkt_price_aud, total_no_of_tkts, tkts_remaining) VALUES (%s, %s, %s, %s, %s, %s)",
        (new_record.event_name, new_record.event_date, new_record.venue, new_record.ticket_price, new_record.total_no_of_tickets, new_record.tickets_remaining))

        # commit the changes to the database
        conn.commit()

        # Show a success message
        st.success("Record added successfully!")
        st.balloons()

    # close the cursor and database connection
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()