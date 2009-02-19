# file generated using 21.py

CREATE TABLE Currencies (
     id CHAR(3),
  name_en VARCHAR(50),
  PRIMARY KEY (id)
);
CREATE TABLE Languages (
     id CHAR(2),
  name_en VARCHAR(50),
  PRIMARY KEY (id)
);
CREATE TABLE Nations (
     id CHAR(2),
  name_en VARCHAR(50),
  area BIGINT,
  population BIGINT,
  curr VARCHAR(50),
  isocode VARCHAR(50),
  PRIMARY KEY (id)
);
CREATE TABLE Cities (
     nation_id CHAR(2),
  id BIGINT,
  name VARCHAR(50),
  zipCode VARCHAR(50),
  inhabitants BIGINT,
  PRIMARY KEY (nation_id, id)
);
CREATE TABLE Organisations (
     id BIGINT,
  email VARCHAR(60),
  phone VARCHAR(50),
  gsm VARCHAR(50),
  fax VARCHAR(50),
  website VARCHAR(200),
  nation_id CHAR(2),
  city_nation_id CHAR(2),
  city_id BIGINT,
  zip VARCHAR(50),
  street VARCHAR(50),
  house BIGINT,
  box VARCHAR(50),
  name VARCHAR(50),
  PRIMARY KEY (id)
);
CREATE TABLE Persons (
     id BIGINT,
  name VARCHAR(50),
  firstName VARCHAR(50),
  sex CHAR(1),
  birthDate CHAR(8),
  PRIMARY KEY (id)
);
CREATE TABLE Partners (
     id BIGINT,
  name VARCHAR(50),
  firstName VARCHAR(50),
  email VARCHAR(60),
  phone VARCHAR(50),
  gsm VARCHAR(50),
  fax VARCHAR(50),
  website VARCHAR(200),
  nation_id CHAR(2),
  city_nation_id CHAR(2),
  city_id BIGINT,
  zip VARCHAR(50),
  street VARCHAR(50),
  house BIGINT,
  box VARCHAR(50),
  type_id VARCHAR(50),
  title VARCHAR(50),
  logo VARCHAR(50),
  lang_id CHAR(2),
  currency_id CHAR(3),
  PRIMARY KEY (id)
);
CREATE TABLE PartnerTypes (
     id VARCHAR(50),
  name_en VARCHAR(50),
  PRIMARY KEY (id)
);
CREATE TABLE Products (
     id BIGINT,
  name VARCHAR(50),
  price BIGINT,
  PRIMARY KEY (id)
);
CREATE TABLE Journals (
     id CHAR(3),
  name VARCHAR(50),
  tableName VARCHAR(50),
  PRIMARY KEY (id)
);
CREATE TABLE BankStatements (
     jnl_id CHAR(3),
  seq BIGINT,
  date INT,
  closed BIGINT,
  remark VARCHAR(50),
  balance1 BIGINT,
  balance2 BIGINT,
  PRIMARY KEY (jnl_id, seq)
);
CREATE TABLE MiscOperations (
     jnl_id CHAR(3),
  seq BIGINT,
  date INT,
  closed BIGINT,
  remark VARCHAR(50),
  PRIMARY KEY (jnl_id, seq)
);
CREATE TABLE Invoices (
     jnl_id CHAR(3),
  seq BIGINT,
  date INT,
  closed BIGINT,
  remark VARCHAR(50),
  partner_id BIGINT,
  zziel INT,
  amount BIGINT,
  inverted BIGINT,
  PRIMARY KEY (jnl_id, seq)
);
CREATE TABLE InvoiceLines (
     invoice_jnl_id CHAR(3),
  invoice_seq BIGINT,
  line BIGINT,
  amount BIGINT,
  remark VARCHAR(50),
  unitPrice BIGINT,
  qty BIGINT,
  product_id BIGINT,
  PRIMARY KEY (invoice_jnl_id, invoice_seq, line)
);
CREATE TABLE BalanceItems (
     id VARCHAR(50),
  name_en VARCHAR(50),
  attrib VARCHAR(50),
  dc CHAR(1),
  type CHAR(2),
  doc TEXT,
  PRIMARY KEY (id)
);
CREATE TABLE CashFlowItems (
     id VARCHAR(50),
  name_en VARCHAR(50),
  attrib VARCHAR(50),
  dc CHAR(1),
  type CHAR(2),
  doc TEXT,
  PRIMARY KEY (id)
);
CREATE TABLE ProfitAndLossItems (
     id VARCHAR(50),
  name_en VARCHAR(50),
  attrib VARCHAR(50),
  dc CHAR(1),
  type CHAR(2),
  doc TEXT,
  PRIMARY KEY (id)
);
CREATE TABLE Accounts (
     id BIGINT,
  name_en VARCHAR(50),
  pcmn VARCHAR(50),
  parent_id BIGINT,
  balance_id VARCHAR(50),
  profit_id VARCHAR(50),
  cash_id VARCHAR(50),
  PRIMARY KEY (id)
);
CREATE TABLE Bookings (
     id BIGINT,
  date INT,
  amount BIGINT,
  dc BIGINT,
  account_id BIGINT,
  label VARCHAR(50),
  invoice_jnl_id CHAR(3),
  invoice_seq BIGINT,
  partner_id BIGINT,
  PRIMARY KEY (id)
);
/* commit */
SELECT id, name_en FROM Currencies WHERE id = 'EUR';
INSERT INTO Currencies ( id, name_en ) VALUES ( 'EUR', 'Euro' );
SELECT id, name_en FROM Currencies WHERE id = 'BEF';
INSERT INTO Currencies ( id, name_en ) VALUES ( 'BEF', 'Belgian Francs' );
SELECT id, name_en FROM Currencies WHERE id = 'USD';
INSERT INTO Currencies ( id, name_en ) VALUES ( 'USD', 'US Dollar' );
SELECT id, name_en FROM Currencies WHERE id = 'EEK';
INSERT INTO Currencies ( id, name_en ) VALUES ( 'EEK', 'Estonian kroon' );
/* commit */
SELECT id, name_en, area, population, curr, isocode FROM Nations WHERE id = 'ee';
INSERT INTO Nations ( id, name_en, area, population, curr, isocode ) VALUES ( 'ee', 'Estonia', NULL, NULL, NULL, NULL );
SELECT id, name_en, area, population, curr, isocode FROM Nations WHERE id = 'be';
INSERT INTO Nations ( id, name_en, area, population, curr, isocode ) VALUES ( 'be', 'Belgium', NULL, NULL, NULL, NULL );
SELECT id, name_en, area, population, curr, isocode FROM Nations WHERE id = 'de';
INSERT INTO Nations ( id, name_en, area, population, curr, isocode ) VALUES ( 'de', 'Germany', NULL, NULL, NULL, NULL );
SELECT id, name_en, area, population, curr, isocode FROM Nations WHERE id = 'fr';
INSERT INTO Nations ( id, name_en, area, population, curr, isocode ) VALUES ( 'fr', 'France', NULL, NULL, NULL, NULL );
SELECT id, name_en, area, population, curr, isocode FROM Nations WHERE id = 'us';
INSERT INTO Nations ( id, name_en, area, population, curr, isocode ) VALUES ( 'us', 'United States of America', NULL, NULL, NULL, NULL );
SELECT id, name_en, area, population, curr, isocode FROM Nations WHERE id = 'be';
SELECT id, name_en, area, population, curr, isocode FROM Nations WHERE id = 'be';
SELECT id, name_en, area, population, curr, isocode FROM Nations WHERE id = 'ee';
SELECT id, name_en, area, population, curr, isocode FROM Nations WHERE id = 'ee';
SELECT id, name_en, area, population, curr, isocode FROM Nations WHERE id = 'de';
SELECT id, name_en, area, population, curr, isocode FROM Nations WHERE id = 'de';
/* commit */
SELECT MAX(id) FROM Cities WHERE nation_id = 'be';
INSERT INTO Cities ( nation_id, id, name, zipCode, inhabitants ) VALUES ( 'be', 1, 'Bruxelles', NULL, 1004239 );
INSERT INTO Cities ( nation_id, id, name, zipCode, inhabitants ) VALUES ( 'be', 2, 'Brugge', NULL, 116848 );
INSERT INTO Cities ( nation_id, id, name, zipCode, inhabitants ) VALUES ( 'be', 3, 'Eupen', NULL, 17872 );
INSERT INTO Cities ( nation_id, id, name, zipCode, inhabitants ) VALUES ( 'be', 4, 'Kelmis', NULL, 10175 );
INSERT INTO Cities ( nation_id, id, name, zipCode, inhabitants ) VALUES ( 'be', 5, 'Raeren', NULL, 9933 );
INSERT INTO Cities ( nation_id, id, name, zipCode, inhabitants ) VALUES ( 'be', 6, 'Mons', NULL, 90992 );
INSERT INTO Cities ( nation_id, id, name, zipCode, inhabitants ) VALUES ( 'be', 7, 'Liège', NULL, 185608 );
INSERT INTO Cities ( nation_id, id, name, zipCode, inhabitants ) VALUES ( 'be', 8, 'Charleroi', NULL, 200983 );
INSERT INTO Cities ( nation_id, id, name, zipCode, inhabitants ) VALUES ( 'be', 9, 'Verviers', NULL, 52739 );
SELECT MAX(id) FROM Cities WHERE nation_id = 'de';
INSERT INTO Cities ( nation_id, id, name, zipCode, inhabitants ) VALUES ( 'de', 1, 'Aachen', NULL, NULL );
INSERT INTO Cities ( nation_id, id, name, zipCode, inhabitants ) VALUES ( 'de', 2, 'Köln', NULL, NULL );
INSERT INTO Cities ( nation_id, id, name, zipCode, inhabitants ) VALUES ( 'de', 3, 'Berlin', NULL, NULL );
INSERT INTO Cities ( nation_id, id, name, zipCode, inhabitants ) VALUES ( 'de', 4, 'Bonn', NULL, NULL );
INSERT INTO Cities ( nation_id, id, name, zipCode, inhabitants ) VALUES ( 'de', 5, 'München', NULL, NULL );
INSERT INTO Cities ( nation_id, id, name, zipCode, inhabitants ) VALUES ( 'de', 6, 'Eschweiler', NULL, NULL );
INSERT INTO Cities ( nation_id, id, name, zipCode, inhabitants ) VALUES ( 'de', 7, 'Alfter-Oedekoven', NULL, NULL );
SELECT MAX(id) FROM Cities WHERE nation_id = 'ee';
INSERT INTO Cities ( nation_id, id, name, zipCode, inhabitants ) VALUES ( 'ee', 1, 'Tallinn', NULL, 442000 );
INSERT INTO Cities ( nation_id, id, name, zipCode, inhabitants ) VALUES ( 'ee', 2, 'Tartu', NULL, 109100 );
INSERT INTO Cities ( nation_id, id, name, zipCode, inhabitants ) VALUES ( 'ee', 3, 'Narva', NULL, 80300 );
INSERT INTO Cities ( nation_id, id, name, zipCode, inhabitants ) VALUES ( 'ee', 4, 'Kilingi-Nõmme', NULL, 2490 );
INSERT INTO Cities ( nation_id, id, name, zipCode, inhabitants ) VALUES ( 'ee', 5, 'Pärnu', NULL, 52000 );
INSERT INTO Cities ( nation_id, id, name, zipCode, inhabitants ) VALUES ( 'ee', 6, 'Rakvere', NULL, 18096 );
INSERT INTO Cities ( nation_id, id, name, zipCode, inhabitants ) VALUES ( 'ee', 7, 'Viljandi', NULL, 20756 );
INSERT INTO Cities ( nation_id, id, name, zipCode, inhabitants ) VALUES ( 'ee', 8, 'Ruhnu', NULL, 58 );
INSERT INTO Cities ( nation_id, id, name, zipCode, inhabitants ) VALUES ( 'ee', 9, 'Vigala', NULL, 1858 );
INSERT INTO Cities ( nation_id, id, name, zipCode, inhabitants ) VALUES ( 'ee', 10, 'Kohtla-Järve', NULL, 70800 );
/* commit */
SELECT id, name_en FROM PartnerTypes WHERE id = 'c';
INSERT INTO PartnerTypes ( id, name_en ) VALUES ( 'c', 'Customer' );
SELECT id, name_en FROM PartnerTypes WHERE id = 's';
INSERT INTO PartnerTypes ( id, name_en ) VALUES ( 's', 'Supplier' );
SELECT id, name_en FROM PartnerTypes WHERE id = 'm';
INSERT INTO PartnerTypes ( id, name_en ) VALUES ( 'm', 'Member' );
SELECT id, name_en FROM PartnerTypes WHERE id = 'e';
INSERT INTO PartnerTypes ( id, name_en ) VALUES ( 'e', 'Employee' );
SELECT id, name_en FROM PartnerTypes WHERE id = 'd';
INSERT INTO PartnerTypes ( id, name_en ) VALUES ( 'd', 'Sponsor' );
/* commit */
SELECT id, name_en, attrib, dc, type, doc FROM ProfitAndLossItems WHERE id = '4';
INSERT INTO ProfitAndLossItems ( id, name_en, attrib, dc, type, doc ) VALUES ( '4', 'TULUD', NULL, 'C', NULL, NULL );
SELECT id, name_en, attrib, dc, type, doc FROM ProfitAndLossItems WHERE id = '41';
INSERT INTO ProfitAndLossItems ( id, name_en, attrib, dc, type, doc ) VALUES ( '41', 'Äritulud', NULL, 'C', NULL, NULL );
SELECT id, name_en, attrib, dc, type, doc FROM ProfitAndLossItems WHERE id = '411';
INSERT INTO ProfitAndLossItems ( id, name_en, attrib, dc, type, doc ) VALUES ( '411', 'Realiseerimise netokäive', NULL, 'C', NULL, NULL );
SELECT id, name_en, attrib, dc, type, doc FROM ProfitAndLossItems WHERE id = '42';
INSERT INTO ProfitAndLossItems ( id, name_en, attrib, dc, type, doc ) VALUES ( '42', 'Finantstulud', NULL, 'C', NULL, NULL );
SELECT id, name_en, attrib, dc, type, doc FROM ProfitAndLossItems WHERE id = '421';
INSERT INTO ProfitAndLossItems ( id, name_en, attrib, dc, type, doc ) VALUES ( '421', 'Intressitulud', NULL, 'C', NULL, NULL );
SELECT id, name_en, attrib, dc, type, doc FROM ProfitAndLossItems WHERE id = '5';
INSERT INTO ProfitAndLossItems ( id, name_en, attrib, dc, type, doc ) VALUES ( '5', 'Ümmargused', NULL, 'C', NULL, NULL );
SELECT id, name_en, attrib, dc, type, doc FROM ProfitAndLossItems WHERE id = '6';
INSERT INTO ProfitAndLossItems ( id, name_en, attrib, dc, type, doc ) VALUES ( '6', 'KULUD', NULL, 'C', NULL, NULL );
SELECT id, name_en, attrib, dc, type, doc FROM ProfitAndLossItems WHERE id = '61';
INSERT INTO ProfitAndLossItems ( id, name_en, attrib, dc, type, doc ) VALUES ( '61', 'Ärikulud', NULL, 'C', NULL, NULL );
SELECT id, name_en, attrib, dc, type, doc FROM ProfitAndLossItems WHERE id = '610';
INSERT INTO ProfitAndLossItems ( id, name_en, attrib, dc, type, doc ) VALUES ( '610', 'Mitmesugused tegevuskulud', NULL, 'C', NULL, NULL );
SELECT id, name_en, attrib, dc, type, doc FROM ProfitAndLossItems WHERE id = '611';
INSERT INTO ProfitAndLossItems ( id, name_en, attrib, dc, type, doc ) VALUES ( '611', 'Tööjõukulud', NULL, 'C', NULL, NULL );
SELECT id, name_en, attrib, dc, type, doc FROM ProfitAndLossItems WHERE id = '6111';
INSERT INTO ProfitAndLossItems ( id, name_en, attrib, dc, type, doc ) VALUES ( '6111', 'Palgakulu', NULL, 'C', NULL, NULL );
SELECT id, name_en, attrib, dc, type, doc FROM ProfitAndLossItems WHERE id = '6112';
INSERT INTO ProfitAndLossItems ( id, name_en, attrib, dc, type, doc ) VALUES ( '6112', 'Sotsiaal- jt. maksud', NULL, 'C', NULL, NULL );
SELECT id, name_en, attrib, dc, type, doc FROM ProfitAndLossItems WHERE id = '612';
INSERT INTO ProfitAndLossItems ( id, name_en, attrib, dc, type, doc ) VALUES ( '612', 'Kulum ja allahindlus', NULL, 'C', NULL, NULL );
SELECT id, name_en, attrib, dc, type, doc FROM ProfitAndLossItems WHERE id = '6121';
INSERT INTO ProfitAndLossItems ( id, name_en, attrib, dc, type, doc ) VALUES ( '6121', 'Põhivara kulum', NULL, 'C', NULL, NULL );
SELECT id, name_en, attrib, dc, type, doc FROM ProfitAndLossItems WHERE id = '613';
INSERT INTO ProfitAndLossItems ( id, name_en, attrib, dc, type, doc ) VALUES ( '613', 'Muud ärikulud', NULL, 'C', NULL, NULL );
SELECT id, name_en, attrib, dc, type, doc FROM ProfitAndLossItems WHERE id = '62';
INSERT INTO ProfitAndLossItems ( id, name_en, attrib, dc, type, doc ) VALUES ( '62', 'Finantskulud', NULL, 'C', NULL, NULL );
SELECT id, name_en, attrib, dc, type, doc FROM ProfitAndLossItems WHERE id = '63';
INSERT INTO ProfitAndLossItems ( id, name_en, attrib, dc, type, doc ) VALUES ( '63', 'Ärikasum (-kahjum)', NULL, 'C', NULL, NULL );
/* commit */
SELECT nation_id, id, name, zipCode, inhabitants FROM Cities WHERE name = 'Eupen';
SELECT nation_id, id, name, zipCode, inhabitants FROM Cities WHERE name = 'Verviers';
SELECT nation_id, id, name, zipCode, inhabitants FROM Cities WHERE name = 'Tallinn';
SELECT nation_id, id, name, zipCode, inhabitants FROM Cities WHERE name = 'Aachen';
SELECT MAX(id) FROM Partners;
INSERT INTO Partners ( id, name, firstName, email, phone, gsm, fax, website, nation_id, city_nation_id, city_id, zip, street, house, box, type_id, title, logo, lang_id, currency_id ) VALUES ( 1, 'Saffre', 'Luc', 'luc.saffre@gmx.net', '6376783', NULL, NULL, NULL, 'ee', 'ee', 1, NULL, NULL, NULL, NULL, NULL, 'Herrn', NULL, NULL, NULL );
INSERT INTO Partners ( id, name, firstName, email, phone, gsm, fax, website, nation_id, city_nation_id, city_id, zip, street, house, box, type_id, title, logo, lang_id, currency_id ) VALUES ( 2, 'Arens', 'Andreas', 'andreas@arens.be', '087.55.66.77', NULL, NULL, NULL, 'be', 'be', 3, NULL, NULL, NULL, NULL, NULL, 'Herrn', NULL, NULL, NULL );
INSERT INTO Partners ( id, name, firstName, email, phone, gsm, fax, website, nation_id, city_nation_id, city_id, zip, street, house, box, type_id, title, logo, lang_id, currency_id ) VALUES ( 3, 'Ausdemwald', 'Anton', 'ausdem@kotmail.com', NULL, NULL, NULL, NULL, 'de', 'de', 1, NULL, NULL, NULL, NULL, NULL, 'Herrn', NULL, NULL, NULL );
INSERT INTO Partners ( id, name, firstName, email, phone, gsm, fax, website, nation_id, city_nation_id, city_id, zip, street, house, box, type_id, title, logo, lang_id, currency_id ) VALUES ( 4, 'Bodard', 'Henri', NULL, NULL, NULL, NULL, NULL, 'be', 'be', 9, NULL, NULL, NULL, NULL, NULL, 'Dr.', NULL, NULL, NULL );
INSERT INTO Partners ( id, name, firstName, email, phone, gsm, fax, website, nation_id, city_nation_id, city_id, zip, street, house, box, type_id, title, logo, lang_id, currency_id ) VALUES ( 5, 'Eierschal', 'Emil', NULL, NULL, NULL, NULL, NULL, 'be', 'be', 3, NULL, NULL, NULL, NULL, NULL, 'Herrn', NULL, NULL, NULL );
INSERT INTO Partners ( id, name, firstName, email, phone, gsm, fax, website, nation_id, city_nation_id, city_id, zip, street, house, box, type_id, title, logo, lang_id, currency_id ) VALUES ( 6, 'Eierschal', 'Erna', NULL, NULL, NULL, NULL, NULL, 'be', 'be', 3, NULL, NULL, NULL, NULL, NULL, 'Frau', NULL, NULL, NULL );
INSERT INTO Partners ( id, name, firstName, email, phone, gsm, fax, website, nation_id, city_nation_id, city_id, zip, street, house, box, type_id, title, logo, lang_id, currency_id ) VALUES ( 7, 'Großmann', 'Gerd', NULL, NULL, NULL, NULL, NULL, 'be', 'be', 3, NULL, NULL, NULL, NULL, NULL, 'Herrn', NULL, NULL, NULL );
INSERT INTO Partners ( id, name, firstName, email, phone, gsm, fax, website, nation_id, city_nation_id, city_id, zip, street, house, box, type_id, title, logo, lang_id, currency_id ) VALUES ( 8, 'Freitag', 'Frédéric', NULL, NULL, NULL, NULL, NULL, 'be', 'be', 3, NULL, NULL, NULL, NULL, NULL, 'Herrn', NULL, NULL, NULL );
INSERT INTO Partners ( id, name, firstName, email, phone, gsm, fax, website, nation_id, city_nation_id, city_id, zip, street, house, box, type_id, title, logo, lang_id, currency_id ) VALUES ( 9, 'Rumma & Ko OÜ', NULL, NULL, NULL, NULL, NULL, NULL, 'ee', 'ee', 1, '10115', 'Tartu mnt.', 71, '5', NULL, NULL, NULL, NULL, NULL );
INSERT INTO Partners ( id, name, firstName, email, phone, gsm, fax, website, nation_id, city_nation_id, city_id, zip, street, house, box, type_id, title, logo, lang_id, currency_id ) VALUES ( 10, 'Girf OÜ', NULL, NULL, NULL, NULL, NULL, NULL, 'ee', 'ee', 1, '10621', 'Laki', 16, NULL, NULL, NULL, NULL, NULL, NULL );
INSERT INTO Partners ( id, name, firstName, email, phone, gsm, fax, website, nation_id, city_nation_id, city_id, zip, street, house, box, type_id, title, logo, lang_id, currency_id ) VALUES ( 11, 'PAC Systems PGmbH', NULL, NULL, NULL, NULL, NULL, NULL, 'be', 'be', 3, '4700', 'Hütte', 79, NULL, NULL, NULL, NULL, NULL, NULL );
INSERT INTO Partners ( id, name, firstName, email, phone, gsm, fax, website, nation_id, city_nation_id, city_id, zip, street, house, box, type_id, title, logo, lang_id, currency_id ) VALUES ( 12, 'Eesti Telefon', NULL, NULL, NULL, NULL, NULL, NULL, 'ee', 'ee', 1, '13415', 'Sõpruse pst.', 193, NULL, NULL, NULL, NULL, NULL, NULL );
SELECT id, name_en FROM Currencies WHERE id = 'BEF';
SELECT id, name_en FROM Currencies WHERE id = 'BEF';
SELECT id, name_en, area, population, curr, isocode FROM Nations WHERE id = 'be';
SELECT id, name_en, area, population, curr, isocode FROM Nations WHERE id = 'be';
SELECT id, name, firstName, email, phone, gsm, fax, website, nation_id, city_nation_id, city_id, zip, street, house, box, type_id, title, logo, lang_id, currency_id FROM Partners WHERE nation_id = 'be';
UPDATE Partners SET id = 2, name = 'Arens', firstName = 'Andreas', email = 'andreas@arens.be', phone = '087.55.66.77', gsm = NULL, fax = NULL, website = NULL, nation_id = 'be', city_nation_id = 'be', city_id = 3, zip = NULL, street = NULL, house = NULL, box = NULL, type_id = NULL, title = 'Herrn', logo = NULL, lang_id = NULL, currency_id = 'BEF' WHERE id = 2;


