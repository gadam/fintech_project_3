
![NFTix_Banner](https://user-images.githubusercontent.com/112692272/223023428-74b07d70-50c6-443d-9c3b-78d04fcc4672.png)

**NFTix - Anti-scalping blockchain based event Ticketing system**

This project aims at building a resilient Non-Fungible Event ticketing application which provides ability to purchase tickets for various events on blockchain. The primary aim of the application is to prevent ticket scalping. Example - A buyer cannot purchase a bulk of tickets much in advance and later sell them off for a different (higher) price because all the purchases are blockchain based and the ownership of the tickets cannot be transferred to a different person, it is simply not possible on blockchain. 

***Technical Architecture***

The whole application architecture comprises of 5 components : A PostgreSQL Database which will store the details of all the events and receives calls from Streamlit/Python to store the details of ticket purchases. The addition of the event details, purchasing of the tickets can be done on the Streamlit front-end and the actual ticket purchasing activity on the blockchain is performed by Solidity. Ganache is used as a buyer's wallet to make successful purchases solely for this test application purpose.

The Streamlit application interacts with Python and Solidity. The Python application interacts with PostgreSQL database and the Streamlit to cater to the requests made by Streamlit to store and retreive the data to and from PostgreSQL database. When the ticket purchases are made, Streamlit interacts with Solidity and Ganache Wallets to make a successfull purchase on the blockchain. Once the ticket purchase is successful, the transaction details are pushed through to PostgreSQL database by Python.

***Data Flow***

This project uses PostgreSQL database to store events related data and transactions related to ticket purchases. We have used "psycopg2" Python module which will help Python perfrom query execution on PostgreSQL database. The database comprises of a schema called "nftix" which has two tables called "events" and "event_sales". The "event" table stored the details of all the upcoming events with their schedules, number of tickets, ticket prices and remaining tickets. The "event_sales" table stores the details of the tickets purchased including the event id and buyer's address.

## The whole application workflow :

**Event Oraganizers entering/updating the event related details**

The Event Organizers can register and login to our web application to register their Events. The details of the Events can be entered on the front-end Streamlit application and upon saving, the details will be pushed through to the PostgreSQL database in the backend. Similarly, The event details can be updated in-case of any changes to the events.

Below are the screen-shots showing how to add a new event :

Cick on "NFTix Events" on the side-ar to enter the event details.

![03_tc_01_adding_new_event_01](https://user-images.githubusercontent.com/112692272/223017198-17eb5472-7b50-4178-bcb5-5d81acfe9001.png)

Once details are entered - Click "Add Record" then the event details will be pushed to PostgreSQL database.

![03_tc_01_adding_new_event_02](https://user-images.githubusercontent.com/112692272/223017223-956c1935-6fdf-42b7-960a-7f9d31df8b51.png)

The new event details showing up in the PostgreSQL Database.

![03_tc_01_adding_new_event_03](https://user-images.githubusercontent.com/112692272/223017249-d64c1222-b3e5-4514-a25c-eddbfc507d92.png)

Retreiving the newly added Event details.

![03_tc_01_adding_new_event_04](https://user-images.githubusercontent.com/112692272/223017282-bb5d6bb6-11f0-4d31-b7c4-c0c861a0f0fc.png)


**The event participants can view the available events and purchase the tickets**

The aspiring event participants can login to see the various events and their schedules along with the available tickets and their prices on the Streamlit front-end screen. The ticket purchase can be done instantly :

On the lefthand side on the side-bar participants can choose the Event, choose the number of tickets needed for any event of interest, select a Wallet they want to use to purchase the ticket and click "purchase ticket" button then the transaction would be performed on the blockchain. To make this possible we have used Solidity (A smart contracting application) in the background which registeres the ticket purchase on the blockchain and a unique hash-value will be generated in the form of a reciept to uniquely identify the purchase. Also, for building this test application we have used Ganache Wallets a Buyer can use to purchase the tickets. A successful transaction will make a database call to store the event_id, transaction_id and Buyer's contract Address in a table called "nftix.events_sales" table.

Dependencies and script execution process

Dependencies

To ensure the code executes well, below are the pre-requisites and dependecies to be full-filled :

- A PostgreSQL database must be installed and must be running on port 5432
- Login to the PostgreSQL database and run the following script so that the database is created with the required schema, tables and the data

    psql -p 5432 postgres -U postgres

    \i FintechProj3_DB_build.sql

- Ensure "Streamlit" is successfully installed
- Ensure "psycopg2" module is successfully installed
- Ensure Web3==5.17.0 is successfully installed

Script Execution process

Clone the Git repo as shown below :

    git clone https://github.com/gadam/fintech_project_3.git

Go to the cloned directory

    cd fintech_project_3

Execute the script as follows

    streamlit run sales.py

You should be able to see the front-end webpage.






