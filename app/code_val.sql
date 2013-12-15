delete from type_val where id_val > 0;

insert into type_val (name,class_name,description) values ("FUN","NET_PHASE_TYPE", "Just For Fun");
insert into type_val (name,class_name,description) values ("PLANNED","NET_PHASE_TYPE", "Planned");
insert into type_val (name,class_name,description) values ("IN_PROGRESS","NET_PHASE_TYPE", "Build In Progress");
insert into type_val (name,class_name,description) values ("ONLINE","NET_PHASE_TYPE", "Online");

insert into type_val (name,class_name,description) values ("A_NETWORK_B_PERSON","RELATION","");
insert into type_val (name,class_name,description) values ("A_NETWORK_B_DEVICE","RELATION","");

insert into type_val (name,class_name,description) values ("POLYGON","OBJECT","");

insert into type_val (name,class_name,description) values ("FREE","NET_TYPE","NCL Compliant");
insert into type_val (name,class_name,description) values ("CORPORATE", "NET_TYPE","For Profit");
insert into type_val (name,class_name,description) values ("UNKNOWN","NET_TYPE", "Unknown");

insert into type_val (name,class_name,description) values ("HORIZONTAL","POLARIZATION_TYPE","Horizontal");
insert into type_val (name,class_name,description) values ("VERTICAL","POLARIZATION_TYPE","Vertical");
insert into type_val (name,class_name,description) values ("UNKNOWN","POLARIZATION_TYPE","Unknown");

insert into type_val (name,class_name,description) values ("UNKNOWN","NODE_TYPE","Unknown");

insert into type_val (name,class_name,description) values ("UNKNOWN","CONNECTION_TYPE","Unknown");
