DROP TABLE IF EXISTS QUERIES;
CREATE TABLE QUERIES (
  id       CHAR(20) NOT NULL PRIMARY KEY,
  master   CHAR(10),
  label_en VARCHAR(60),
  pglen    INT,
  filter VARCHAR(200)
  -- desc_en  TEXT
);

INSERT INTO QUERIES VALUES
       ("LANG",    "LANG", "Languages",20,NULL);
INSERT INTO QUERIES VALUES
       ("NATIONS", "NATIONS",  "Nations",20,NULL);
INSERT INTO QUERIES VALUES
       ("CITIES",  "CITIES",   "Cities",20,NULL);
INSERT INTO QUERIES VALUES
       ("ADDR",    "ADDR",     "Addresses",10,NULL);
INSERT INTO QUERIES VALUES
       ("PERS",    "PERS",     "Persons",10,NULL);
INSERT INTO QUERIES VALUES
       ("ORG",     "ORG",      "Organisations",10,NULL);
INSERT INTO QUERIES VALUES
       ("QUERIES", "QUERIES",  "Queries",10,NULL);
INSERT INTO QUERIES VALUES
       ("QRYCOLS", "QRYCOLS",  "Query Columns",15,NULL);
INSERT INTO QUERIES VALUES
       ("TALKS", "Talks", "Talks",10,NULL);
INSERT INTO QUERIES VALUES
       ("NEWS",     "NEWS", "News",20,NULL);
INSERT INTO QUERIES VALUES
       ("TODO",    "PROJECTS", "To-Do-List",20,
       "ISNULL(PROJECTS.stopDate)");
--INSERT INTO QUERIES VALUES
--       ("ORG2ORG",  "ORG2ORG", NULL,10,NULL);
--INSERT INTO QUERIES VALUES
--       ("ORG2PERS",  "ORG2PERS", NULL,10,NULL);
-- INSERT INTO QRYCOLS VALUES
--  ("CONTACTS",1,"V",NULL,"parent","Parent", 20,0);

DROP TABLE IF EXISTS QRYCOLS;
CREATE TABLE QRYCOLS (
  query    CHAR(20) NOT NULL,
  seq      INT NOT NULL,
  coltype  CHAR(1) NOT NULL,
  alias    CHAR(20),          -- name of table
  fieldname  CHAR(20),          -- name of field, vurt or action
  label_en VARCHAR(60),
  -- desc_en  TEXT,
  width    INT,
  qfilter  INT
);


