select '*** Config table ***';

--Clear old table
drop table if exists config;

--Metadata config table
select 'Creating config table';
create table config( name text(64) primary key,
       	     	     value text(64) );

--Metadata
select 'Inserting metadata';
insert into config values ('min_reload', '300');
insert into config values ('last_reload', '2000-01-01 00:00:00'); --more than 300 seconds ago
insert into config values ('server_utcoffset', '-0800');
insert into config values ('asx_utcoffset', '+1000');

select '*** Config complete ***';
