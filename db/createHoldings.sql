/*
	Create structure and data for current holdings
*/

select '*** Holdings table ***';
select 'Dropping backup';
drop table if exists holdings_backup;

select 'Create backup';
create table holdings_backup as select * from holdings;

select 'Dropping holdings table';
drop table if exists holdings;

select 'Creating holdings table';
create table holdings (
       id integer primary key,
       symbol text(16),
       holding integer,
       purchase_price real,
       purchase_date text(32), --ISO8601 format
       sale_price real,
       sale_date text(32)
);

select 'Creating holdings';
insert into holdings select * from holdings_backup;

/*
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

select 'Database Created';
*/
select symbol from holdings;
select count(symbol) from holdings;

select '*** Holdings table complete ***';
