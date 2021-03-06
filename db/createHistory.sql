--Must retain old history data.
select '*** History ***';

select 'If there is no history table, this script complains but succeeds';
select 'If in doubt, run it again';

select 'Dropping backup table';
drop table if exists history_backup;

select 'Creating backup';
create table history_backup as select * from history;

select 'Dropping old history';
drop table if exists history;

select 'Creating history table';
create table history (   id integer primary key
       	     	       , symbol text(16)
		       , price real
		       , date text(32)
		       );

select 'Recovering history';
insert into history
select   id
       , symbol
       , price
       , date
       from history_backup;

select '*** History complete ***';
       
