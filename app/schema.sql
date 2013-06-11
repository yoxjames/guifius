drop table if exists nodes;
create table nodes (
	id integer primary key autoincrement,
	lon int not null,
	lat int not null,
	network_id int not null,
	foreign key(network_id) REFERENCES network(network_id)
);

drop table if exists users;
create table users (
	id integer primary key autoincrement,
	username string not null,
	password string not null,
	email string not null,
	name string not null,
	city string not null,
	role integer not null
);

drop table if exists network;
create table network (
	network_id integer primary key autoincrement,
	name string not null,
	owner_id int,
	foreign key(owner_id) REFERENCES users(id)
);
