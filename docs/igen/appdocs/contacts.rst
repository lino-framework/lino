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

.. _igen.contacts.CompanyType:

---------------------
Model **CompanyType**
---------------------




Represents a possible choice for the :class:`Company`.type
field.
Implemented by 
:ref:`dsbe.contacts.CompanyType`
:ref:`igen.contacts.CompanyType`

  
======= ============== =================================
name    type           verbose name                     
======= ============== =================================
id      AutoField      ID                               
name    BabelCharField Designation (Bezeichnung,Nimetus)
abbr    BabelCharField Abbreviation (Abkürzung,Lühend)  
name_de CharField      Designation (de)                 
name_fr CharField      Designation (fr)                 
name_nl CharField      Designation (nl)                 
name_et CharField      Designation (et)                 
abbr_de CharField      Abbreviation (de)                
abbr_fr CharField      Abbreviation (fr)                
abbr_nl CharField      Abbreviation (nl)                
abbr_et CharField      Abbreviation (et)                
======= ============== =================================

    
Defined in :srcref:`/lino/modlib/contacts/models.py`

.. index::
   single: field;id
   
.. _igen.contacts.CompanyType.id:

Field **CompanyType.id**
========================





Type: AutoField

   
.. index::
   single: field;name
   
.. _igen.contacts.CompanyType.name:

Field **CompanyType.name**
==========================





Type: BabelCharField

   
.. index::
   single: field;abbr
   
.. _igen.contacts.CompanyType.abbr:

Field **CompanyType.abbr**
==========================





Type: BabelCharField

   
.. index::
   single: field;name_de
   
.. _igen.contacts.CompanyType.name_de:

Field **CompanyType.name_de**
=============================





Type: CharField

   
.. index::
   single: field;name_fr
   
.. _igen.contacts.CompanyType.name_fr:

Field **CompanyType.name_fr**
=============================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _igen.contacts.CompanyType.name_nl:

Field **CompanyType.name_nl**
=============================





Type: CharField

   
.. index::
   single: field;name_et
   
.. _igen.contacts.CompanyType.name_et:

Field **CompanyType.name_et**
=============================





Type: CharField

   
.. index::
   single: field;abbr_de
   
.. _igen.contacts.CompanyType.abbr_de:

Field **CompanyType.abbr_de**
=============================





Type: CharField

   
.. index::
   single: field;abbr_fr
   
.. _igen.contacts.CompanyType.abbr_fr:

Field **CompanyType.abbr_fr**
=============================





Type: CharField

   
.. index::
   single: field;abbr_nl
   
.. _igen.contacts.CompanyType.abbr_nl:

Field **CompanyType.abbr_nl**
=============================





Type: CharField

   
.. index::
   single: field;abbr_et
   
.. _igen.contacts.CompanyType.abbr_et:

Field **CompanyType.abbr_et**
=============================





Type: CharField

   


.. index::
   pair: model; ContactType

.. _igen.contacts.ContactType:

---------------------
Model **ContactType**
---------------------




Implements the :class:`contacts.ContactType` convention.

  
======= ============== =================================
name    type           verbose name                     
======= ============== =================================
id      AutoField      ID                               
name    BabelCharField Designation (Bezeichnung,Nimetus)
name_de CharField      Designation (de)                 
name_fr CharField      Designation (fr)                 
name_nl CharField      Designation (nl)                 
name_et CharField      Designation (et)                 
======= ============== =================================

    
Defined in :srcref:`/lino/modlib/contacts/models.py`

.. index::
   single: field;id
   
.. _igen.contacts.ContactType.id:

Field **ContactType.id**
========================





Type: AutoField

   
.. index::
   single: field;name
   
.. _igen.contacts.ContactType.name:

Field **ContactType.name**
==========================





Type: BabelCharField

   
.. index::
   single: field;name_de
   
.. _igen.contacts.ContactType.name_de:

Field **ContactType.name_de**
=============================





Type: CharField

   
.. index::
   single: field;name_fr
   
.. _igen.contacts.ContactType.name_fr:

Field **ContactType.name_fr**
=============================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _igen.contacts.ContactType.name_nl:

Field **ContactType.name_nl**
=============================





Type: CharField

   
.. index::
   single: field;name_et
   
.. _igen.contacts.ContactType.name_et:

Field **ContactType.name_et**
=============================





Type: CharField

   


.. index::
   pair: model; Contact

.. _igen.contacts.Contact:

-----------------
Model **Contact**
-----------------




Represents a :class:`Person` having a (more or less known) 
role in a :class:`Company`.

  
============ ============ ======================================
name         type         verbose name                          
============ ============ ======================================
id           AutoField    ID                                    
person       ForeignKey   person (Person,isik)                  
company      ForeignKey   company (Firma,firma)                 
type         ForeignKey   contact type (Kontaktart,Kontaktiliik)
payment_term ForeignKey   payment term (Tasumistingimused)      
vat_exempt   BooleanField VAT exempt                            
item_vat     BooleanField item_vat                              
============ ============ ======================================

    
Defined in :srcref:`/lino/modlib/contacts/models.py`

.. index::
   single: field;id
   
.. _igen.contacts.Contact.id:

Field **Contact.id**
====================





Type: AutoField

   
.. index::
   single: field;person
   
.. _igen.contacts.Contact.person:

Field **Contact.person**
========================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _igen.contacts.Contact.company:

Field **Contact.company**
=========================





Type: ForeignKey

   
.. index::
   single: field;type
   
.. _igen.contacts.Contact.type:

Field **Contact.type**
======================





Type: ForeignKey

   
.. index::
   single: field;payment_term
   
.. _igen.contacts.Contact.payment_term:

Field **Contact.payment_term**
==============================





Type: ForeignKey

   
.. index::
   single: field;vat_exempt
   
.. _igen.contacts.Contact.vat_exempt:

Field **Contact.vat_exempt**
============================





Type: BooleanField

   
.. index::
   single: field;item_vat
   
.. _igen.contacts.Contact.item_vat:

Field **Contact.item_vat**
==========================





Type: BooleanField

   


.. index::
   pair: model; Person

.. _igen.contacts.Person:

----------------
Model **Person**
----------------



Person(id, name, addr1, street, street_no, street_box, addr2, country_id, city_id, zip_code, region, language, email, url, phone, gsm, fax, remarks, first_name, last_name, title)
  
========== ============= =========================================================
name       type          verbose name                                             
========== ============= =========================================================
id         AutoField     ID                                                       
name       CharField     Name (Nimi)                                              
addr1      CharField     Address line before street (Addressi lisatext enne tänav)
street     CharField     Street (Straße,Rue,Tänav)                                
street_no  CharField     No. (Nr.,N°,Nr.)                                         
street_box CharField     Box (boîte,PK/krt)                                       
addr2      CharField     Address line after street (Aadressilisa pärast tänav)    
country    ForeignKey    Country (Land,Maa)                                       
city       ForeignKey    City (Stadt,Linn)                                        
zip_code   CharField     Zip code (Postleitzahl,Sihtnumber)                       
region     CharField     Region (Maakond)                                         
language   LanguageField Language (Sprache)                                       
email      EmailField    E-Mail                                                   
url        URLField      URL                                                      
phone      CharField     Phone (Telefon,Telefon)                                  
gsm        CharField     GSM                                                      
fax        CharField     Fax                                                      
remarks    TextField     Remarks (Märkused)                                       
first_name CharField     First name (Vorname,Eesnimi)                             
last_name  CharField     Last name (Familienname,Perekonnanimi)                   
title      CharField     Title (Anrede,Pealkiri)                                  
========== ============= =========================================================

    
Defined in :srcref:`/lino/apps/igen/models.py`

.. index::
   single: field;id
   
.. _igen.contacts.Person.id:

Field **Person.id**
===================





Type: AutoField

   
.. index::
   single: field;name
   
.. _igen.contacts.Person.name:

Field **Person.name**
=====================





Type: CharField

   
.. index::
   single: field;addr1
   
.. _igen.contacts.Person.addr1:

Field **Person.addr1**
======================



Address line before street

Type: CharField

   
.. index::
   single: field;street
   
.. _igen.contacts.Person.street:

Field **Person.street**
=======================



Name of street. Without house number.

Type: CharField

   
.. index::
   single: field;street_no
   
.. _igen.contacts.Person.street_no:

Field **Person.street_no**
==========================



House number

Type: CharField

   
.. index::
   single: field;street_box
   
.. _igen.contacts.Person.street_box:

Field **Person.street_box**
===========================



Text to print after :attr:`steet_no` on the same line

Type: CharField

   
.. index::
   single: field;addr2
   
.. _igen.contacts.Person.addr2:

Field **Person.addr2**
======================



Address line to print below street line

Type: CharField

   
.. index::
   single: field;country
   
.. _igen.contacts.Person.country:

Field **Person.country**
========================



The country where this contact is located.

Type: ForeignKey

   
.. index::
   single: field;city
   
.. _igen.contacts.Person.city:

Field **Person.city**
=====================




        The city where this contact is located.
        The list of choices for this field is context-sensitive
        and depends on the :attr:`country`.
        

Type: ForeignKey

   
.. index::
   single: field;zip_code
   
.. _igen.contacts.Person.zip_code:

Field **Person.zip_code**
=========================





Type: CharField

   
.. index::
   single: field;region
   
.. _igen.contacts.Person.region:

Field **Person.region**
=======================





Type: CharField

   
.. index::
   single: field;language
   
.. _igen.contacts.Person.language:

Field **Person.language**
=========================





Type: LanguageField

   
.. index::
   single: field;email
   
.. _igen.contacts.Person.email:

Field **Person.email**
======================





Type: EmailField

   
.. index::
   single: field;url
   
.. _igen.contacts.Person.url:

Field **Person.url**
====================





Type: URLField

   
.. index::
   single: field;phone
   
.. _igen.contacts.Person.phone:

Field **Person.phone**
======================





Type: CharField

   
.. index::
   single: field;gsm
   
.. _igen.contacts.Person.gsm:

Field **Person.gsm**
====================





Type: CharField

   
.. index::
   single: field;fax
   
.. _igen.contacts.Person.fax:

Field **Person.fax**
====================





Type: CharField

   
.. index::
   single: field;remarks
   
.. _igen.contacts.Person.remarks:

Field **Person.remarks**
========================





Type: TextField

   
.. index::
   single: field;first_name
   
.. _igen.contacts.Person.first_name:

Field **Person.first_name**
===========================





Type: CharField

   
.. index::
   single: field;last_name
   
.. _igen.contacts.Person.last_name:

Field **Person.last_name**
==========================





Type: CharField

   
.. index::
   single: field;title
   
.. _igen.contacts.Person.title:

Field **Person.title**
======================





Type: CharField

   


.. index::
   pair: model; Company

.. _igen.contacts.Company:

-----------------
Model **Company**
-----------------



Company(id, name, addr1, street, street_no, street_box, addr2, country_id, city_id, zip_code, region, language, email, url, phone, gsm, fax, remarks, vat_id, type_id)
  
========== ============= =========================================================
name       type          verbose name                                             
========== ============= =========================================================
id         AutoField     ID                                                       
name       CharField     Name (Nimi)                                              
addr1      CharField     Address line before street (Addressi lisatext enne tänav)
street     CharField     Street (Straße,Rue,Tänav)                                
street_no  CharField     No. (Nr.,N°,Nr.)                                         
street_box CharField     Box (boîte,PK/krt)                                       
addr2      CharField     Address line after street (Aadressilisa pärast tänav)    
country    ForeignKey    Country (Land,Maa)                                       
city       ForeignKey    City (Stadt,Linn)                                        
zip_code   CharField     Zip code (Postleitzahl,Sihtnumber)                       
region     CharField     Region (Maakond)                                         
language   LanguageField Language (Sprache)                                       
email      EmailField    E-Mail                                                   
url        URLField      URL                                                      
phone      CharField     Phone (Telefon,Telefon)                                  
gsm        CharField     GSM                                                      
fax        CharField     Fax                                                      
remarks    TextField     Remarks (Märkused)                                       
vat_id     CharField     VAT id (MWSt.-Nr.,KMKR nr)                               
type       ForeignKey    Company type (Firmenart,Firmaliik)                       
========== ============= =========================================================

    
Defined in :srcref:`/lino/apps/igen/models.py`

.. index::
   single: field;id
   
.. _igen.contacts.Company.id:

Field **Company.id**
====================





Type: AutoField

   
.. index::
   single: field;name
   
.. _igen.contacts.Company.name:

Field **Company.name**
======================





Type: CharField

   
.. index::
   single: field;addr1
   
.. _igen.contacts.Company.addr1:

Field **Company.addr1**
=======================



Address line before street

Type: CharField

   
.. index::
   single: field;street
   
.. _igen.contacts.Company.street:

Field **Company.street**
========================



Name of street. Without house number.

Type: CharField

   
.. index::
   single: field;street_no
   
.. _igen.contacts.Company.street_no:

Field **Company.street_no**
===========================



House number

Type: CharField

   
.. index::
   single: field;street_box
   
.. _igen.contacts.Company.street_box:

Field **Company.street_box**
============================



Text to print after :attr:`steet_no` on the same line

Type: CharField

   
.. index::
   single: field;addr2
   
.. _igen.contacts.Company.addr2:

Field **Company.addr2**
=======================



Address line to print below street line

Type: CharField

   
.. index::
   single: field;country
   
.. _igen.contacts.Company.country:

Field **Company.country**
=========================



The country where this contact is located.

Type: ForeignKey

   
.. index::
   single: field;city
   
.. _igen.contacts.Company.city:

Field **Company.city**
======================




        The city where this contact is located.
        The list of choices for this field is context-sensitive
        and depends on the :attr:`country`.
        

Type: ForeignKey

   
.. index::
   single: field;zip_code
   
.. _igen.contacts.Company.zip_code:

Field **Company.zip_code**
==========================





Type: CharField

   
.. index::
   single: field;region
   
.. _igen.contacts.Company.region:

Field **Company.region**
========================





Type: CharField

   
.. index::
   single: field;language
   
.. _igen.contacts.Company.language:

Field **Company.language**
==========================





Type: LanguageField

   
.. index::
   single: field;email
   
.. _igen.contacts.Company.email:

Field **Company.email**
=======================





Type: EmailField

   
.. index::
   single: field;url
   
.. _igen.contacts.Company.url:

Field **Company.url**
=====================





Type: URLField

   
.. index::
   single: field;phone
   
.. _igen.contacts.Company.phone:

Field **Company.phone**
=======================





Type: CharField

   
.. index::
   single: field;gsm
   
.. _igen.contacts.Company.gsm:

Field **Company.gsm**
=====================





Type: CharField

   
.. index::
   single: field;fax
   
.. _igen.contacts.Company.fax:

Field **Company.fax**
=====================





Type: CharField

   
.. index::
   single: field;remarks
   
.. _igen.contacts.Company.remarks:

Field **Company.remarks**
=========================





Type: TextField

   
.. index::
   single: field;vat_id
   
.. _igen.contacts.Company.vat_id:

Field **Company.vat_id**
========================





Type: CharField

   
.. index::
   single: field;type
   
.. _igen.contacts.Company.type:

Field **Company.type**
======================





Type: ForeignKey

   


