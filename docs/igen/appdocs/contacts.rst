========
contacts
========



.. currentmodule:: contacts

Defined in :srcref:`/lino/modlib/contacts/models.py`


This module deserves more documentation.

It defines tables like `Person` and `Company`



.. contents:: Table of Contents



.. index::
   pair: model; CompanyType

.. _lino.contacts.CompanyType:

---------------------
Model **CompanyType**
---------------------




Represents a possible choice for the :class:`Company`.type
field.
Implemented by 
:ref:`dsbe.contacts.CompanyType`
:ref:`igen.contacts.CompanyType`

  
======= ============== ==============================================
name    type           verbose name                                  
======= ============== ==============================================
id      AutoField      ID                                            
name    BabelCharField Designation (Beschreibung,Désignation,Nimetus)
abbr    BabelCharField Abbreviation (Abkürzung,Abbréviation,Lühend)  
name_de CharField      Designation (de)                              
name_fr CharField      Designation (fr)                              
name_nl CharField      Designation (nl)                              
name_et CharField      Designation (et)                              
abbr_de CharField      Abbreviation (de)                             
abbr_fr CharField      Abbreviation (fr)                             
abbr_nl CharField      Abbreviation (nl)                             
abbr_et CharField      Abbreviation (et)                             
======= ============== ==============================================

    
Defined in :srcref:`/lino/modlib/contacts/models.py`

Referenced from
`lino.contacts.Company.type`_



.. index::
   single: field;id
   
.. _lino.contacts.CompanyType.id:

Field **CompanyType.id**
========================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.contacts.CompanyType.name:

Field **CompanyType.name**
==========================





Type: BabelCharField

   
.. index::
   single: field;abbr
   
.. _lino.contacts.CompanyType.abbr:

Field **CompanyType.abbr**
==========================





Type: BabelCharField

   
.. index::
   single: field;name_de
   
.. _lino.contacts.CompanyType.name_de:

Field **CompanyType.name_de**
=============================





Type: CharField

   
.. index::
   single: field;name_fr
   
.. _lino.contacts.CompanyType.name_fr:

Field **CompanyType.name_fr**
=============================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _lino.contacts.CompanyType.name_nl:

Field **CompanyType.name_nl**
=============================





Type: CharField

   
.. index::
   single: field;name_et
   
.. _lino.contacts.CompanyType.name_et:

Field **CompanyType.name_et**
=============================





Type: CharField

   
.. index::
   single: field;abbr_de
   
.. _lino.contacts.CompanyType.abbr_de:

Field **CompanyType.abbr_de**
=============================





Type: CharField

   
.. index::
   single: field;abbr_fr
   
.. _lino.contacts.CompanyType.abbr_fr:

Field **CompanyType.abbr_fr**
=============================





Type: CharField

   
.. index::
   single: field;abbr_nl
   
.. _lino.contacts.CompanyType.abbr_nl:

Field **CompanyType.abbr_nl**
=============================





Type: CharField

   
.. index::
   single: field;abbr_et
   
.. _lino.contacts.CompanyType.abbr_et:

Field **CompanyType.abbr_et**
=============================





Type: CharField

   


.. index::
   pair: model; ContactType

.. _lino.contacts.ContactType:

---------------------
Model **ContactType**
---------------------




Implements the :class:`contacts.ContactType` convention.

  
======= ============== ==============================================
name    type           verbose name                                  
======= ============== ==============================================
id      AutoField      ID                                            
name    BabelCharField Designation (Beschreibung,Désignation,Nimetus)
name_de CharField      Designation (de)                              
name_fr CharField      Designation (fr)                              
name_nl CharField      Designation (nl)                              
name_et CharField      Designation (et)                              
======= ============== ==============================================

    
Defined in :srcref:`/lino/modlib/contacts/models.py`

Referenced from
`lino.contacts.Contact.type`_



.. index::
   single: field;id
   
.. _lino.contacts.ContactType.id:

Field **ContactType.id**
========================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.contacts.ContactType.name:

Field **ContactType.name**
==========================





Type: BabelCharField

   
.. index::
   single: field;name_de
   
.. _lino.contacts.ContactType.name_de:

Field **ContactType.name_de**
=============================





Type: CharField

   
.. index::
   single: field;name_fr
   
.. _lino.contacts.ContactType.name_fr:

Field **ContactType.name_fr**
=============================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _lino.contacts.ContactType.name_nl:

Field **ContactType.name_nl**
=============================





Type: CharField

   
.. index::
   single: field;name_et
   
.. _lino.contacts.ContactType.name_et:

Field **ContactType.name_et**
=============================





Type: CharField

   


.. index::
   pair: model; Contact

.. _lino.contacts.Contact:

-----------------
Model **Contact**
-----------------




Represents a :class:`Person` having a (more or less known) 
role in a :class:`Company`.

  
============ ============ ======================================================
name         type         verbose name                                          
============ ============ ======================================================
id           AutoField    ID                                                    
person       ForeignKey   person (Person,Personne,isik)                         
company      ForeignKey   company (Firma,Société,firma)                         
type         ForeignKey   contact type (Kontaktart,type de contact,Kontaktiliik)
payment_term ForeignKey   payment term (Tasumistingimused)                      
vat_exempt   BooleanField VAT exempt                                            
item_vat     BooleanField item_vat                                              
============ ============ ======================================================

    
Defined in :srcref:`/lino/modlib/contacts/models.py`

Referenced from
`lino.sales.SalesDocument.contact`_, `lino.sales.Order.contact`_, `lino.sales.Invoice.contact`_



.. index::
   single: field;id
   
.. _lino.contacts.Contact.id:

Field **Contact.id**
====================





Type: AutoField

   
.. index::
   single: field;person
   
.. _lino.contacts.Contact.person:

Field **Contact.person**
========================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _lino.contacts.Contact.company:

Field **Contact.company**
=========================





Type: ForeignKey

   
.. index::
   single: field;type
   
.. _lino.contacts.Contact.type:

Field **Contact.type**
======================





Type: ForeignKey

   
.. index::
   single: field;payment_term
   
.. _lino.contacts.Contact.payment_term:

Field **Contact.payment_term**
==============================





Type: ForeignKey

   
.. index::
   single: field;vat_exempt
   
.. _lino.contacts.Contact.vat_exempt:

Field **Contact.vat_exempt**
============================





Type: BooleanField

   
.. index::
   single: field;item_vat
   
.. _lino.contacts.Contact.item_vat:

Field **Contact.item_vat**
==========================





Type: BooleanField

   


.. index::
   pair: model; Person

.. _lino.contacts.Person:

----------------
Model **Person**
----------------



Person(id, country_id, city_id, name, addr1, street_prefix, street, street_no, street_box, addr2, zip_code, region, language, email, url, phone, gsm, fax, remarks, first_name, last_name, title, sex)
  
============= ============= ==========================================================================================================
name          type          verbose name                                                                                              
============= ============= ==========================================================================================================
id            AutoField     ID                                                                                                        
country       ForeignKey    Country (Land)                                                                                            
city          ForeignKey    City (Stadt)                                                                                              
name          CharField     Name (Nom,Nimi)                                                                                           
addr1         CharField     Address line before street (Adresszeile vor Straße,Ligne avant le nom de rue,Addressi lisatext enne tänav)
street_prefix CharField     Street prefix (Präfix Straße,Préfixe rue)                                                                 
street        CharField     Street (Straße,Rue,Tänav)                                                                                 
street_no     CharField     No. (Nr.,N°,Nr.)                                                                                          
street_box    CharField     Box (boîte,PK/krt)                                                                                        
addr2         CharField     Address line after street (Adresszeile nach Straße,Ligne après le nom de rue,Aadressilisa pärast tänav)   
zip_code      CharField     Zip code (Postleitzahl,Code postal,Sihtnumber)                                                            
region        CharField     Region (Région,Maakond)                                                                                   
language      LanguageField Language (Sprache,Langue)                                                                                 
email         EmailField    E-Mail (E-mail)                                                                                           
url           URLField      URL                                                                                                       
phone         CharField     Phone (Telefon,Téléphone,Telefon)                                                                         
gsm           CharField     GSM                                                                                                       
fax           CharField     Fax                                                                                                       
remarks       TextField     Remarks (Bemerkungen,Remarques,Märkused)                                                                  
first_name    CharField     First name (Vorname,Prénom,Eesnimi)                                                                       
last_name     CharField     Last name (Familienname,Nom de famille,Perekonnanimi)                                                     
title         CharField     Title (Anrede,Allocution)                                                                                 
sex           CharField     Sex (Geschlecht,Sexe)                                                                                     
============= ============= ==========================================================================================================

    
Defined in :srcref:`/lino/apps/igen/models.py`

Referenced from
`lino.contacts.Contact.person`_, `lino.ledger.Booking.person`_, `lino.sales.SalesDocument.person`_, `lino.sales.Order.person`_, `lino.sales.Invoice.person`_, `lino.finan.DocItem.person`_



.. index::
   single: field;id
   
.. _lino.contacts.Person.id:

Field **Person.id**
===================





Type: AutoField

   
.. index::
   single: field;country
   
.. _lino.contacts.Person.country:

Field **Person.country**
========================





Type: ForeignKey

   
.. index::
   single: field;city
   
.. _lino.contacts.Person.city:

Field **Person.city**
=====================





Type: ForeignKey

   
.. index::
   single: field;name
   
.. _lino.contacts.Person.name:

Field **Person.name**
=====================





Type: CharField

   
.. index::
   single: field;addr1
   
.. _lino.contacts.Person.addr1:

Field **Person.addr1**
======================



Address line before street

Type: CharField

   
.. index::
   single: field;street_prefix
   
.. _lino.contacts.Person.street_prefix:

Field **Person.street_prefix**
==============================



Text to print before name of street, but to ignore for sorting.

Type: CharField

   
.. index::
   single: field;street
   
.. _lino.contacts.Person.street:

Field **Person.street**
=======================



Name of street. Without house number.

Type: CharField

   
.. index::
   single: field;street_no
   
.. _lino.contacts.Person.street_no:

Field **Person.street_no**
==========================



House number

Type: CharField

   
.. index::
   single: field;street_box
   
.. _lino.contacts.Person.street_box:

Field **Person.street_box**
===========================



Text to print after :attr:`steet_no` on the same line

Type: CharField

   
.. index::
   single: field;addr2
   
.. _lino.contacts.Person.addr2:

Field **Person.addr2**
======================



Address line to print below street line

Type: CharField

   
.. index::
   single: field;zip_code
   
.. _lino.contacts.Person.zip_code:

Field **Person.zip_code**
=========================





Type: CharField

   
.. index::
   single: field;region
   
.. _lino.contacts.Person.region:

Field **Person.region**
=======================





Type: CharField

   
.. index::
   single: field;language
   
.. _lino.contacts.Person.language:

Field **Person.language**
=========================





Type: LanguageField

   
.. index::
   single: field;email
   
.. _lino.contacts.Person.email:

Field **Person.email**
======================





Type: EmailField

   
.. index::
   single: field;url
   
.. _lino.contacts.Person.url:

Field **Person.url**
====================





Type: URLField

   
.. index::
   single: field;phone
   
.. _lino.contacts.Person.phone:

Field **Person.phone**
======================





Type: CharField

   
.. index::
   single: field;gsm
   
.. _lino.contacts.Person.gsm:

Field **Person.gsm**
====================





Type: CharField

   
.. index::
   single: field;fax
   
.. _lino.contacts.Person.fax:

Field **Person.fax**
====================





Type: CharField

   
.. index::
   single: field;remarks
   
.. _lino.contacts.Person.remarks:

Field **Person.remarks**
========================





Type: TextField

   
.. index::
   single: field;first_name
   
.. _lino.contacts.Person.first_name:

Field **Person.first_name**
===========================





Type: CharField

   
.. index::
   single: field;last_name
   
.. _lino.contacts.Person.last_name:

Field **Person.last_name**
==========================





Type: CharField

   
.. index::
   single: field;title
   
.. _lino.contacts.Person.title:

Field **Person.title**
======================





Type: CharField

   
.. index::
   single: field;sex
   
.. _lino.contacts.Person.sex:

Field **Person.sex**
====================





Type: CharField

   


.. index::
   pair: model; Company

.. _lino.contacts.Company:

-----------------
Model **Company**
-----------------



Company(id, country_id, city_id, name, addr1, street_prefix, street, street_no, street_box, addr2, zip_code, region, language, email, url, phone, gsm, fax, remarks, vat_id, type_id)
  
============= ============= ==========================================================================================================
name          type          verbose name                                                                                              
============= ============= ==========================================================================================================
id            AutoField     ID                                                                                                        
country       ForeignKey    Country (Land)                                                                                            
city          ForeignKey    City (Stadt)                                                                                              
name          CharField     Name (Nom,Nimi)                                                                                           
addr1         CharField     Address line before street (Adresszeile vor Straße,Ligne avant le nom de rue,Addressi lisatext enne tänav)
street_prefix CharField     Street prefix (Präfix Straße,Préfixe rue)                                                                 
street        CharField     Street (Straße,Rue,Tänav)                                                                                 
street_no     CharField     No. (Nr.,N°,Nr.)                                                                                          
street_box    CharField     Box (boîte,PK/krt)                                                                                        
addr2         CharField     Address line after street (Adresszeile nach Straße,Ligne après le nom de rue,Aadressilisa pärast tänav)   
zip_code      CharField     Zip code (Postleitzahl,Code postal,Sihtnumber)                                                            
region        CharField     Region (Région,Maakond)                                                                                   
language      LanguageField Language (Sprache,Langue)                                                                                 
email         EmailField    E-Mail (E-mail)                                                                                           
url           URLField      URL                                                                                                       
phone         CharField     Phone (Telefon,Téléphone,Telefon)                                                                         
gsm           CharField     GSM                                                                                                       
fax           CharField     Fax                                                                                                       
remarks       TextField     Remarks (Bemerkungen,Remarques,Märkused)                                                                  
vat_id        CharField     VAT id (MWSt.-Nr.,N° de TVA,KMKR nr)                                                                      
type          ForeignKey    Company type (Firmenart,Type de société,Firmaliik)                                                        
============= ============= ==========================================================================================================

    
Defined in :srcref:`/lino/apps/igen/models.py`

Referenced from
`lino.contacts.Contact.company`_, `lino.ledger.Booking.company`_, `lino.sales.SalesDocument.company`_, `lino.sales.Order.company`_, `lino.sales.Invoice.company`_, `lino.lino.SiteConfig.site_company`_, `lino.finan.DocItem.company`_



.. index::
   single: field;id
   
.. _lino.contacts.Company.id:

Field **Company.id**
====================





Type: AutoField

   
.. index::
   single: field;country
   
.. _lino.contacts.Company.country:

Field **Company.country**
=========================





Type: ForeignKey

   
.. index::
   single: field;city
   
.. _lino.contacts.Company.city:

Field **Company.city**
======================





Type: ForeignKey

   
.. index::
   single: field;name
   
.. _lino.contacts.Company.name:

Field **Company.name**
======================





Type: CharField

   
.. index::
   single: field;addr1
   
.. _lino.contacts.Company.addr1:

Field **Company.addr1**
=======================



Address line before street

Type: CharField

   
.. index::
   single: field;street_prefix
   
.. _lino.contacts.Company.street_prefix:

Field **Company.street_prefix**
===============================



Text to print before name of street, but to ignore for sorting.

Type: CharField

   
.. index::
   single: field;street
   
.. _lino.contacts.Company.street:

Field **Company.street**
========================



Name of street. Without house number.

Type: CharField

   
.. index::
   single: field;street_no
   
.. _lino.contacts.Company.street_no:

Field **Company.street_no**
===========================



House number

Type: CharField

   
.. index::
   single: field;street_box
   
.. _lino.contacts.Company.street_box:

Field **Company.street_box**
============================



Text to print after :attr:`steet_no` on the same line

Type: CharField

   
.. index::
   single: field;addr2
   
.. _lino.contacts.Company.addr2:

Field **Company.addr2**
=======================



Address line to print below street line

Type: CharField

   
.. index::
   single: field;zip_code
   
.. _lino.contacts.Company.zip_code:

Field **Company.zip_code**
==========================





Type: CharField

   
.. index::
   single: field;region
   
.. _lino.contacts.Company.region:

Field **Company.region**
========================





Type: CharField

   
.. index::
   single: field;language
   
.. _lino.contacts.Company.language:

Field **Company.language**
==========================





Type: LanguageField

   
.. index::
   single: field;email
   
.. _lino.contacts.Company.email:

Field **Company.email**
=======================





Type: EmailField

   
.. index::
   single: field;url
   
.. _lino.contacts.Company.url:

Field **Company.url**
=====================





Type: URLField

   
.. index::
   single: field;phone
   
.. _lino.contacts.Company.phone:

Field **Company.phone**
=======================





Type: CharField

   
.. index::
   single: field;gsm
   
.. _lino.contacts.Company.gsm:

Field **Company.gsm**
=====================





Type: CharField

   
.. index::
   single: field;fax
   
.. _lino.contacts.Company.fax:

Field **Company.fax**
=====================





Type: CharField

   
.. index::
   single: field;remarks
   
.. _lino.contacts.Company.remarks:

Field **Company.remarks**
=========================





Type: TextField

   
.. index::
   single: field;vat_id
   
.. _lino.contacts.Company.vat_id:

Field **Company.vat_id**
========================





Type: CharField

   
.. index::
   single: field;type
   
.. _lino.contacts.Company.type:

Field **Company.type**
======================





Type: ForeignKey

   


