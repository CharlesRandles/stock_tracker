/*
	Create structure and data for current holdings
*/

.print Destroying old objects
drop table if exists holdings;

.print "Creating new table"
create table holdings (
       id integer primary key,
       symbol text(16),
       holding integer,
       purchase_price real,
       purchase_date text(32) --ISO8601 format
);

.print Creating holdings

insert into holdings values(
       0,
       'CTN.AX',
       '14000',
       1.065,
       '2015-02-01 14:30:00.000');
       
insert into holdings values(
       1,
       'MPL.AX',
       '7500',
       2.0,
       '2014-11-20 14:30:00.000');

.print Database Created
select symbol from holdings;
select count(symbol) from holdings;


