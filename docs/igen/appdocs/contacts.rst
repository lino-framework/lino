========
contacts
========



.. currentmodule:: contacts

Defined in :srcref:`/lino/modlib/contacts/models.py`


This module deserves more documentation.

It defines tables like `Person` and `Company`



.. contents:: Table of Contents



.. index::
   pair: model; Contact

.. _lino.contacts.Contact:

-----------------
Model **Contact**
-----------------




Base class for anything that has contact information 
(postal address, email, phone,...).


  
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
============= ============= ==========================================================================================================

    
Defined in :srcref:`/lino/modlib/contacts/models.py`

Referenced from
`lino.mails.Recipient.contact`_, `lino.users.User.contact_ptr`_, `lino.contacts.Role.parent`_, `lino.contacts.Role.child`_, `lino.contacts.Person.contact_ptr`_, `lino.contacts.Company.contact_ptr`_, `lino.ledger.Booking.contact`_, `lino.sales.Customer.contact_ptr`_, `lino.cal.Guest.contact`_, `lino.finan.DocItem.contact`_



.. index::
   single: field;id
   
.. _lino.contacts.Contact.id:

Field **Contact.id**
====================





Type: AutoField

   
.. index::
   single: field;country
   
.. _lino.contacts.Contact.country:

Field **Contact.country**
=========================





Type: ForeignKey

   
.. index::
   single: field;city
   
.. _lino.contacts.Contact.city:

Field **Contact.city**
======================





Type: ForeignKey

   
.. index::
   single: field;name
   
.. _lino.contacts.Contact.name:

Field **Contact.name**
======================





Type: CharField

   
.. index::
   single: field;addr1
   
.. _lino.contacts.Contact.addr1:

Field **Contact.addr1**
=======================



Address line before street

Type: CharField

   
.. index::
   single: field;street_prefix
   
.. _lino.contacts.Contact.street_prefix:

Field **Contact.street_prefix**
===============================



Text to print before name of street, but to ignore for sorting.

Type: CharField

   
.. index::
   single: field;street
   
.. _lino.contacts.Contact.street:

Field **Contact.street**
========================



Name of street. Without house number.

Type: CharField

   
.. index::
   single: field;street_no
   
.. _lino.contacts.Contact.street_no:

Field **Contact.street_no**
===========================



House number

Type: CharField

   
.. index::
   single: field;street_box
   
.. _lino.contacts.Contact.street_box:

Field **Contact.street_box**
============================



Text to print after :attr:`steet_no` on the same line

Type: CharField

   
.. index::
   single: field;addr2
   
.. _lino.contacts.Contact.addr2:

Field **Contact.addr2**
=======================



Address line to print below street line

Type: CharField

   
.. index::
   single: field;zip_code
   
.. _lino.contacts.Contact.zip_code:

Field **Contact.zip_code**
==========================





Type: CharField

   
.. index::
   single: field;region
   
.. _lino.contacts.Contact.region:

Field **Contact.region**
========================





Type: CharField

   
.. index::
   single: field;language
   
.. _lino.contacts.Contact.language:

Field **Contact.language**
==========================





Type: LanguageField

   
.. index::
   single: field;email
   
.. _lino.contacts.Contact.email:

Field **Contact.email**
=======================





Type: EmailField

   
.. index::
   single: field;url
   
.. _lino.contacts.Contact.url:

Field **Contact.url**
=====================





Type: URLField

   
.. index::
   single: field;phone
   
.. _lino.contacts.Contact.phone:

Field **Contact.phone**
=======================





Type: CharField

   
.. index::
   single: field;gsm
   
.. _lino.contacts.Contact.gsm:

Field **Contact.gsm**
=====================





Type: CharField

   
.. index::
   single: field;fax
   
.. _lino.contacts.Contact.fax:

Field **Contact.fax**
=====================





Type: CharField

   
.. index::
   single: field;remarks
   
.. _lino.contacts.Contact.remarks:

Field **Contact.remarks**
=========================





Type: TextField

   


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

  
======= ============== ============================================
name    type           verbose name                                
======= ============== ============================================
id      AutoField      ID                                          
name    BabelCharField Designation (Beschreibung)                  
abbr    BabelCharField Abbreviation (Abkürzung,Abbréviation,Lühend)
abbr_de CharField      Abbreviation (de)                           
abbr_fr CharField      Abbreviation (fr)                           
abbr_nl CharField      Abbreviation (nl)                           
abbr_et CharField      Abbreviation (et)                           
name_de CharField      Designation (de)                            
name_fr CharField      Designation (fr)                            
name_nl CharField      Designation (nl)                            
name_et CharField      Designation (et)                            
======= ============== ============================================

    
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
   pair: model; RoleType

.. _lino.contacts.RoleType:

------------------
Model **RoleType**
------------------




Deserves more documentation.

  
======= ============== ==========================
name    type           verbose name              
======= ============== ==========================
id      AutoField      ID                        
name    BabelCharField Designation (Beschreibung)
name_de CharField      Designation (de)          
name_fr CharField      Designation (fr)          
name_nl CharField      Designation (nl)          
name_et CharField      Designation (et)          
======= ============== ==========================

    
Defined in :srcref:`/lino/modlib/contacts/models.py`

Referenced from
`lino.contacts.Role.type`_



.. index::
   single: field;id
   
.. _lino.contacts.RoleType.id:

Field **RoleType.id**
=====================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.contacts.RoleType.name:

Field **RoleType.name**
=======================





Type: BabelCharField

   
.. index::
   single: field;name_de
   
.. _lino.contacts.RoleType.name_de:

Field **RoleType.name_de**
==========================





Type: CharField

   
.. index::
   single: field;name_fr
   
.. _lino.contacts.RoleType.name_fr:

Field **RoleType.name_fr**
==========================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _lino.contacts.RoleType.name_nl:

Field **RoleType.name_nl**
==========================





Type: CharField

   
.. index::
   single: field;name_et
   
.. _lino.contacts.RoleType.name_et:

Field **RoleType.name_et**
==========================





Type: CharField

   


.. index::
   pair: model; Role

.. _lino.contacts.Role:

--------------
Model **Role**
--------------




The role of a given :class:`Person` in a given :class:`Company`.

  
====== ========== =============================
name   type       verbose name                 
====== ========== =============================
id     AutoField  ID                           
parent ForeignKey Parent Contact (Kontakt für) 
child  ForeignKey Child Contact (Kontaktperson)
type   ForeignKey Contact Role (Funktion)      
====== ========== =============================

    
Defined in :srcref:`/lino/modlib/contacts/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.contacts.Role.id:

Field **Role.id**
=================





Type: AutoField

   
.. index::
   single: field;parent
   
.. _lino.contacts.Role.parent:

Field **Role.parent**
=====================





Type: ForeignKey

   
.. index::
   single: field;child
   
.. _lino.contacts.Role.child:

Field **Role.child**
====================





Type: ForeignKey

   
.. index::
   single: field;type
   
.. _lino.contacts.Role.type:

Field **Role.type**
===================





Type: ForeignKey

   


.. index::
   pair: model; Person

.. _lino.contacts.Person:

----------------
Model **Person**
----------------



Person(id, country_id, city_id, name, addr1, street_prefix, street, street_no, street_box, addr2, zip_code, region, language, email, url, phone, gsm, fax, remarks, contact_ptr_id, first_name, last_name, title, sex, birth_date, birth_date_circa)
  
================ ============= ==========================================================================================================
name             type          verbose name                                                                                              
================ ============= ==========================================================================================================
id               AutoField     ID                                                                                                        
country          ForeignKey    Country (Land)                                                                                            
city             ForeignKey    City (Stadt)                                                                                              
name             CharField     Name (Nom,Nimi)                                                                                           
addr1            CharField     Address line before street (Adresszeile vor Straße,Ligne avant le nom de rue,Addressi lisatext enne tänav)
street_prefix    CharField     Street prefix (Präfix Straße,Préfixe rue)                                                                 
street           CharField     Street (Straße,Rue,Tänav)                                                                                 
street_no        CharField     No. (Nr.,N°,Nr.)                                                                                          
street_box       CharField     Box (boîte,PK/krt)                                                                                        
addr2            CharField     Address line after street (Adresszeile nach Straße,Ligne après le nom de rue,Aadressilisa pärast tänav)   
zip_code         CharField     Zip code (Postleitzahl,Code postal,Sihtnumber)                                                            
region           CharField     Region (Région,Maakond)                                                                                   
language         LanguageField Language (Sprache,Langue)                                                                                 
email            EmailField    E-Mail (E-mail)                                                                                           
url              URLField      URL                                                                                                       
phone            CharField     Phone (Telefon,Téléphone,Telefon)                                                                         
gsm              CharField     GSM                                                                                                       
fax              CharField     Fax                                                                                                       
remarks          TextField     Remarks (Bemerkungen,Remarques,Märkused)                                                                  
contact_ptr      OneToOneField Contact (Kontakt)                                                                                         
first_name       CharField     First name                                                                                                
last_name        CharField     Last name                                                                                                 
title            CharField     Title                                                                                                     
sex              CharField     Sex                                                                                                       
birth_date       DateField     Birth date (Geburtsdatum)                                                                                 
birth_date_circa BooleanField  not exact (ungenau)                                                                                       
================ ============= ==========================================================================================================

    
Defined in :srcref:`/lino/apps/igen/models.py`

Referenced from




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
   single: field;contact_ptr
   
.. _lino.contacts.Person.contact_ptr:

Field **Person.contact_ptr**
============================





Type: OneToOneField

   
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
   single: field;birth_date
   
.. _lino.contacts.Person.birth_date:

Field **Person.birth_date**
===========================





Type: DateField

   
.. index::
   single: field;birth_date_circa
   
.. _lino.contacts.Person.birth_date_circa:

Field **Person.birth_date_circa**
=================================





Type: BooleanField

   


.. index::
   pair: model; Company

.. _lino.contacts.Company:

-----------------
Model **Company**
-----------------



Company(id, country_id, city_id, name, addr1, street_prefix, street, street_no, street_box, addr2, zip_code, region, language, email, url, phone, gsm, fax, remarks, contact_ptr_id, vat_id, type_id)
  
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
contact_ptr   OneToOneField Contact (Kontakt)                                                                                         
vat_id        CharField     VAT id (MWSt.-Nr.,N° de TVA,KMKR nr)                                                                      
type          ForeignKey    Company type (Firmenart,Type de société,Firmaliik)                                                        
============= ============= ==========================================================================================================

    
Defined in :srcref:`/lino/apps/igen/models.py`

Referenced from
`lino.lino.SiteConfig.site_company`_



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
   single: field;contact_ptr
   
.. _lino.contacts.Company.contact_ptr:

Field **Company.contact_ptr**
=============================





Type: OneToOneField

   
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

   


