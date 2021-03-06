create table pitches (
	game_date date not null,
	play_guid varchar(64),
	sv_id varchar(30),
	pid int not null,
	bid int not null,
	gid varchar(30) not null,
	abid bigint not null,
	des varchar(30),
	result char(1) not null,
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
	foreign key (gid) references games(gid),
	foreign key (pid) references players(pid),
	foreign key (bid) references players(pid),
	foreign key (abid) references atbats(abid)
);
