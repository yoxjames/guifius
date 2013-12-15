drop table if exists point;
create table point (
	id integer primary key autoincrement,
	lat int not null,
	lon int not null,
	altitude int,
	seq int
);

drop table if exists device;
create table device (
	id integer primary key autoincrement,
	name string not null,
	type_val int not null,
	point_id not null,
	azimuth int,
	elevation int,
	polarization_type_val,
	status_type_val not null,

	foreign key(point_id) REFERENCES point(point_id),
	foreign key(type_val) REFERENCES type_val(id_val),
	foreign key(polarization_type_val) REFERENCES type_val(id_val),
	foreign key(status_type_val) REFERENCES type_val(id_val)
);

drop table if exists network;
create table network (
	id integer primary key autoincrement,
	name string not null,
	type_val int not null,
	phase_type_val int not null,
	geometry_obj int,


	foreign key(type_val) REFERENCES type_val(id_val),
	foreign key(phase_type_val) REFERENCES type_val(id_val),
        foreign key(geometry_obj) REFERENCES object(id_obj)
);

drop table if exists users;
create table users (
	id integer primary key autoincrement,
	username string not null,
	password string not null,
	email string not null,
	type_val int not null,

        foreign key(type_val) REFERENCES type_val(id_val)
);

drop table if exists object;
create table object (
	id_obj integer primary key autoincrement,
	type_val int not null,
	data string,

	foreign key(type_val) REFERENCES type_val(id_val)
);

drop table if exists relation;
create table relation (
	id integer primary key autoincrement,
	a_id int not null,
	b_id int not null,
        type_val int not null,

	foreign key(type_val) REFERENCES type_val(id_val)
);

drop table if exists type_val;
create table type_val (
	id_val integer primary key autoincrement,
	name string not null,
	description string,
	obj int,
	class_name string not null,

	foreign key(obj) REFERENCES object(id_obj)
);

drop table if exists connection;
create table connection (
	id integer primary key autoincrement,
	type_val int not null,
	device_a_id int not null,
	device_b_id int,
	target_point_id int not null,
	active int not null,
	bandwidth int,

	foreign key(device_a_id) REFERENCES device(id),
	foreign key(device_b_id) REFERENCES device(id)
);



