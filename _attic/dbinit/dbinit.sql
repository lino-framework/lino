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


DROP TABLE IF EXISTS LANG;
CREATE TABLE LANG (
  id      CHAR(2) PRIMARY KEY NOT NULL,
  name_en    VARCHAR(60)
);

-- ISO 639 2-letter codes

INSERT INTO LANG VALUES ("AA", "Afar");
INSERT INTO LANG VALUES ("AB", "Abkhazian");
INSERT INTO LANG VALUES ("AF", "Afrikaans");
INSERT INTO LANG VALUES ("AM", "Amharic");
INSERT INTO LANG VALUES ("AR", "Arabic");
INSERT INTO LANG VALUES ("AS", "Assamese");
INSERT INTO LANG VALUES ("AY", "Aymara");
INSERT INTO LANG VALUES ("AZ", "Azerbaijani");
INSERT INTO LANG VALUES ("BA", "Bashkir");
INSERT INTO LANG VALUES ("BE", "Byelorussian");
INSERT INTO LANG VALUES ("BG", "Bulgarian");
INSERT INTO LANG VALUES ("BH", "Bihari");
INSERT INTO LANG VALUES ("BI", "Bislama");
INSERT INTO LANG VALUES ("BN", "Bengali/ Bangla");
INSERT INTO LANG VALUES ("BO", "Tibetan");
INSERT INTO LANG VALUES ("BR", "Breton");
INSERT INTO LANG VALUES ("CA", "Catalan");
INSERT INTO LANG VALUES ("CO", "Corsican");
INSERT INTO LANG VALUES ("CS", "Czech");
INSERT INTO LANG VALUES ("CY", "Welsh");
INSERT INTO LANG VALUES ("DA", "Danish");
INSERT INTO LANG VALUES ("DE", "German");
INSERT INTO LANG VALUES ("DZ", "Bhutani");
INSERT INTO LANG VALUES ("EL", "Greek");
INSERT INTO LANG VALUES ("EN", "English");
INSERT INTO LANG VALUES ("EO", "Esperanto");
INSERT INTO LANG VALUES ("ES", "Spanish");
INSERT INTO LANG VALUES ("ET", "Estonian");
INSERT INTO LANG VALUES ("EU", "Basque");
INSERT INTO LANG VALUES ("FA", "Persian");
INSERT INTO LANG VALUES ("FI", "Finnish");
INSERT INTO LANG VALUES ("FJ", "Fiji");
INSERT INTO LANG VALUES ("FO", "Faeroese");
INSERT INTO LANG VALUES ("FR", "French");
INSERT INTO LANG VALUES ("FY", "Frisian");
INSERT INTO LANG VALUES ("GA", "Irish");
INSERT INTO LANG VALUES ("GD", "Gaelic / Scots Gaelic");
INSERT INTO LANG VALUES ("GL", "Galician");
INSERT INTO LANG VALUES ("GN", "Guarani");
INSERT INTO LANG VALUES ("GU", "Gujarati");
INSERT INTO LANG VALUES ("HA", "Hausa");
INSERT INTO LANG VALUES ("HI", "Hindi");
INSERT INTO LANG VALUES ("HR", "Croatian");
INSERT INTO LANG VALUES ("HU", "Hungarian");
INSERT INTO LANG VALUES ("HY", "Armenian");
INSERT INTO LANG VALUES ("IA", "Interlingua");
INSERT INTO LANG VALUES ("IE", "Interlingue");
INSERT INTO LANG VALUES ("IK", "Inupiak");
INSERT INTO LANG VALUES ("IN", "Indonesian");
INSERT INTO LANG VALUES ("IS", "Icelandic");
INSERT INTO LANG VALUES ("IT", "Italian");
INSERT INTO LANG VALUES ("IW", "Hebrew");
INSERT INTO LANG VALUES ("JA", "Japanese");
INSERT INTO LANG VALUES ("JI", "Yiddish");
INSERT INTO LANG VALUES ("JW", "Javanese");
INSERT INTO LANG VALUES ("KA", "Georgian");
INSERT INTO LANG VALUES ("KK", "Kazakh");
INSERT INTO LANG VALUES ("KL", "Greenlandic");
INSERT INTO LANG VALUES ("KM", "Cambodian");
INSERT INTO LANG VALUES ("KN", "Kannada");
INSERT INTO LANG VALUES ("KO", "Korean");
INSERT INTO LANG VALUES ("KS", "Kashmiri");
INSERT INTO LANG VALUES ("KU", "Kurdish");
INSERT INTO LANG VALUES ("KY", "Kirghiz");
INSERT INTO LANG VALUES ("LA", "Latin");
INSERT INTO LANG VALUES ("LN", "Lingala");
INSERT INTO LANG VALUES ("LO", "Laothian");
INSERT INTO LANG VALUES ("LT", "Lithuanian");
INSERT INTO LANG VALUES ("LV", "Latvian / Lettish");
INSERT INTO LANG VALUES ("MG", "Malagasy");
INSERT INTO LANG VALUES ("MI", "Maori");
INSERT INTO LANG VALUES ("MK", "Macedonian");
INSERT INTO LANG VALUES ("ML", "Malayalam");
INSERT INTO LANG VALUES ("MN", "Mongolian");
INSERT INTO LANG VALUES ("MO", "Moldavian");
INSERT INTO LANG VALUES ("MR", "Marathi");
INSERT INTO LANG VALUES ("MS", "Malay");
INSERT INTO LANG VALUES ("MT", "Maltese");
INSERT INTO LANG VALUES ("MY", "Burmese");
INSERT INTO LANG VALUES ("NA", "Nauru");
INSERT INTO LANG VALUES ("NE", "Nepali");
INSERT INTO LANG VALUES ("NL", "Dutch");
INSERT INTO LANG VALUES ("NO", "Norwegian");
INSERT INTO LANG VALUES ("OC", "Occitan");
INSERT INTO LANG VALUES ("OM", "Oromo / Afan");
INSERT INTO LANG VALUES ("OR", "Oriya");
INSERT INTO LANG VALUES ("PA", "Punjabi");
INSERT INTO LANG VALUES ("PL", "Polish");
INSERT INTO LANG VALUES ("PS", "Pashto / Pushto");
INSERT INTO LANG VALUES ("PT", "Portuguese");
INSERT INTO LANG VALUES ("QU", "Quechua");
INSERT INTO LANG VALUES ("RM", "Rhaeto-Romance");
INSERT INTO LANG VALUES ("RN", "Kirundi");
INSERT INTO LANG VALUES ("RO", "Romanian");
INSERT INTO LANG VALUES ("RU", "Russian");
INSERT INTO LANG VALUES ("RW", "Kinyarwanda");
INSERT INTO LANG VALUES ("SA", "Sanskrit");
INSERT INTO LANG VALUES ("SD", "Sindhi");
INSERT INTO LANG VALUES ("SG", "Sangro");
INSERT INTO LANG VALUES ("SH", "Serbo-Croatian");
INSERT INTO LANG VALUES ("SI", "Singhalese");
INSERT INTO LANG VALUES ("SK", "Slovak");
INSERT INTO LANG VALUES ("SL", "Slovenian");
INSERT INTO LANG VALUES ("SM", "Samoan");
INSERT INTO LANG VALUES ("SN", "Shona");
INSERT INTO LANG VALUES ("SO", "Somali");
INSERT INTO LANG VALUES ("SQ", "Albanian");
INSERT INTO LANG VALUES ("SR", "Serbian");
INSERT INTO LANG VALUES ("SS", "Siswati");
INSERT INTO LANG VALUES ("ST", "Sesotho");
INSERT INTO LANG VALUES ("SU", "Sudanese");
INSERT INTO LANG VALUES ("SV", "Swedish");
INSERT INTO LANG VALUES ("SW", "Swahili");
INSERT INTO LANG VALUES ("TA", "Tamil");
INSERT INTO LANG VALUES ("TE", "Tegulu");
INSERT INTO LANG VALUES ("TG", "Tajik");
INSERT INTO LANG VALUES ("TH", "Thai");
INSERT INTO LANG VALUES ("TI", "Tigrinya");
INSERT INTO LANG VALUES ("TK", "Turkmen");
INSERT INTO LANG VALUES ("TL", "Tagalog");
INSERT INTO LANG VALUES ("TN", "Setswana");
INSERT INTO LANG VALUES ("TO", "Tonga");
INSERT INTO LANG VALUES ("TR", "Turkish");
INSERT INTO LANG VALUES ("TS", "Tsonga");
INSERT INTO LANG VALUES ("TT", "Tatar");
INSERT INTO LANG VALUES ("TW", "Twi");
INSERT INTO LANG VALUES ("UK", "Ukrainian");
INSERT INTO LANG VALUES ("UR", "Urdu");
INSERT INTO LANG VALUES ("UZ", "Uzbek");
INSERT INTO LANG VALUES ("VI", "Vietnamese");
INSERT INTO LANG VALUES ("VO", "Volapuk");
INSERT INTO LANG VALUES ("WO", "Wolof");
INSERT INTO LANG VALUES ("XH", "Xhosa");
INSERT INTO LANG VALUES ("YO", "Yoruba");
INSERT INTO LANG VALUES ("ZH", "Chinese");
INSERT INTO LANG VALUES ("ZU", "Zulu");




DROP TABLE IF EXISTS NATIONS;
CREATE TABLE NATIONS (
  id      CHAR(2) PRIMARY KEY NOT NULL,
  name_en VARCHAR(60),
  name_de VARCHAR(60),
  name_fr VARCHAR(60),
  name_ee VARCHAR(60)
);

INSERT INTO NATIONS VALUES
       ("ee","Estonia","Estland","Estonie","Eesti");
INSERT INTO NATIONS VALUES
       ("be","Belgium","Belgien","Belgique","Belgia");
INSERT INTO NATIONS VALUES
       ("de","Germany","Deutschland","Allemagne","Saksamaa");
INSERT INTO NATIONS VALUES
       ("fr","France","Frankreich","France","Prantsusmaa");

DROP TABLE IF EXISTS NATIONS_ISO;
CREATE TABLE NATIONS_ISO (
  id      CHAR(3) PRIMARY KEY NOT NULL,
  name_en VARCHAR(60),
  name_de VARCHAR(60),
  name_fr VARCHAR(60),
  name_ee VARCHAR(60)
);

INSERT INTO NATIONS_ISO VALUES ("AFG","Afghanistan",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("ALB","Albania",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("DZA","Algeria",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("ASM","American Samoa",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("AND","Andorra",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("AGO","Angola",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("AIA","Anguilla",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("ATA","Antarctica",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("ATG","Antigua and Barbuda",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("ARG","Argentina",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("ARM","Armenia",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("ABW","Aruba",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("AUS","Australia",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("AUT","Austria",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("AZE","Azerbaijan",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("BHR","Bahrain",NULL,NULL,NULL);
-- INSERT INTO NATIONS_ISO VALUES ("UMI","Baker Island",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("BGD","Bangladesh",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("BRB","Barbados",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("BLR","Belarus",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("BEL","Belgium",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("BLZ","Belize",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("BEN","Benin",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("BMU","Bermuda",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("BTN","Bhutan",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("BOL","Bolivia",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("BIH","Bosnia and Herzegovina",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("BWA","Botswana",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("BVT","Bouvet Island",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("BRA","Brazil",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("IOT","British Indian Ocean Territory",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("VGB","British Virgin Islands",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("BRN","Brunei",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("BGR","Bulgaria",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("BFA","Burkina Faso",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("MMR","Burma",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("BDI","Burundi",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("KHM","Cambodia",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("CMR","Cameroon",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("CAN","Canada",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("CPV","Cape Verde",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("CYM","Cayman Islands",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("CAF","Central African Republic",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("TCD","Chad",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("CHL","Chile",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("CHN","China",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("CXR","Christmas Island",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("CCK","Cocos (Keeling) Islands",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("COL","Colombia",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("COM","Comoros",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("ZAR","Congo, Democratic Republic of the",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("COG","Congo, Republic of the",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("COK","Cook Islands",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("CRI","Costa Rica",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("CIV","Cote d'Ivoire",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("HRV","Croatia",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("CUB","Cuba",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("CYP","Cyprus",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("CZE","Czech Republic",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("DNK","Denmark",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("DJI","Djibouti",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("DMA","Dominica",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("DOM","Dominican Republic",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("ECU","Ecuador",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("EGY","Egypt",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("SLV","El Salvador",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("GNQ","Equatorial Guinea",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("ERI","Eritrea",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("EST","Estonia",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("ETH","Ethiopia",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("FLK","Falkland Islands (Islas Malvinas)",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("FRO","Faroe Islands",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("FJI","Fiji",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("FIN","Finland",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("FRA","France",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("GUF","French Guiana",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("PYF","French Polynesia",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("ATF","French Southern and Antarctic Lands",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("GAB","Gabon",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("GEO","Georgia",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("DEU","Germany",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("GHA","Ghana",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("GIB","Gibraltar",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("GRC","Greece",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("GRL","Greenland",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("GRD","Grenada",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("GLP","Guadeloupe",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("GUM","Guam",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("GTM","Guatemala",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("GIN","Guinea",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("GNB","Guinea-Bissau",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("GUY","Guyana",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("HTI","Haiti",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("HMD","Heard Island and McDonald Islands",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("VAT","Holy See (Vatican City)",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("HND","Honduras",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("HKG","Hong Kong",NULL,NULL,NULL);
-- INSERT INTO NATIONS_ISO VALUES ("UMI","Howland Island",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("HUN","Hungary",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("ISL","Iceland",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("IND","India",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("IDN","Indonesia",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("IRN","Iran",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("IRQ","Iraq",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("IRL","Ireland",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("ISR","Israel",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("ITA","Italy",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("JAM","Jamaica",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("JPN","Japan",NULL,NULL,NULL);
-- INSERT INTO NATIONS_ISO VALUES ("UMI","Jarvis Island",NULL,NULL,NULL);
-- INSERT INTO NATIONS_ISO VALUES ("UMI","Johnston Atoll",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("JOR","Jordan",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("KAZ","Kazakhstan",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("KEN","Kenya",NULL,NULL,NULL);
-- INSERT INTO NATIONS_ISO VALUES ("UMI","Kingman Reef",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("KIR","Kiribati",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("PRK","Korea, North",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("KOR","Korea, South",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("KWT","Kuwait",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("KGZ","Kyrgyzstan",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("LAO","Laos",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("LVA","Latvia",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("LBN","Lebanon",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("LSO","Lesotho",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("LBR","Liberia",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("LBY","Libya",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("LIE","Liechtenstein",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("LTU","Lithuania",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("LUX","Luxembourg",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("MAC","Macau",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("MKD","Macedonia, The Former Yugoslav Republic of",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("MDG","Madagascar",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("MWI","Malawi",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("MYS","Malaysia",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("MDV","Maldives",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("MLI","Mali",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("MLT","Malta",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("MHL","Marshall Islands",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("MTQ","Martinique",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("MRT","Mauritania",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("MUS","Mauritius",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("MYT","Mayotte",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("MEX","Mexico",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("FSM","Micronesia, Federated States of",NULL,NULL,NULL);
-- INSERT INTO NATIONS_ISO VALUES ("UMI","Midway Islands",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("MDA","Moldova",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("MCO","Monaco",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("MNG","Mongolia",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("MSR","Montserrat",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("MAR","Morocco",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("MOZ","Mozambique",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("NAM","Namibia",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("NRU","Nauru",NULL,NULL,NULL);
-- INSERT INTO NATIONS_ISO VALUES ("UMI","Navassa Island",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("NPL","Nepal",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("NLD","Netherlands",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("ANT","Netherlands Antilles",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("NCL","New Caledonia",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("NZL","New Zealand",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("NIC","Nicaragua",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("NER","Niger",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("NGA","Nigeria",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("NIU","Niue",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("NFK","Norfolk Island",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("MNP","Northern Mariana Islands",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("NOR","Norway",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("OMN","Oman",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("PAK","Pakistan",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("PLW","Palau",NULL,NULL,NULL);
-- INSERT INTO NATIONS_ISO VALUES ("UMI","Palmyra Atoll",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("PAN","Panama",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("PNG","Papua New Guinea",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("PRY","Paraguay",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("PER","Peru",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("PHL","Philippines",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("PCN","Pitcairn Islands",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("POL","Poland",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("PRT","Portugal",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("PRI","Puerto Rico",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("QAT","Qatar",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("REU","Reunion",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("ROM","Romania",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("RUS","Russia",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("RWA","Rwanda",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("SHN","Saint Helena",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("KNA","Saint Kitts and Nevis",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("LCA","Saint Lucia",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("SPM","Saint Pierre and Miquelon",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("VCT","Saint Vincent and the Grenadines",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("WSM","Samoa",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("SMR","San Marino",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("STP","Sao Tome and Principe",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("SAU","Saudi Arabia",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("SEN","Senegal",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("SYC","Seychelles",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("SLE","Sierra Leone",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("SGP","Singapore",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("SVK","Slovakia",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("SVN","Slovenia",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("SLB","Solomon Islands",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("SOM","Somalia",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("ZAF","South Africa",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("SGS","South Georgia and the South Sandwich Islands",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("ESP","Spain",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("LKA","Sri Lanka",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("SDN","Sudan",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("SUR","Suriname",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("SJM","Svalbard",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("SWZ","Swaziland",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("SWE","Sweden",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("CHE","Switzerland",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("SYR","Syria",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("TWN","Taiwan",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("TJK","Tajikistan",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("TZA","Tanzania",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("THA","Thailand",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("BHS","The Bahamas",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("GMB","The Gambia",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("TGO","Togo",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("TKL","Tokelau",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("TON","Tonga",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("TTO","Trinidad and Tobago",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("TUN","Tunisia",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("TUR","Turkey",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("TKM","Turkmenistan",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("TCA","Turks and Caicos Islands",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("TUV","Tuvalu",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("UGA","Uganda",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("UKR","Ukraine",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("ARE","United Arab Emirates",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("GBR","United Kingdom",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("USA","United States",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("URY","Uruguay",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("UZB","Uzbekistan",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("VUT","Vanuatu",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("VEN","Venezuela",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("VNM","Vietnam",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("VIR","Virgin Islands",NULL,NULL,NULL);
-- INSERT INTO NATIONS_ISO VALUES ("UMI","Wake Island",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("WLF","Wallis and Futuna",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("ESH","Western Sahara",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("YEM","Yemen",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("ZMB","Zambia",NULL,NULL,NULL);
INSERT INTO NATIONS_ISO VALUES ("ZWE","Zimbabwe",NULL,NULL,NULL);

DROP TABLE IF EXISTS ORG;
CREATE TABLE ORG (
  id BIGINT PRIMARY KEY NOT NULL,
  name  VARCHAR(60),
  parent BIGINT
);
INSERT INTO ORG VALUES (1,'Lino Partners',NULL);
INSERT INTO ORG VALUES (2,'Girf OÜ',1);
INSERT INTO ORG VALUES (3,'Rumma & Ko OÜ',1);
INSERT INTO ORG VALUES (4,'PAC Systems PGmbH',1);
INSERT INTO ORG VALUES (5,'Microsoft',NULL);
INSERT INTO ORG VALUES (6,'Eesti Telefon',NULL);


DROP TABLE IF EXISTS PERS;
CREATE TABLE PERS (
  id BIGINT PRIMARY KEY AUTO_INCREMENT NOT NULL,
  title  VARCHAR(30),
  fname  VARCHAR(30),
  name   VARCHAR(60)
);
INSERT INTO PERS VALUES (1,NULL,'Luc','Saffre');
INSERT INTO PERS VALUES (2,NULL,'Andres','Anier');
INSERT INTO PERS VALUES (3,NULL,'Paul','Antys');
INSERT INTO PERS VALUES (4,NULL,'Bill','Gates');
INSERT INTO PERS VALUES (5,NULL,'Hannes','Plinte');
INSERT INTO PERS VALUES (6,NULL,'Marko','Aid');


DROP TABLE IF EXISTS SLOTS;
CREATE TABLE SLOTS (
  id BIGINT PRIMARY KEY AUTO_INCREMENT NOT NULL,
  pers   BIGINT, -- ref to PERS
  org    BIGINT, -- ref to ORG
  type  VARCHAR(10),
  slot  VARCHAR(60)
);

INSERT INTO SLOTS VALUES (NULL,2,2,'email','andres@girf.ee');
INSERT INTO SLOTS VALUES (NULL,3,4,'email','paul.antys@pacsystems.be');
INSERT INTO SLOTS VALUES (NULL,3,4,'phone','087.59.35.50');
INSERT INTO SLOTS VALUES (NULL,1,3,'email','luc.saffre@gmx.net');
INSERT INTO SLOTS VALUES (NULL,1,3,'phone','6376783');
INSERT INTO SLOTS VALUES (NULL,NULL,2,'url','http://www.girf.ee');
INSERT INTO SLOTS VALUES (NULL,NULL,4,'url','http://www.pacsystems.be');



DROP TABLE IF EXISTS CITIES;
CREATE TABLE CITIES (
  id      BIGINT PRIMARY KEY AUTO_INCREMENT NOT NULL,
  nation  CHAR(3) NOT NULL,
  name    VARCHAR(60)
);

INSERT INTO CITIES VALUES (1,"ee","Tallinn");
INSERT INTO CITIES VALUES (2,"ee","Tartu");
INSERT INTO CITIES VALUES (3,"ee","Otepää");
INSERT INTO CITIES VALUES (4,"ee","Narva");
INSERT INTO CITIES VALUES (5,"ee","Kilingi-Nõmme");
INSERT INTO CITIES VALUES (6,"ee","Pärnu");
INSERT INTO CITIES VALUES (7,"ee","Rakvere");
INSERT INTO CITIES VALUES (8,"ee","Viljandi");
INSERT INTO CITIES VALUES (9,"ee","Ruhnu");
INSERT INTO CITIES VALUES (10,"ee","Vigala");
                           
INSERT INTO CITIES VALUES (11,"be","Bruxelles");
INSERT INTO CITIES VALUES (12,"be","Brugge");
INSERT INTO CITIES VALUES (13,"be","Eupen");
INSERT INTO CITIES VALUES (14,"be","Kettenis");
INSERT INTO CITIES VALUES (15,"be","Kelmis");
INSERT INTO CITIES VALUES (16,"be","Raeren");
INSERT INTO CITIES VALUES (17,"be","Mons");
INSERT INTO CITIES VALUES (18,"be","Liège");
INSERT INTO CITIES VALUES (19,"be","Charleroi");





DROP TABLE IF EXISTS ADDR;
CREATE TABLE ADDR (
  id BIGINT PRIMARY KEY AUTO_INCREMENT NOT NULL,
  pers   BIGINT, -- ref to PERS
  org    BIGINT, -- ref to ORG
  -- email  VARCHAR(60),
  nation CHAR(3), -- ref to NATIONS
  city   BIGINT,  -- ref to CITIES
  zip    VARCHAR(10),
  street VARCHAR(80),
  house  INT,
  box    VARCHAR(10)
  -- tel    VARCHAR(30),
  -- fax    VARCHAR(30)
);


INSERT INTO ADDR VALUES
       (NULL,2,2, "ee",1,'10621', "Laki",16,NULL);
INSERT INTO ADDR VALUES
       (NULL,3,4, "be",13,'4700', "Hütte",79,NULL);
INSERT INTO ADDR VALUES
       (NULL,1,3, "ee",1,'10115', "Tartu mnt.",71,'-5');
INSERT INTO ADDR VALUES
       (NULL,NULL,6, "ee",1,'13415', "Sõpruse pst",193,'-5');


DROP TABLE IF EXISTS ORG2ORG;
CREATE TABLE ORG2ORG (
  id1      BIGINT   NOT NULL,
  id2      BIGINT   NOT NULL
);

INSERT INTO ORG2ORG VALUES (1,2);
INSERT INTO ORG2ORG VALUES (1,3);
INSERT INTO ORG2ORG VALUES (1,4);


DROP TABLE IF EXISTS ORG2PERS;
CREATE TABLE ORG2PERS (
  id1      BIGINT   NOT NULL,
  id2      BIGINT   NOT NULL,
  note     VARCHAR(60)
);

INSERT INTO ORG2PERS VALUES (1,1,'Lino author');
INSERT INTO ORG2PERS VALUES (3,1,'2001-2002');
INSERT INTO ORG2PERS VALUES (4,1,'1991-2001');
INSERT INTO ORG2PERS VALUES (2,2,NULL);
INSERT INTO ORG2PERS VALUES (2,5,NULL);
INSERT INTO ORG2PERS VALUES (2,6,NULL);
INSERT INTO ORG2PERS VALUES (4,3,NULL);
INSERT INTO ORG2PERS VALUES (5,4,NULL);

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
  project   BIGINT, -- ref to PROJECTS
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
  date      DATE,
  title     VARCHAR(80),
  major     INT NOT NULL,
  minor     INT NOT NULL,
  release   INT NOT NULL
);

INSERT INTO FILES (body, abstract, id, title) VALUES (NULL, NULL, "datadict.inc.php", "Data Dictionary");
INSERT INTO FILES (body, abstract, id, title) VALUES (NULL, NULL, "lino.inc.php", "Lino main include file");
INSERT INTO FILES (body, abstract, id, title) VALUES (NULL, NULL, "html.inc.php", "HTML rendering");
INSERT INTO FILES (body, abstract, id, title) VALUES (NULL, "Instantiates a Query, translates the URL parameters to Query
settings, then renders this query.
", "render.php", "render the specified query");
INSERT INTO CLASSES (body, file, title, abstract, super, id) VALUES (NULL, "datadict.inc.php", "Base class for data type descriptors", NULL, NULL, "Type");
INSERT INTO CLASSES (body, file, title, abstract, super, id) VALUES (NULL, "datadict.inc.php", "type-specific methods for values of type CHAR or VARCHAR", NULL, "Type", "TextType");
INSERT INTO CLASSES (body, file, title, abstract, super, id) VALUES (NULL, "datadict.inc.php", "type-specific methods for values of type INT or BIGINT", NULL, "Type", "IntType");
INSERT INTO CLASSES (body, file, title, abstract, super, id) VALUES (NULL, "datadict.inc.php", "type-specific methods for values of type TEXT", NULL, "TextType", "MemoType");
INSERT INTO CLASSES (body, file, title, abstract, super, id) VALUES (NULL, "datadict.inc.php", "A named set of columns on a master table", "Views are the part of a query
which can be modified and saved.
A View contains an ordererd set of columns.
A View is valid for one known master table.
", NULL, "View");
INSERT INTO CLASSES (body, file, title, abstract, super, id) VALUES (NULL, "datadict.inc.php", "Query", NULL, NULL, "Query");
INSERT INTO CLASSES (body, file, title, abstract, super, id) VALUES (NULL, "datadict.inc.php", "a field in a Table", NULL, NULL, "Table");
INSERT INTO CLASSES (body, file, title, abstract, super, id) VALUES (NULL, "datadict.inc.php", "a field in a Table", NULL, NULL, "Field");
INSERT INTO CLASSES (body, file, title, abstract, super, id) VALUES (NULL, "datadict.inc.php", "a field in a Table", NULL, NULL, "Detail");
INSERT INTO CLASSES (body, file, title, abstract, super, id) VALUES (NULL, "datadict.inc.php", "(abstract) the element of a View", NULL, NULL, "Column");
INSERT INTO CLASSES (body, file, title, abstract, super, id) VALUES (NULL, "datadict.inc.php", "a column representing a Field", NULL, "Column", "FieldColumn");
INSERT INTO CLASSES (body, file, title, abstract, super, id) VALUES (NULL, "datadict.inc.php", "a column representing a Detail", NULL, "Column", "DetailColumn");
INSERT INTO CLASSES (body, file, title, abstract, super, id) VALUES (NULL, "datadict.inc.php", "a column representing a joined table", NULL, "FieldColumn", "JoinFieldColumn");
INSERT INTO CLASSES (body, file, title, abstract, super, id) VALUES (NULL, "datadict.inc.php", "(abstract) base class for Lino modules", NULL, NULL, "Module");
INSERT INTO CLASSES (body, file, title, abstract, super, id) VALUES (NULL, "apidoc.inc.php", "API documentation", NULL, "Module", "APIDOC");
INSERT INTO CLASSES (body, file, title, abstract, super, id) VALUES (NULL, "crm.inc.php", "Addressbook", NULL, "Module", "ADDBOOK");
INSERT INTO METHODS (body, class, abstract, name, title) VALUES (NULL, "Query", NULL, "Render", "Execute the query and output the data");
INSERT INTO METHODS (body, class, abstract, name, title) VALUES (NULL, "Query", NULL, "GetDefaultDetailDepth", NULL);
INSERT INTO METHODS (body, class, abstract, name, title) VALUES (NULL, "MemoType", NULL, "ShowValue", "Show a value of type memo");
INSERT INTO METHODS (body, class, abstract, name, title) VALUES (NULL, "JoinFieldColumn", NULL, "Render", "output the value of this column in current row");
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES ("This property does not depend on the renderer.
Removed class EditRender (editing capacity is now in the query).

<p>", "2002-06-04.", 1, 0,0,9, "You can now switch on or off the isEditing property of a query.
", "updating data", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES (NULL, "2002-06-04.", 1, 0,0,9, "I splitted the navigator into its components:
Format Selector, Navigator, Quick Filter, View Editor, and the new
Editing toggle.
", "Navigator components", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES (NULL, "2002-06-05", 1, 0,0,9, "Detail->ShowRenderer : if masterId is NULL, don't try
to display details.
", NULL, NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES (NULL, "2002-06-05", 1, 0,0,9, "This [edit] button links to a page where this detail is displayed as
main component and thus editable.
", "A Detail now shows an [edit] button.", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES (NULL, "2002-06-05", 1, 0,0,9, "\"reusing\" a Query which isEditing() would mean that it would be possible
to save the data in an edited form without submitting it. This is
currently not possible. If you edit data in a form, then forget to
click the submit button, your changes are simply lost.
", NULL, NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES ("The primary key is a column who canEdit(), but in practice this
editor is readonly on all existing rows. You can modify the primary
key only on a new row.

<p>This use of readonly editors is necessary if there is more than one
row in the form. There must be an editor for each row in the form,
otherwise the update method gets messed because the arrays are not all
of same length. 

<p>", "2002-06-05", 1, 0,0,9, "There is a difference between canEdit() and IsReadOnly(). A column who
canEdit() *must* canEdit() for each row. But IsReadOnly() is allowed
to change from row to row.
", "canEdit() and isReadOnly()", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES (NULL, "2002-06-05", 1, 0,0,9, "At least in queries without SetRngKey().
<br>TODO: if Query->SetRngKey() are set, canEdit()
for these columns must return FALSE. And CreateRow() must fill them
with the correct SetRngVal().
", "Updating and inserting rows works now.", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES (NULL, "2002-06-05", 1, 0,0,9, "Renderer->OnHeader() is back. It was *not* useless: difference between
OnHeader() and OnRow() with if($first) is that the latter will be
executed only if there is at least one row.
", NULL, NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES (NULL, "2002-06-05", 1, 0,0,9, "I am developing my debugging techniques...
It is now possible to start Lino using
<?= urlref(\"index.php?debug=1&verbose=2&meth=reset\")?>.
<tt>meth=reset</tt> works on any page
(which includes lino.php)
and causes a new session to be started.
", NULL, NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES (NULL, "2002-06-06", 1, 0,0,9, "source.php had a bug. This was the first bug
discovered by somebody else than the author.
", NULL, NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES (NULL, "2002-06-06", 1, 0,0,9, "Looking for a solution to the circular references
problem in datadict...
<li>http://www.ideenreich.com/php/methoden.shtml
<li>http://php.planetmirror.com/manual/en/language.oop.serialization.php
", NULL, NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES ("<li>http://ee.php.net/manual/en/language.references.pass.php:

<p>Note that there's no reference sign on function call - only on function definition. Function definition alone is enough to correctly pass the argument by reference. 

<p>", "2002-06-07", 1, 0,0,9, "Continued: circular or bi-directional references in datadict...
<li>http://ee.php.net/manual/en/language.references.arent.php
<li>http://www.digiways.com/articles/php/smartcompare/
", NULL, NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES ("Reference problem: PHP is very sticky in making copies of objects. Lino
initialized the data dictionary, but then suddenly some parts were
again un-initialized. Because in fact a copy had been initialized. And
there were in fact a lot of unnecessary copies in the session
data. The is_ref() function (original name comparereferences() by Val
Samko, http://www.digiways.com/articles/php/smartcompare/ ) finally
helped me out of this.

<p>One big background change :
the user-code interface is completely new.
Look at index.php

<p><ul>
<li>Before :
<pre>
&lt;li>Addressbook : 
&lt;?= $ADDRBOOK->PERS->ShowViewRef()?>,
</pre>

<p><li>Now:
<pre>
&ltli>Addressbook :
&lt?= ShowQueryRef('PERS')?>,
</pre>
</ul>

<p>", "2002-06-08", 1, 0,0,9, "I worked almost two
full days on a frustrating reference problem.
One big background change:
the user-code interface is completely new.
", "Release 0.0.7 is ready.", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES ("A \"slot\" is one of the following: phone or fax number, email
adress, url, ...

<p><pre>
class SLOTS extends Table {

<p>  function init() {
    $this->AddIntField('id','ID');
    $this->AddTextField('type','Type');
    $this->AddTextField('slot','Slot');
    $this->label = 'Slots';
  }
  
  function GetRowLabel($query,$alias='') {
    $s = '';
    $s .= $query->row[$alias.'type'];
    $s .= ' ' . $query->row[$alias.'slot'];
    return $s;
  }
}
</pre>

<p>And later during ADDRBOOK::link():
<pre>
AddLink('SLOTS','pers','Person',
        'PERS','slots','Slots');
AddLink('SLOTS','org','Organisation',
        'ORG','slots','Slots');
</pre>
a slot knows its Person and/or Organisation.

<p>", "2002-06-09", 1, 0,0,9, "I modified the database structure for module ADDRBOOK.
", "New table \"SLOTS\"", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES (NULL, "2002-06-09", 1, 0,0,9, "I wrote pin2sql.py, a little Python script which converts a \"pinboard\"
file into SQL statements.  Result: my change log is now really in the
NEWS table.
", "pin2sql.py", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES ("pin2sql.py reads a Pinboard input file (from stdin, by default) and
outputs an SQL script which, if executed in MySQL, will create the
actual rows in the SQL database.

<p>I have now a dbinit.bat which does:
<pre>
python ..\pinboard\pin2sql.py < ..\pinboard\changes.pin > changes.sql
type sys.sql > dbinit.sql
type lang.sql >> dbinit.sql
type addrbook.sql >> dbinit.sql
type nations.sql >> dbinit.sql
type community.sql >> dbinit.sql
type changes.sql >> dbinit.sql
mysql %1 < dbinit.sql
</pre>

<p>The Pinboard format is inspired by RFC2822 (the format used for email
messages), but with flexible headers. Look at
[srcref pinboard/changes.pin]
and ask questions if you want...

<p>", "2002-06-10", 1, 0,0,9, "I re-wrote pin2sql.py, now it is worth to speak about it.
I invented the \"Pinboard\" format because I prefer Emacs to all other
user interfaces which i have seen so far.
", "pin2sql.py version 2", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES ("Results :
<ul>
<li>The Browser's Back Button now works as expected.
<li>[Close] and [Refresh] buttons are no longer necessary
</ul>

<p>Another advantage: you can now copy and paste a link to a certain view
since the query's state no longer depends on session data.

<p>TODO:
The update button is currently broken. 

<p>", "2002-06-10", 1, 0,0,9, "Release 0.0.8 had a bug in this.php.  The idea of this.php was to have
a \"current query\", that is, a Query instance stored in the session
data.  Now the current state of the Query is completely reflected in
each URL, and the Query instance is re-created for each page.
", "this.php no longer used", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES ("<ul>
<li>Table.ShowPeekRef($id,$label):
shows a link to a page where the row with the specified primary key
will be displayed.
Used for example
(1) to render a JoinFieldColumn (that is, a Column which
links to another table).
Or (2) as default implementation for Table.ShowInCommaList().

<p><li>Table.ShowInCommaList($query):
<li>Table.GetRowLabel($query,$alias=''):
</ul>

<p>", "2002-06-10", 1, 0,0,9, "There is still some chaos in this part of the API...
", "ShowPageRef(), ShowPeekRef()", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES (NULL, "2002-06-11", 1, 0,0,9, "Even though there is not much documentation, there were already some
seriously outdated things written in <a href=\"tour.php\">Le Tour de
Lino</a>.  There are probably more such things on other places.
", "Documentation outdated", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES ("<b>Notice</b>: Undefined property: editingRows
<br>in /home/luc/public_html/lino-0.0.8/datadict.php on line 2056

<p>A Query which is editing will now store itself into the session data
($_SESSION['editingQuery']) where update.php will take it out again.

<p>The Query->editingRows[] attribute is an array of the rows which have
been rendered with editors.

<p>There is currently no record locking mechanism. So, it two users ask
to edit the same data at the same time, you will have surprising
results. 

<p>", "2002-06-11", 1, 0,0,9, "Query updating was broken.  When you clicked on \"isEditing : [on]\",
you got only a run-time error.
", "Undefined property: editingRows", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES ("class Renderer renamed to HtmlRenderer.  HTML renderers
are now singleton objects in a global array $htmlRenderers
which maps the format name to the renderer instance.
Query->renderer no longer exists. Was used only in Query.Render().
Instead there is now again Query->format.
Query.Render() usually chooses the renderer by getting it from
$htmlRenderers. Exception:
if isset($HTTP_GET_VARS['xml']) (that is:
\"&xml\" was added to the URL (which is done if click on
the [XML] pseudo button)),
it always chooses the unique XmlRenderer.

<p>", "2002-06-12", 1, 0,0,9, "Some internal changes as preparation for XML support.
", "Renderers", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES ("This XML is probably not very valid.
I will wait a little bit for ideas
about how to continue...

<p>What is XSLT?
Interesting article about XSLT at
<? urlref('http://www.xml.com/pub/a/2000/08/holman/')?>.

<p>", "2002-06-12", 1, 0,0,9, "Now Lino gives XML output...
but you should probably ask
your browser to show the page's source.
", "Lino speaks XML", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES (NULL, "2002-06-12", 1, 0,0,9, "title.php: The togglers for $debug and $verbose
referenced still to this.php...
Now they work at least when you are on index.php.
On render.php for example they still don't work.
", "Setting debug level and verbosity", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES ("<b>Notice</b>: Undefined index: editingQuery
<br>in /home/luc/public_html/lino-0.0.9/update.php on line 7.

<p>This error is not reproduceable on my local installation (PHP
4.2.0). Perhaps somebody who knows PHP better than me finds the
reason?

<p>At the end of Query.ShowRef()
(file <? srcref('datadict.php')?>)
I save the current query to
session data:
<pre>
$HTTP_SESSION_VARS['editingQuery'] = $this;
</pre>

<p>Then, if the user clicks Submit,
<? srcref('update.php')?> is called, and at this
moment 
$HTTP_SESSION_VARS['editingQuery'] is not defined.
Mysterious...

<p>", "2002-06-12", 1, 0,0,9, "There is now another runtime error when you try to update rows. One
click later than before.
", "Updating rows", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES (NULL, "2002-06-12", 1, 0,0,9, "Lino 0.0.9 is out at http://www.girf.ee/~luc/lino-0.0.9/index.php
", "0.0.9 released", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES ("Notice: Undefined property: row
in /home/luc/public_html/lino-0.0.9/datadict.php on line 1887.

<p>", "2002-06-12", 1, 0,0,10, "A little bug, came only if $debug was 1.
", "Undefined property: row", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES (NULL, "2002-06-12", 1, 0,0,10, "There is now a new Table PRJ2PRJ (a Project can have parents and
children).
And there is a Link from NEWS to PROJECTS : each NEWS itemcan be
assigned to a single project.
", "Projects and News linked", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES (NULL, "2002-06-12", 1, 0,0,10, "To encode the projects.pin file i wanted a new header field type
\"Array\". So now I can create PROJECTS using Pinboard format. They need
a field \"parentProjects\" which is a list of 0 to N Project id's...
", "pin2sql.py : ArrayType", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES ("Answer: Because I omitted to send the appropriate HTTP header. PHP by
default answers in HTML. If I answer in XML, I must explicitly say it
using <tt>header(\"Content-type: text/xml\");</tt>.

<p>Now the client browser knows that Lino answers in XML.  Result: since
the browser now also checks whether this is <i>valid</i> XML,
and since Lino's XML is not yet perfect,
you don't see anything but an error message indicating what is invalid.

<p>", "2002-06-12", 1, 0,0,10, "Why does my browser display other people's xml pages as xml, while
Lino's XML output is displayed in a very strange manner?
", "HTTP content-type", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES ("There is now a global variable $renderer. There are currently two
Renderer classes : HtmlRenderer and XmlRenderer.
Renderer.OnRow renamed to Renderer.ShowQueryRow.
Renderer.OnHeader renamed to Renderer.ShowQueryHeader.
Renderer.OnFooter renamed to Renderer.ShowQueryFooter.

<p>", "2002-06-13", 1, 0,0,10, "Some internal changes to get the XML output working.
It seems to work
now for queries where the contents has no special characters
(umlauts).
", "Renderer", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES ("I read 
[url http://www.devshed.com/Server_Side/PHP/SelfDoc/print] and
looked at
[url http://www.phpdoc.de/doc/introduction.html 2].
A tool like PHPDoc would be nice, but the current Version 1.0beta has
a conceptual problem: it does not really parse the code. It
would have problems to create the Lino API since almost all
classes are in one file.
This Version 1.0beta is more than one yar old:
the project seems dead...

<p>", "2002-06-17", 1, 0,0,11, "PHPDoc is a tool like JavaDoc which could be useful to create the Lino
API documentation.
", "Use PHPDoc?", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES ("<table>
<tr>
<td>Code
<td>Result
<tr>
<td><tt>ref('PERS:1')</tt>
<td><?= ref('PERS:1')?>
<tr>
<td><tt>ref('PERS:1','Luc')</tt>
<td><?= ref('PERS:1','Luc')?>
</table>

<p>", "2002-06-18", 1, 0,0,11, "Shows a reference to a single record in a table.
", "new global function ref()", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES ("<table>

<p><tr>
<td>Quick tag
<td>equivalent PHP code
<td>Result

<p><tr>
<td><tt>&#91;url http://www.url.com]</tt>
<td><tt>&lt;? urlref('http://www.url.com')?></tt>
<td>[url http://www.url.com]

<p><tr>
<td><tt>&#91;url http://www.url.com url]</tt>
<td><tt>&lt;? urlref('http://www.url.com','url')?></tt>
<td>[url http://www.url.com url]

<p><tr>
<td><tt>&#91;ref PERS:1]</tt>
<td><tt>&lt;? ref('PERS:1')?></tt>
<td>[ref PERS:1]

<p><tr>
<td><tt>&#91;ref PERS:1 Luc]</tt>
<td><tt>&lt;? ref('PERS:1','Luc')?></tt>
<td>[ref PERS:1 Luc]
</table>

<p>This system is implemented using preg_replace(),
actually 2 x 3 lines of code.
Look at the source of [ref METHODS:MemoType,ShowValue].

<p>API change as side effect: all Show*Ref() methods
renamed to Get*Ref().
They don't echo the string themselves but just return it.

<p>", "2002-06-18", 1, 0,0,11, "In memo fields you can now use quick tags instead of the quite
complicated PHP code.
", "Quick Command Tags", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES (NULL, "2002-06-18", 1, 0,0,11, "[ref METHODS:JoinFieldColumn,Render] always displayed an url with an
empty label. Fixed.
", "JoinFieldColumn.Render() did not work.", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES (NULL, "2002-06-18", 1, 0,0,11, "GetRowLabel($query,$alias)
replaced by
GetRowLabel($row)
", "API for GetRowLabel() changed", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES ("API change : [ref METHODS:Table,GetPrimaryKey]
must now return an array of references to
the fields who serve as primary key.

<p>", "2002-06-18", 1, 0,0,11, "It is now possible to define tables whose primary key is more than one
column.
", "Compound primary keys", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES (NULL, "2002-06-18", 1, 0,0,11, "Some important internal changes in the data dictionary.
The Join class now represents more closely a link.
", "Internal structure of data dictionary modified", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES (NULL, "2002-06-18", 1, 0,0,11, "I started the new module [ref CLASSES:APIDOC]
in the hope that it helps me to write
API documentation. 
", "New module APIDOC", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES (NULL, "2002-06-20", 1, 0,0,11, "If you change the showDetail option using OptionPanel on a IsSingleRow
query, then this property gets lost because Query.GetRef() does not
know about it...
", "todo: \"&id=\"", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES ("After reading 
[url http://www.faqts.com/knowledge_base/view.phtml/aid/562/fid/9] and
[url http://www.phpbuilder.com/tips/item.php?id=66],
i won't rename them to *.inc but to *.inc.php.

<p>", "2002-06-21", 1, 0,0,11, "How should include files be named? foo.php? foo.inc? foo.inc.php?
", "include files", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES ("[ref DBITEMS:tour] is now implemented using DocBook and pin2sql.
The pinboard source used to feed the database
is [srcref pinboard/doc.pin]

<p>", "2002-06-22", 1, 0,0,11, "A module to write structured documents such as books or articles. This
module will probably also replace the [ref CLASSES:APIDOC ApiDoc]
module.
", "new DocBook module", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES ("ShowTitle($title) and ShowFooter() are now replaced by BeginSection()
and EndSection().

<p>There is now the concept of a margin and a new global function
ToMargin().

<p>", "2002-06-22", 1, 0,0,11, "Some important works in presentation logic.
", "The margin", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES ("<ul>
<li>
We decided that Lino should be split into a
[ref DBITEMS:architecture_backend Backend]
and a [ref DBITEMS:architecture_middle Middle Tier]
(meeting on Thursday 2002-06-20 at Girf).
We must continue to
think together about this change in architecture.
I need more concrete decisions before I can implement something.

<p><li>If web users update the database, Lino can write this update to a
log file and notify some responsible person (me, for example). It
would be a step towards using Lino as a community tool if people can
easily add their remarks to DocBook entries.

<p><li>
I have still quite some ideas for the HTML presentation layer
which I would like to become visible.
I hope that the Lino HTML interface
can soon be considered \"usable\".
The first application would be the DocBook module.

<p><li>When calling show source, user gets Fatal error: Call to a member
function on a non-object in html.inc.php on line 137.
The $renderer must become independent from Lino. BeginSection() and
EndSection(), ToMargin() must become methods of the renderer.

<p></ul>

<p>", "2002-06-22", 1, 0,0,11, "Here an overview of where Lino is and what to do next.
", "Release 0.0.11 is ready", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES ("The data dictionary must not speak about the format of a query, but
well about its depth.

<p><ul>

<p><li>The most superficial query which i can imagine
(depth 1) is the <b>reference</b> to a potential query.
It needs a user's click before Lino even executes such a query.

<p><li><b>short list</b> (depth 2) means that yes, i am interested in
the result of this query, but please don't waste space. Maximum one
paragraph for the whole result.

<p><li><b>list</b> (depth 3) means that I expect a series of
paragraphs, one for each row. (List can become later a simple
paragraph list, a numbered list, a bullet list,...)

<p><li><b>table</b> (depth 4) shows all rows in the well-known table.

<p><li><b>page</b> (depth 5) shows one row at a time. \"I want to see
this row, only this one.\"

<p></ul>

<p>Let's add one item to the beginning of this list: depth 0 means
that Lino should not show this query at all. This depth is not
meaningful for a main-level query, but our travel into the depths of a
query is not finished.

<p><b>The depth of details.</b>

<p><ul>
<li>A query with depth 1 or 2 will not show any details.
maxDetailDepth() is 0.

<p><li>A List query (depth 3) usually also won't show any details.  But
it could. It is able to show references to details, and it could even
show details as short lists. But certainly not more.
maxDetailDepth() is 2.
defaultDetailDepth is 0.

<p><li>A table query (depth 4) is able to show details as a list. Even
(rarely) as a table (which is a table inside a table).
maxDetailDepth() is 4.  defaultDetailDepth is 3.

<p><li>A page query (depth 5) can show details in any formats. (oops:
here it is again, the word \"format\"). maxDetailDepth() is 5.
defaultDetailDepth is 4.

<p></ul>

<p>Note that the depth level is represented by an integer. It is no
longer a format keyword but a \"level\".

<p>Lino uses this to determine the default depth of detail queries.
because (by default) a page query will display 

<p>Notes concerning the HTML interface:
<ul>
<li>only table and page queries can directly modify
the data (using isEditing).

<p><li>there can now be a button to increase or decrease
the depth.
</ul>

<p>", "2002-06-25", 1, 0,0,12, "I introduced a new concept: the <b>depth</b> property of a query.
This is a more abstract replacement for the current \"format\" property.
", "The depth of a query", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES (NULL, "2002-06-28", 1, 0,0,13, "<ul>
<li>URL to Query now handled in [ref FILES:render.php].
<li>Module::SetupLinks() and SetupTables()
<li>peek with complex primary key
<li>Projects table moved from COMMUNITY to APIDOC module.
<li>Structure changes in APIDOC module
<li>many more...
</ul>
", "Many little changes", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES ("isMainComponent and renderNestingLevel are now replaced by the
Query->parent attribute.  isMainComponent() now simply returns
is_null($this->parent), and NestingLevel() loops backwards through the
chain of parents. Either a simple count, or perhaps the sum of all.
Perhaps with weight factors?

<p>When a Detail creates its Query, it can decide about the depth.

<p>", "2002-06-29", 1, 0,0,14, "DBITEMS::MoveUp()
$HTTP_SESSION_VARS['editingQuery']
replaced by 
$HTTP_SESSION_VARS['renderedQuery']
function show() is used only in index.php
and does not work with renderedQuery
", "Actions (start)", NULL);
INSERT INTO CHANGES (body, date, author, release,major,minor, abstract, title, id) VALUES (NULL, "2002-07-02", 1, 0,0,14, "New table TOPICS in DOCBOOK module.
Module APIDOC renamed to SDK (Software Development Kit).
New table RELEASES in SDK module.
", "Some new tables and names", NULL);
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES (NULL, NULL, "index", "LinoConcepts", "Lino Concepts");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES ("The first Lino uses in the near future will be:

<p><ul>
<li>a Community Platform for Software Development
(in particular, for developing the Lino software)

<p><li>a CRM application
</ul>

<p>Technically, an application is defined by
<ul>
<li>a database 
<li>a domain (directory on the server) where the
application specific php files reside.
</ul>

<p>", "The behaviour of a Lino Application is defined by the set of modules
which have been chosen to be part of this particular
applications.
[url http://www.girf.ee/luc/lino] is currently the only
known Lino Application.
", "LinoConcepts", "tour_Applications", "Applications");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES ("Let's look at two table definitions :

<p><pre>
class PERSONS extends Table {

<p>  function init() {

<p>    $this->AddIntField(\"id\",\"ID\");
    $this->AddTextField(\"name\",\"Name\");
    $this->AddTextField(\"fname\",\"First Name\");
    $this->AddTextField(\"title\",\"Title\");
    
    $this->label = \"Persons\";
  }

<p>}

<p>class ADDRESSES extends Table {

<p>  function init() {
    $this->AddIntField('id','ID');

<p>    $this->AddTextField('email','E-Mail');

<p>    $this->AddTextField('zip','Zip Code');
    $this->AddTextField('city','City');
    
    $this->AddTextField('street','Street');
    $this->AddIntField('house','#');
    $this->AddTextField('box','box');

<p>    $this->label = 'Addresses';

<p>  }
  
}
</pre>

<p>", "A Table in Lino describes a data table in the SQL database.  A Lino
Table contains not only Fields (SQL columns), but also Vurts (Virtual
fields) and Actions.  (Vurts and Actions are for later. Currently there
is no concrete example to show their use.)
", "LinoConcepts", "tour_Tables", "Tables");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES ("Examples of Lino Standard Modules :

<p><ul>

<p><li>System (Users, Views, Languages)

<p><li>Addressbook (Persons, Organisations, Addresses)
<li>Agenda (Talks, Meetings)
<li>Community (News,Projects,To-Do-List)

<p><li>Topics, Products, Ordering, Invoicing, Accounting...
</ul>

<p>Each module is theoretically implemented in its own .php file.  But
the list of Standard Modules and tables is still unstable.
That's why currently the file
<a href=\"source.php?file=crm.php\">crm.php</a>
provides three modules ADDRESS, COMMUNITY and
AGENDA.

<p>Another file
<a href=\"source.php?file=sys.php\">sys.php</a>
provides the System module.

<p>", "A Lino Module is currently
nothing more than a collection of
<b>table
definitions</b> and the <b>links</b> between them.
", "LinoConcepts", "tour_Modules", "Modules");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES ("<pre>
class ADDRBOOK extends Module {
  
  function init() {
    AddTable('PERSONS');
    AddTable('ADDRESSES');
  }

<p>  function link() {

<p>    AddLink('ADDRESSES','pers','Person',
            'PERSONS','addresses','Addresses');
    
  }
</pre>

<p>(Implementation note: Lino currently initializes in two steps: init()
and link(). This is because all tables must be initialized before it
is possible to create links between them.)

<p>Here the ADDRBOOK Module defines two Tables PERSONS and
ADDRESSES. These tables are linked together : FROM Addresses TO
Persons.  This Link will automatically create another special field
'pers' in the ADDRESSES table which is a pointer to a PERSON. This
Link is a 0-N relation : 1 Person can have 0, 1 or many addresses.

<p>The User will see this Link as follows:

<p><ul>
<li>If you create an Address, you must specify a Person who lives at
this address.
<li>If you look at a Person, you can see a list of Adresses
which are connected to this Person.
</ul>

<p>", "Lino simplifies the programming of links between tables.
Here again some code:
", "LinoConcepts", "tour_Links", "Links");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES ("This is somewhat unconventional.
Lino separates the definition of \"real\" data fields from fields who
are just pointers. This makes it easy to juggle around with different
variants of database structures during a prototype phase.

<p>", "Note that the \"pers\" field must not be specified in the table
definition. It comes automatically because you linked the two tables.
", "LinoConcepts", "tour_Separating", "Separating data definition from link definition");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES ("Of course, the specified id must be unique. And the name of a person
may not be empty. These are constraints which even MySQL can
handle.

<p>Another case for validation is : id is unique, but there is already
another person with same (name,first_name). Okay, if the birth dates
are different, we can assume that they are different persons. But if
the new person has no birthdate specified? There is no general rule
for such cases. The appropriate reaction depends on the application. 

<p>Lino can refuse any database update because of such reasons which are
application-specific rules.

<p>Instead of refusing, Lino can also say \"Do you want that I ask for
manual confirmation by some operator\". Lino would then send an e-mail
to a responsible human database supervisor: User X asked to create a
Person (id, first_name, name, birthdate), but there is possible
duplicate creation. Please give your confirmation.

<p>", "Imagine a database with a table of Persons. Somebody asks Lino to add
a new Person (id, first_name, name,
birthdate).
", "LinoConcepts", "tour_validation", "Data validation");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES ("Examples of data which don't come from SQL database:

<p><ul>
<li>Calendar : a virtual table. The rows of the calendar represent
each day of the year. They are not stored anywhere since they are
well-known and easy to compute.
But DateFields could automaticaly link to the Calendar,
and a Calendar
query has a lot of Details.

<p><li>The currency exchange rates could be stored in an array which is
initialized via Internet from a currency exchange rates server.

<p><li>A FileSystem table could represent the tree structured directories
and files of a file system.

<p></ul>

<p>Note that this connectivity can also be implemented using
\"Database Agents\", that is little daemons which update the Lino
database independently of the Lino server....

<p>", "Currently Lino has one database for one application, and Lino can
manage only SQL data. This could change in the future.
", "LinoConcepts", "Heterogenous", "Heterogenous data sources");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES (NULL, NULL, "index", "tour", "Le Tour de Lino");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES (NULL, NULL, "tour", "tour_intro", "Introduction");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES ("<ul>
<li>Programming Framework : Lino is not meant for end-users, but as
a library or engine to be used by Lino Providers.

<p><li>Web Application : a Web-based interface to an SQL database.
</ul>

<p>", "Lino is a
<b>Programming Framework</b>
to create high-quality, low-cost <b>Web Applications</b>.
", "tour_intro", "tour_whatis", "What is Lino?");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES ("In its current implementation (PHP, MySQL), Lino has probably some
technical limits, so it is not a choice for large-scale
applications. [TODO: Is this true? What limits?]

<p>", "Lino aims the low-cost Web Application market. Potential End-users are
medium-sized or small companies who understand that they need
assistance from IT experts for the analysis and setup of their
Information System and who are willing to dedicate an appropriate
budget to these services.
", "tour_intro", "tour_for_whom", "For whom is Lino?");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES ("<ol>

<p><li>Selling:
<ul>

<p><li>Know the <b>Standard Modules</b> and what they do. Know also what
they can <b>not</b> do.

<p><li>Analysis :
Speak with the User to find out which modules are necessary.

<p></ul>

<p><li>System Administration
<ul>
<li>Install Apache, MySQL, PHP, Lino
<li>Manage SQL databases
<li>Install backup possibilities. Explain to the User how to use them.
</ul>

<p><li>Maintenance
<ul>
<li>Training : Explain to the User how to use their Lino.

<p><li>Support : Answer to the User's questions.

<p><li>Check continuously with the User if the analysis is correct or
whether there are new needs.
</ul>

<p><li>Take part in the development process:
<ul>
<li>Understand the Lino source code and how Lino works internally.
<li>Specify requirements for new Lino Modules.
<li>Test Lino modules and report bugs to a Developer.
</ul>
</ol>

<p>A Lino Developer is somebody who writes new Lino Modules.  Currently
there is only one such person, but I don't want to stay alone.

<p>Since Lino is Free Software, the Lino Service Providers are not
legally bound to the developer. They can decide to rely on their own
Lino Developer.

<p>", "A Lino Service Provider is a company who knows enough about Lino to be
able to give quality service to end-users. A Lino Service Provider
should have the following abilities:
", "tour_intro", "tour_providers", "Service Providers");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES ("I am currently working on Lino without getting money for this
work. This shows only that I personally believe that there is need for
Lino. I may be wrong.

<p>I currently get moral and technical support from
the people at [url http://www.girf.ee Girf].
Without them, you would not be able to see Lino:
they are not only hosting the currently only Lino instance of the WWW,
but they gave me the idea to implement Lino in PHP and MySQL.

<p>", "Lino is born from my 10 years of experience in Software Development
at [url http://www.pacsystems.be PAC Systems].  I had to stop
working for PAC Systems because I moved from Belgium to Estonia and
because Lino was not finished, not even visible, at this time.
There is hope that Lino could become a successor for good old TIM.
", "tour_intro", "tour_who", "Who is developing Lino?");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES ("Note that the current
implementation is only a draft of the big plans for the future.

<p>", "Here is an overview of the Lino components and how they interact.
", "index", "architecture", "Lino Architecture");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES (NULL, "Lino works with any SQL-compatible database server, even MySQL.
There will be optimized <b>database drivers</b> for
PostgreSQL, Oracle...
", "architecture", "components.dbserver", "Database Server");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES (NULL, "The Lino Backend 
sits around the database and controls
the accesses to this database.
", "architecture", "architecture_backend", "The Backend");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES ("See [ref DBITEMS:tour_validation] for an example of rules in the
datadict. 

<p>The data dictionary also contains abstract presentation logic.

<p>", "The Data Dictionary contains meta-data
about an application:
Which tables are available,
how they are linked together,
user actions,
business rules,...
", "architecture_backend", "components.datadict", "Data Dictionary");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES ("The backend is the only component who communicates directly with the
database. This is to protect the database from accesses which don't
obbey the application's rules and thus would corrupt the data
integrity.

<p>The [ref DBITEMS:pinboard_interface pin2sql tool] which I currently
use is an example of short-cutting this architecture.  pin2sql
should better create Lino XML statements.  These statements are sent
to the Lino Backend who translates them to SQL and sends them to the
database server.

<p>", "The Backend communicates 
with the
database, using a <b>Database Driver</b> who creates the SQL
statements to be sent to the database server.
", "architecture_backend", "components.dbdriver", "Database driver");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES ("TODO: 
Is the Backend a HTTP server?
Or a simple TCP server?
What about user authentification?
Which programming language (Python, Java, PHP, ...)?

<p>[TODO: XML specification]

<p>Why do you want to split the XML server from the HTML renderer?
Because here is a reason why you should not split them: The Backend
and the HTML renderer access the same data. And they usually run
on the same server.
Why do you want to split them into two processes?

<p>Unsplit: Lino backend gets data from Database. As an array of
rows. Then he passes this array to the renderer who will output it
with the appropriate HTML tags around it.

<p>Split: Backend gets data from database as array. Renders it as
XML (putting the appropriate tags around the data and sending this to
stdout).
Then another Lino component reads this XML stream, parses it,
re-creates the original array, then continues the second part of the
job (HTML renderer).

<p>Load balancing. If there are many processes.

<p>", "The Backend communicates with the outside world using XML.
", "architecture_backend", "components.comm", "Communication");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES (NULL, "The Middle Tier is a suite of software components, also third-party
products, which translate Lino's XML interface into more useful
outside-world languages (HTML, PDF, ...).
", "architecture", "architecture_middle", "The Middle Tier");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES (NULL, "The <b>HTML interface</b>
is a little HTTP server who accepts HTTP
requests and forwards them to Lino. 
The answer from Lino which is in XML can
be translated to HTML using XSLT.
", "architecture_middle", "html_interface", "The HTML interface");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES ("Currently this tool shortcuts the Lino Backend and writes directly to
the database. 

<p>", "I decided to develop my own format to edit structured texts.  I called
it Pinboard. And I wrote a little tool which imports pinboard
documents into Lino.
", "architecture_middle", "pinboard_interface", "The Pinboard interface");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES (NULL, NULL, "index", "limits", "Limits");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES ("Lino does not yet reflect your structure changes automatically into an
existing database.  You must do this yourself.

<p>Databases are currently being created manually using SQL scripts.

<p>", "Juggling around with the data structure is very easy and useful,
but for the moment only if you don't forget to modify the underlying
SQL database structure accordingly.
", "limits", "database", "Database");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES (NULL, NULL, "index", "fence", "Peeking over the fence");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES ("<quote>
Copyright 2002 101communications LLC. XML Report may only be
redistributed in its unedited form. Written permission from the editor
must be obtained to reprint the information contained within this
newsletter. Contact [url mailto:khefner@101com.com]
</quote>

<p>", "XML Report is a newsletter by 101communications.
Subscribe at
[url http://subscribe.101com.com/ADT/default.htm]
", "fence", "XMLReport", "XML Report");
INSERT INTO NEWS (body, project, author, date, abstract, title, id) VALUES (NULL, NULL, 1, "2002-06-26", "Lino should perhaps support business-to-business communication using
the OAGIS XML specification for Business Object Documents
(e.g. Purchase Orders, Invoices, Shipments,...).  [url
http://www.openapplications.org]
", "OAGIS interface", NULL);
INSERT INTO NEWS (body, project, author, date, abstract, title, id) VALUES ("Lino also uses a technique which I could call pipelining:

<p>ToBody(), ToMargin() and
ToSuperHeader() are pipeline streamers. A method does not write simply
to \"stdout\" but to one of these pipelines.
Body, Margin and SuperHeader are pipeline areas.

<p>", NULL, 1, "2002-06-26", "AxKit ([url http://www.axkit.org]),
a Perl-based XML application server framework
for Apache [url http://www.xml.apache.org],
uses a technique which they call \"Pipelining\".
", "AxKit and Apache", NULL);
INSERT INTO NEWS (body, project, author, date, abstract, title, id) VALUES ("<quote>
Tamino XML Server is the first XML platform to store XML information
without converting it to other formats, such as relational tables. It
integrates relational or object-oriented data into XML structures.
</quote>

<p>Luc: But XML is not a data storage format?

<p><quote>
The XML engine in Tamino XML Server (...)  has been designed for
URL-based access.  It cooperates with existing standard HTTP servers.
(...)  Tamino XML Server's query language X-Query is based on the
XPath standard. This allows for powerful queries on stored documents
as part of a URL issued either via standard Web browsers or through an
application.</quote>

<p>Luc: Interesting.
So they don't use XML as language for the requests.
I would like to see their query language.
Aha, here is an example:

<p><quote>
The following example of X-Query syntax illustrates a request for a
doctor's details by patient name (for example, a patient is in trouble
and the nurse wants to contact the doctor):

<p><tt>...?_xql=hospital/patient[p-surname=\"Jones\"]/doctor</tt>

<p>where \"...\" stands for the address of the Tamino XML Server. This
query retrieves the record of the doctor associated with the patient
called \"Jones\". The user does not know that the patient's record is
stored in XML format and the doctor's details are retrieved from an
SQL table. In practice, the X-Query syntax is also hidden from the
user by an application GUI.

<p></quote>

<p><quote> The XML engine's basic function is to store XML objects in and
retrieve them from their respective data sources. It does this based
on schemas defined by the administrator in the Data Map. XML objects
are stored natively in Tamino.  (...)  XML objects to be stored by the
XML engine are described by their schema stored in Tamino's Data
Map. Tamino XML Server's built-in XML parser checks the syntactical
correctness of the schema and ensures that incoming XML objects are
well-formed.</quote>

<p>Luc: Lino uses the pure programming language (currently PHP) to define
the data map. If a system administrator wants to adapt the data
dictionary to her needs, she must do this in PHP. Why should XML be
better? One advantage: if a new Lino version decides to switch to
Java, they must all convert their data dictionaries... But...)

<p>More on [url http://tamino.demozone.softwareag.com/mainSiteX/].

<p>", NULL, 1, "2002-06-26", "Commented excerpts from [url http://www.softwareag.com/tamino].
", "Tamino XML server", NULL);
INSERT INTO NEWS (body, project, author, date, abstract, title, id) VALUES ("See also the project list
for [url render.php?t=PROJECTS&depth=5&_super=8 Lino 1.0.x].

<p>", NULL, 1, "2002-06-27", "We met again to speak about Lino.
", "Meeting Hannes, Andres & Luc", NULL);
INSERT INTO NEWS (body, project, author, date, abstract, title, id) VALUES ("Known bugs:
<ul>
<li>the [more] link does not always work
<li>displaying the Persons list with depth 5 causes a User Error
\"sponsor : no such join alias in CHANGES\".
<li>The [url
http://localhost/phptest/lino/render.php?t=DBITEMS&v=DBITEMS&page=1&pglen=10&depth=3&filter=ISNULL(DBITEMS.super)
DocBook items] link does not show the general page header.
</ul>    

<p>", 7, 1, "2002-06-28", "Many little changes. Some known bugs.
", "Summer Release 0.0.13 ready", NULL);
INSERT INTO NEWS (body, project, author, date, abstract, title, id) VALUES ("And, especially after reading
[url http://www.xach.com/aolserver/mysql-to-postgresql.html],
I thought about switching from [ref TOPICS:MySQL] to PostgreSQL.

<p>BTW: PostgreSQL installation is in fact very simple: you just need to
install [ref TOPICS:Cygwin]. 

<p>", 7, 1, "2002-07-02", "I finally managed to get [ref TOPICS:PostgreSQL] running on my
machine.
", "OAGIS interface", NULL);
INSERT INTO PROJECTS (body, sponsor, title, date, stopDate, abstract, responsible, super, id) VALUES (NULL, 1, "Lino", "2002-05-22", NULL, NULL, NULL, NULL, 1);
INSERT INTO PROJECTS (body, sponsor, title, date, stopDate, abstract, responsible, super, id) VALUES (NULL, 2, "Lino 0.0.x", "2002-05-22", NULL, NULL, 1, 1, 2);
INSERT INTO PROJECTS (body, sponsor, title, date, stopDate, abstract, responsible, super, id) VALUES (NULL, 1, "Lino 1.0.x", NULL, NULL, NULL, 1, 1, 8);
INSERT INTO PROJECTS (body, sponsor, title, date, stopDate, abstract, responsible, super, id) VALUES ("Tasks
<ul>

<p><li>Get an LDAP server running on my machine.
Currently working on [url http://www.openldap.prg].

<p><li>Read more about LDAP.
[url http://www.faqs.org/rfcs/rfc2849.html RFC2849],
[url http://developer.netscape.com/docs/manuals/directory/deploy30
Netscape Directory Server Deployment Guide],
[url http://python-ldap.sourceforge.net/pydoc/ldif.html Python ldif
module], 
...

<p><li>A more simple variant of the
[ref CLASSES:ADDRBOOK AddrBook module]
which is more easy to integrate
into an LDAP connection.

<p><li>New concept of DataSupplier:
can be either SqlDataSupplier or LdapDataSupplier

<p></ul>

<p>", 2, "Addressbook connection to & from  LDAP server.", NULL, NULL, "Lino would show the content stored by an LDAP server. For the user it
is not important where the data really comes from.
", 1, 21, 9);
INSERT INTO PROJECTS (body, sponsor, title, date, stopDate, abstract, responsible, super, id) VALUES ("Tasks
<ul>
<li>a logging system for the changes
<li>an XML syntax
<li>a first XML data import slot.
</ul>

<p>", 1, "Data replication", NULL, NULL, "Data replication would mean that Lino logs each change in a local
database and provides possibilities to replicate such changelogs to
another database.
", 1, 8, 10);
INSERT INTO PROJECTS (body, sponsor, title, date, stopDate, abstract, responsible, super, id) VALUES ("Tasks
<ul>
<li>General presentation philopsophy
<li>View Editor does not work
<li>Quick Filter does not work
<li>Searching 
<li>Delete and Append buttons
<li>\"picker\" : Button to select a value of a JoinField
<li>Data validation
</ul>

<p>", 1, "HTML interface", NULL, NULL, "There are some important details to do before the HTML interface can
be considered usable.
", 1, 8, 11);
INSERT INTO PROJECTS (body, sponsor, title, date, stopDate, abstract, responsible, super, id) VALUES ("<ul>
<li>CALENDAR as a virtual table (new class CalendarDataSupplier)
<li>DateType fields automatically link to Calendar
<li>php scripts day.php, week.php, month.php
</ul>

<p>", 1, "Calendar", NULL, NULL, "A Calendar would be a user interface to manage a calendar.
With views by day, week, month.
", 1, 11, 12);
INSERT INTO PROJECTS (body, sponsor, title, date, stopDate, abstract, responsible, super, id) VALUES ("<ul>
<li>InfoCenter : Topics
<li>Business : Products, Manufacturers,
Suppliers, Customers, Orders, Shipments, Invoices
<li>Financial : Accounts, Statements
<li>Items, Reservations
</ul>

<p>", 1, "More modules", "2002-06-28", NULL, "I have a few more modules in mind which I should create so that a new
visitor can see more concretely what Lino can do.
", 1, 8, 13);
INSERT INTO PROJECTS (body, sponsor, title, date, stopDate, abstract, responsible, super, id) VALUES ("Probably create a new class Section which holds the title and number
of a section...

<p>", 1, "Pipelining", NULL, NULL, "Pipelines are a step towards renderer abstraction.
BeginSection() should become visible only if there is
at least some output. If EndSection() is called before any output,
then the title should not be visible at all.
", 1, 11, 14);
INSERT INTO PROJECTS (body, sponsor, title, date, stopDate, abstract, responsible, super, id) VALUES (NULL, 1, "Internationalization (i18n)", NULL, NULL, "I18N means that the User Interface is in the user's language.
", 1, 8, 15);
INSERT INTO PROJECTS (body, sponsor, title, date, stopDate, abstract, responsible, super, id) VALUES ("A BabelText and BabelMemo fields would be special fields who represent
a set of table columns which mean the same thing in different
languages.

<p>Example : if the Products table has a BabelText field \"name\", and if
the database is declared to work for languages de and fr, then the
table in the database has two independant columns name_de and
name_fr. But Lino knows that they are in fact the \"name\" column....

<p>", 1, "Multilingual applications (BabelText)", NULL, NULL, "Besides Internationalization I have some ideas to support multiple
languages applications.
", 1, 8, 16);
INSERT INTO PROJECTS (body, sponsor, title, date, stopDate, abstract, responsible, super, id) VALUES (NULL, 1, "Login and User management", NULL, NULL, "Of course there must also come a Login window. A Users table, possibly
retrieved from LDAP server, and an access attribution system.
", 1, 8, 17);
INSERT INTO PROJECTS (body, sponsor, title, date, stopDate, abstract, responsible, super, id) VALUES ("But that's not enough.
(todo: Sure? Bugs are just little
projects. They are sub-projects of releases...)

<p>", 1, "Tables for Bugs and Releases", NULL, NULL, "The APIDOC module should have separate Tables BUGS and
RELEASES. Currently they are handled as PROJECTS.
", 1, 8, 18);
INSERT INTO PROJECTS (body, sponsor, title, date, stopDate, abstract, responsible, super, id) VALUES ("<ul>
<li>query : \"please give me some data from your database\".
Parameters: table, view, slices, pagelength, page, filter,
renderer, ...
Answer: the result set.
<li>update : \"please do the following updates in your database\".
An update request must then post some data in some XML syntax
(to be specified.) 
<li>action : e.g. shutdown, database integrity check
</ul>

<p>", 2, "XML Server", NULL, NULL, "Lino should be able to respond to requests.
", 1, 8, 19);
INSERT INTO PROJECTS (body, sponsor, title, date, stopDate, abstract, responsible, super, id) VALUES (NULL, 2, "Connection to & from MS-Exchange server", NULL, NULL, "MS-Exchange has also an XML interface. You can then ask (e.g.)
I want to create a meeting with the following participants. Then you
can find a time and date where most participants are available, then
create the meeting. Interesting connectivity slot to be explored.
", 1, 21, 20);
INSERT INTO PROJECTS (body, sponsor, title, date, stopDate, abstract, responsible, super, id) VALUES (NULL, NULL, "Connectivity", NULL, NULL, "Connectivity means to not simply import and
export many foreign file formats,
but establish a real-time connection to avoid replication.
", 1, 8, 21);
INSERT INTO PROJECTS (body, sponsor, title, date, stopDate, abstract, responsible, super, id) VALUES ("For example:
<ul>
<li>DBITEMS: MoveUp, MoveDown, MoveLeft, MoveRight to modify the
item's super and seq fields.
</ul>
", 1, "Implement Actions", NULL, NULL, "There is currently no Action example being used.
I should implement some actions.
", 1, 11, 22);
INSERT INTO RELEASES (release,major,minor, date, title) VALUES (0,0,9, "2002-06-12", "Lino 0.0.9");
INSERT INTO RELEASES (release,major,minor, date, title) VALUES (0,0,10, "2002-06-13", "Lino 0.0.10");
INSERT INTO RELEASES (release,major,minor, date, title) VALUES (0,0,11, "2002-06-22", "Lino 0.0.11");
INSERT INTO RELEASES (release,major,minor, date, title) VALUES (0,0,12, "2002-06-25", "Lino 0.0.12");
INSERT INTO RELEASES (release,major,minor, date, title) VALUES (0,0,13, "2002-06-28", "Lino 0.0.13 (last release before Summer 2002)");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES ("User code
<ul>
<li>should be quite easy to understand
<li>uses only the documented functions of the Lino API,
<li>should not need modification between different Lino versions.
</ul>

<p>", "If you want to look at the Lino source files, you can split them into
two categories: (1) \"user code\" and (2) the \"Lino kernel\".
", "tour_source", "tour_userVersusKernel", "\"User\" versus \"Kernel\" code");
INSERT INTO DBITEMS (body, abstract, super, id, title) VALUES ("These files are Lino kernel
and must reside on the server somewhere in the PHP include path. 

<p><li>The collection of standard modules
<ul>
<li>[srcref sys.inc.php]
<li>[srcref crm.inc.php]
<li>[srcref apidoc.inc.php]
<li>[srcref docbook.inc.php]
</ul>

<p>These files are user code, but since the come with Lino they also
reside on the server somewhere in the PHP include path.

<p><li>Query actions
<ul>                 

<p><li>[srcref render.php] :
instanciates a Query and renders it.

<p><li>[srcref update.php] :
process POST data to update the currently editing Query.

<p></ul>

<p>These files are also to be considered kernel code, but
they must reside on the server in the application directory
(which is not nice).

<p><li>Application-specific files
<ul>
<li>[srcref config.inc.php]
tells Lino the database name and how to access it.
<li>[srcref modules.inc.php]
tells Lino which modules are being used for this application.
<li>[srcref index.inc.php]
</ul>

<p></ol>

<p>", "<ol>
<li>Class and function definitions :
<ul>
<li>[srcref lino.inc.php]
<li>[srcref html.inc.php]
<li>[srcref console.inc.php]
<li>[srcref mysql.inc.php]
<li>[srcref datadict.inc.php]
</ul>
", "source", "tour_files", "Lino source files");
INSERT INTO PROJECTS (body, sponsor, title, date, stopDate, abstract, responsible, super, id) VALUES (NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1000);
