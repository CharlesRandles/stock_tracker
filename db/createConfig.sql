--Clear old table
drop table if exists config;

--Metadata config table
.print Creating config table
create table config( name text(64) primary key,
       	     	     value text(64) );

--Metadata
.print Inserting metadata
insert into config values ('min_reload', '300');
insert into config values ('last_reload', '2000-01-01 00:00:00'); --more than 300 seconds

select * from config;
