-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- database name: tournament
-- CREATE DATABASE tournament;
-- \connect tournament

CREATE TABLE player (
id SERIAL PRIMARY KEY,
name           TEXT    NOT NULL,
initial_points  INT
);

CREATE TABLE tourney (
id SERIAL PRIMARY KEY     NOT NULL,
name           TEXT    NOT NULL,
tourney_date 	DATE     NOT NULL,
location  TEXT
);

CREATE TABLE match (
player1_id  INT references player(id) NOT NULL,
player2_id 	INT references player(id),
tourney_id INT references tourney(id),
player1_score INT,
player2_score INT
);
