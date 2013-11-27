from code_val import *

get_devices = \
'select d.* \
from  \
  network n \
  , relation r \
  , device d \
join n where n.id = ? \
join r where r.a_id = n.id \
  and r.type_val = ? \
join d where d.id = r.b_val'

get_networks_main = \
'select n.id, n.name, o.data \
from network n \
left outer join object as o on o.id_obj = n.geometry_obj \
where n.phase_type_val in(?,?,?)'

get_devices_for_network_json = \
'select p.lat, p.lon, d.name \
from device d \
inner join relation n_d on d.id = n_d.b_id \
and n_d.a_id = ? \
inner join point p on p.id = d.point_id \
and n_d.type_val = ? \
and d.status_type_val = ?'

get_my_networks = \
'select n.* \
from network n \
left outer join relation n_u on n_u.a_id = n.id \
and n_u.type_val = ? \
left outer join users u on u.id = n_u.b_id \
and u.id = ?'

get_devices_for_network = \
'select d.* \
from device d \
left outer join relation n_d on n_d.b_id = d.id \
where n_d.type_val = ? \
and n_d.a_id = ?'

get_code_str = \
'select tv.name from type_val tv where tv.id = ?'

get_device = \
'select * from device d \
join point p on p.id = d.point_id \
where d.id = ?'

update_network = \
'update network \
set name = ? \
, type_val = ? \
, phase_type_val = ? \
where id = ?'

insert_network = \
'insert into network \
(name, type_val, phase_type_val) \
values (?,?,?)'

get_network_polygon = \
'select obj.data \
from object obj \
, network n \
join network where n.network_id = ? \
join obj where obj.id_obj = n.geometry_obj'

add_polygon_to_network = \
'update network set geometry_obj = ? where id = ?'

get_device_on_point = \
'select id from device where point_id = ?'

move_point = \
'update  point \
set lat = ? \
, lon = ? \
where id = ?'

pull_device_id_by_name = \
'select * from device where name = ?'

get_point_id = \
'select point_id from device where id = ?'

update_device = \
'update device \
set name = ? \
, type_val = ? \
, polarization_type_val = ? \
, status_type_val = ? \
, azimuth = ? \
, elevation = ? \
where id = ?'

add_device = \
'insert into device \
(name, type_val, point_id, azimuth, elevation, \
polarization_type_val, status_type_val) \
values(?,?,?,?,?,?,?)'
