create table gamestats_batter (
	gid varchar(30) not null,
	pid int(11) not null,
	game_date date not null,
	pa smallint not null,
	ab smallint not null,
	hits smallint not null,
	runs smallint not null,
	hr smallint not null,
	bb smallint not null,
	so smallint not null,
	rbi smallint not null,
	1b smallint not null,
	2b smallint not null,
	3b smallint not null,
	sb smallint not null,
	cs smallint not null,
	lob smallint not null,
	bo smallint not null,
	sac smallint not null,
	sf smallint not null,
	hbp smallint not null,
	foreign key(gid) references games(gid)
);


create table gamestats_pitcher (
	gid varchar(30) not null,
	pid int(11) not null,
	game_date date not null,
	win smallint not null,
	loss smallint not null,
	save smallint not null,
	hits smallint not null,
	runs smallint not null,
	er smallint not null,
	hr smallint not null,
	bb smallint not null,
	so smallint not null,
	bf smallint not null,
	outs smallint not null,
	strikes smallint not null,
	pitches smallint not null,
	foreign key(gid) references games(gid)
);