
DROP TABLE IF EXISTS TALKS;
CREATE TABLE TALKS (
  id BIGINT PRIMARY KEY AUTO_INCREMENT NOT NULL,
  date   DATE,
  time   VARCHAR(10),
  type   VARCHAR(20),
  title  VARCHAR(80),
  ipers  BIGINT, -- ref to PERS
  epers  BIGINT, -- ref to PERS
  notes  TEXT
);

INSERT INTO TALKS VALUES
  (1,"2002-02-22","11:00","Mail","Let's meet tomorrow",2,1,NULL);
INSERT INTO TALKS VALUES
  (2,"2002-02-23","10:00","Phone","Sorry",2,1,"this is some text");


DROP TABLE IF EXISTS MEETINGS;
CREATE TABLE MEETINGS (
  id BIGINT PRIMARY KEY AUTO_INCREMENT NOT NULL,
  date   DATE,
  time   VARCHAR(10),
  type   VARCHAR(20),
  title  VARCHAR(80),
  org    BIGINT, -- ref to ORG
  addr   BIGINT, -- ref to ADDR
  notes  TEXT
);



DROP TABLE IF EXISTS NEWS;
CREATE TABLE NEWS (
  id BIGINT PRIMARY KEY AUTO_INCREMENT NOT NULL,
  author   BIGINT, -- ref to PERS
  project   BIGINT, -- ref to PROJECTS
  date     DATE,
  title    VARCHAR(80),
  abstract TEXT,
  body     TEXT
);



DROP TABLE IF EXISTS MEET2PERS;
--CREATE TABLE MEET2PERS (
--  id       BIGINT   AUTO_INCREMENT PRIMARY KEY NOT NULL, -- not used...
--  contact  BIGINT   NOT NULL,
--  pers     BIGINT   NOT NULL,
--  note     VARCHAR(60)
--);
CREATE TABLE MEET2PERS (
  id1      BIGINT   NOT NULL,
  id2      BIGINT   NOT NULL,
  note     VARCHAR(60)
);

INSERT INTO MEET2PERS VALUES (1,1,NULL);
INSERT INTO MEET2PERS VALUES (1,2,NULL);
INSERT INTO MEET2PERS VALUES (2,1,NULL);
INSERT INTO MEET2PERS VALUES (2,2,NULL);



