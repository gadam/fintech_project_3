import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import psycopg2

# Connect to db
conn = psycopg2.connect("host=localhost dbname=nftix user=postgres password=postgres")

# Open a cursor to perform DB operations
cur = conn.cursor()

# Query the database and obtain data as python objects
cur.execute("SELECT * FROM nftix.events;")
record = cur.fetchone()
print(record)

# Close connection
cur.close()
conn.close()