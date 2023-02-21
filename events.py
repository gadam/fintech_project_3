import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import psycopg2

load_dotenv()

# Connect to db
host = os.getenv("DBHOST")
db_name = os.getenv("DBNAME")
db_user = os.getenv("DBUSER")
db_password = os.getenv("DBPASSWORD")
db_conn = f"host={host} dbname={db_name} user={db_user} password={db_password}"
conn = psycopg2.connect(db_conn)

# Open a cursor to perform DB operations
cur = conn.cursor()

# Query the database and obtain data as python objects
cur.execute("SELECT * FROM nftix.events;")
record = cur.fetchone()
print(record)

# Close connection
cur.close()
conn.close()