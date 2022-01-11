CREATE TABLE Users
(
    id String NOT NULL PRIMARY KEY,
    username String NOT NULL,
    live boolean NOT NULL
);


CREATE TABLE Polls
(
    id Integer NOT NULL PRIMARY KEY CHECK(id > 0),
    content String NOT NULL,
    possible_answears String NOT NULL /* this will be a string with all possible answears seperated by ','
                                         at need, will be parsed */
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