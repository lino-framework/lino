DROP TABLE IF EXISTS DBITEMS;
CREATE TABLE DBITEMS (
  id       CHAR(100)   PRIMARY KEY NOT NULL,
  super    CHAR(100), -- ref to DBITEMS
  seq      INT NOT NULL,
  title    VARCHAR(80),
  abstract TEXT,
  body     TEXT
);

DROP TABLE IF EXISTS DBI2DBI;
CREATE TABLE DBI2DBI (
  id1      CHAR(100)   NOT NULL,
  id2      CHAR(100)   NOT NULL
);
