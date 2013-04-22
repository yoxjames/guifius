drop table if exists nodes;
create table nodes (
	id integer primary key autoincrement,
	name string not null,
	lon int not null,
	lat int not null
);

drop table if exists users;
create table users (
	id integer primary key autoincrement,
	username string not null,
	password string not null,
	name string not null,
	city string not null,
	role integer not null
);
