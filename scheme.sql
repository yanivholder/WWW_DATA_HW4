CREATE DATABASE www_hw44 
ENCODING 'utf8' 
TEMPLATE template1


CREATE TABLE Users
(
    id String NOT NULL PRIMARY KEY,
    username String NOT NULL,
    live boolean NOT NULL
);


CREATE TABLE Polls
(
    id Integer NOT NULL PRIMARY KEY CHECK(id > 0),
    content String NOT NULL
);


CREATE TABLE Answears
(
    user_id String REFERENCES Users(id),
    poll_id Integer REFERENCES Polls(id),
    answear String NOT NULL,
    PRIMARY KEY (user_id, poll_id)
);


CREATE TABLE Admins
(
    id Integer NOT NULL PRIMARY KEY,
    password String NOT NULL
);