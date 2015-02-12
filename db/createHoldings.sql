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

insert into holdings (symbol, holding, purchase_price, purchase_date) values(
       'AFI.AX',
       1610,
       6.16,
       '2015-02-01 14:30:00.000');

insert into holdings (symbol, holding, purchase_price, purchase_date) values(
       'ARG.AX',
       3101,
       8.00,
       '2014-08-18 14:30:00.000');

insert into holdings (symbol, holding, purchase_price, purchase_date) values(
       'CTN.AX',
       14080,
       1.065,
       '2015-02-01 14:30:00.000');
       
insert into holdings (symbol, holding, purchase_price, purchase_date) values(
       'MPL.AX',
       7618,
       2.0,
       '2014-11-20 14:30:00.000');

insert into holdings (symbol, holding, purchase_price, purchase_date) values(
       'SUN.AX',
       74,
       0.0,
       '2013-09-01 14:30:00.000');

insert into holdings (symbol, holding, purchase_price, purchase_date) values(
       'SUN.AX',
       67,
       0.0,
       '2014-11-20 14:30:00.000');

.print Database Created
select symbol from holdings;
select count(symbol) from holdings;

.exit

