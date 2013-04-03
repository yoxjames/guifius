drop table if exists nodes;
create table nodes (
	id integer primary key autoincrement,
	name string not null,
	lon int not null,
	lat int not null
);
