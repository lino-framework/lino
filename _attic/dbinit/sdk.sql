DROP TABLE IF EXISTS FILES;
CREATE TABLE FILES (
  id       CHAR(100)   PRIMARY KEY NOT NULL,
  title    VARCHAR(80),
  abstract TEXT,
  body     TEXT
);

DROP TABLE IF EXISTS CLASSES;
CREATE TABLE CLASSES (
  id       CHAR(100)   PRIMARY KEY NOT NULL,
  super    CHAR(100), -- ref to CLASSES
  file     CHAR(100), -- ref to FILES
  title    VARCHAR(80),
  abstract TEXT,
  body     TEXT
);

DROP TABLE IF EXISTS METHODS;
CREATE TABLE METHODS (
  name     CHAR(100) NOT NULL,
  class    CHAR(100) NOT NULL, -- ref to CLASSES
  title    VARCHAR(80),
  abstract TEXT,
  body     TEXT,
  PRIMARY KEY (name,class)
);

-- ERROR 1171 : All parts of a PRIMARY KEY must be NOT NULL; If you
-- need NULL in a key, use UNIQUE instead

DROP TABLE IF EXISTS PROJECTS;
-- inherits NEWS
CREATE TABLE PROJECTS (
  date      DATE,
  title     VARCHAR(80),
  abstract  TEXT,
  body      TEXT,
  id BIGINT PRIMARY KEY AUTO_INCREMENT NOT NULL,
  responsible  BIGINT, -- ref to PERS
  sponsor   BIGINT, -- ref to ORG
  super   BIGINT, -- ref to PROJECTS
  stopDate  DATE
);

DROP TABLE IF EXISTS PRJ2PRJ;
CREATE TABLE PRJ2PRJ (
  id1      BIGINT   NOT NULL,
  id2      BIGINT   NOT NULL
);

DROP TABLE IF EXISTS CHANGES;
CREATE TABLE CHANGES (
  id BIGINT PRIMARY KEY AUTO_INCREMENT NOT NULL,
  author   BIGINT, -- ref to PERS
  major     INT NOT NULL,
  minor     INT NOT NULL,
  release   INT NOT NULL,
  date     DATE,
  title    VARCHAR(80),
  abstract TEXT,
  body     TEXT
);

DROP TABLE IF EXISTS FILES2CHANGES;
CREATE TABLE FILES2CHANGES (
  id1      CHAR(100)  NOT NULL, -- ref to FILES
  id2      BIGINT     NOT NULL -- ref to CHANGES
);


DROP TABLE IF EXISTS RELEASES;
CREATE TABLE RELEASES (
  major     INT NOT NULL,
  minor     INT NOT NULL,
  release   INT NOT NULL,
  date      DATE,
  title     VARCHAR(80),
  PRIMARY KEY (major,minor,release)
);

