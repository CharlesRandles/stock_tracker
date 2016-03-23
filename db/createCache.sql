--A table for caching holdings and prices

select '*** Cache table ***';

select 'Dropping old cache table';
drop table if exists cache;

select 'Creating new cache table';
create table cache ( symbol text(16),
       	     	     name text(64),
       	     	     holding integer,
       		     purchase_price real,
       		     purchase_date text(32), --ISO8601 format
       		     sale_price real,
       		     sale_date text(32),
		     bid real,
		     offer real,
		     change real);

select '*** Cache complete ***';
