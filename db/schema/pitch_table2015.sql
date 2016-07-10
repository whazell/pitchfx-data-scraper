create table pitches_2015 (
	id int not null auto_increment,
	sv_id varchar(30),
	pitcher_id int not null,
	batter_id int not null,
	pitcher_throws char(1),
	batter_hits char(1),
	description varchar(30),
	pitch_result char(1) not null,
	balls int not null,
	strikes int not null,
	outs int not null,
	start_speed float,
	end_speed float,
	sz_top float,
	sz_bot float,
	pfx_x float,
	pfx_z float,
	px float,
	pz float,
	x0 float,
	y0 float,
	z0 float,
	vx0 float,
	vy0 float,
	vz0 float,
	ax float,
	ay float,
	az float,
	break_y float,
	break_angle float,
	break_length float,
	pitch_type char(2),
	type_confidence float,
	zone int,
	nasty int,
	spin_dir float,
	spin_rate float,
	primary key(id)
);
