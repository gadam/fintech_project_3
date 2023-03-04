drop database if exists nftix;
create database nftix;
\c nftix;
create schema nftix;
drop table if exists events_sales;
drop table if exists events; 
create table if not exists nftix.events (
			event_id serial primary key, 
			event_name varchar(255), 
			event_date timestamp, 
			venue 	varchar(1000), 
			tkt_price_AUD numeric(8,2),
			total_no_of_tkts int, 
			tkts_remaining int);
create table if not exists nftix.events_sales (txn_id serial primary key, event_id int references nftix.events(event_id), contract_address varchar(250));
insert into nftix.events (event_name, event_date, venue,tkt_price_AUD, total_no_of_tkts,tkts_remaining) values ('Bonjovi Live Concert - 2023','2023-06-10 20:00:00','Central London',500.00,50000,12345);
insert into nftix.events (event_name, event_date, venue,tkt_price_AUD, total_no_of_tkts,tkts_remaining) values ('European League - 2023 : England vs Spain','2023-04-21 22:00:00','Manchester',480.00,45000,15345);
insert into nftix.events (event_name, event_date, venue,tkt_price_AUD, total_no_of_tkts,tkts_remaining) values ('Ed Sheeran Live Concert - 2023','2023-10-10 19:00:00','New York',600.00,60000,24945);
insert into nftix.events (event_name, event_date, venue,tkt_price_AUD, total_no_of_tkts,tkts_remaining) values ('European League 2023 Final - France vs Spain','2023-12-10 20:00:00','Milan, Italy',650.00,75000,53219);
insert into nftix.events (event_name, event_date, venue,tkt_price_AUD, total_no_of_tkts,tkts_remaining) values ('Italian Wine Festival','2023-08-14 16:00:00','Venice,Italy',465.00,20000,14560);
insert into nftix.events (event_name, event_date, venue,tkt_price_AUD, total_no_of_tkts,tkts_remaining) values ('Fintech Event, Australia - 2023','2023-09-15 08:00:00','Sydney, Australia',250.00,8000,4500);
insert into nftix.events (event_name, event_date, venue,tkt_price_AUD, total_no_of_tkts,tkts_remaining) values ('Wine Festival Byron Bay, Australia - 2023','2023-10-15 07:00:00','Byron Bay, Australia',300.00,10000,6500);
insert into nftix.events (event_name, event_date, venue,tkt_price_AUD, total_no_of_tkts,tkts_remaining) values ('Justin Biber Live Concert - 2023','2023-11-15 20:00:00','Hyde Park, Sydney, Australia',450.00,75000,16000);
insert into nftix.events (event_name, event_date, venue,tkt_price_AUD, total_no_of_tkts,tkts_remaining) values ('Cricket - BBL 2023 : Perth Scortchers vs Sydney Thunders','2023-12-20 19:00:00','Perth, Australia',575.00,30000,17500);
insert into nftix.events (event_name, event_date, venue,tkt_price_AUD, total_no_of_tkts,tkts_remaining) values ('Blockchain Conference 2023','2023-07-15 09:00:00','Sydney, Australia',320.00,2000,550);
insert into nftix.events (event_name, event_date, venue,tkt_price_AUD, total_no_of_tkts,tkts_remaining) values ('Solidity for Smart Contracts - Work Shop 2023','2023-08-10 08:00:00','Sydney, Australia',250.00,5000,1550);
insert into nftix.events (event_name, event_date, venue,tkt_price_AUD, total_no_of_tkts,tkts_remaining) values ('Crypto Digital asserts SUMMIT 2023','2023-05-25 09:00:00','London, UK',430.00,12000,11500);
insert into nftix.events (event_name, event_date, venue,tkt_price_AUD, total_no_of_tkts,tkts_remaining) values ('Blockchain Revolution SUMMIT','2023-06-24 09:00:00','London',800.00,20000,15000);
insert into nftix.events (event_name, event_date, venue,tkt_price_AUD, total_no_of_tkts,tkts_remaining) values ('Crossborder Payments on Blockchain','2023-08-24 09:00:00','San Fransisco, USA',700.00,6000,1550);
insert into nftix.events (event_name, event_date, venue,tkt_price_AUD, total_no_of_tkts,tkts_remaining) values ('Blockchain Security','2023-11-20 09:00:00','Dublin, Ireland',600.0,20000,2500);
