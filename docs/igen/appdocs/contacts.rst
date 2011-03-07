========
contacts
========



.. currentmodule:: contacts

Defined in :srcref:`/lino/modlib/contacts/models.py`


This module deserves more documentation.

It defines tables like `Person` and `Company`




.. index::
   pair: model; CompanyType
   single: field;id
   single: field;name
   single: field;abbr
   single: field;name_de
   single: field;name_fr
   single: field;name_nl
   single: field;name_et
   single: field;abbr_de
   single: field;abbr_fr
   single: field;abbr_nl
   single: field;abbr_et

.. _igen.contacts.CompanyType:

---------------------
Model ``CompanyType``
---------------------




    Implements the :class:`contacts.CompanyType` convention.
    
  
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
   pair: model; ContactType
   single: field;id
   single: field;name
   single: field;name_de
   single: field;name_fr
   single: field;name_nl
   single: field;name_et

.. _igen.contacts.ContactType:

---------------------
Model ``ContactType``
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
   pair: model; Contact
   single: field;id
   single: field;person
   single: field;company
   single: field;type
   single: field;payment_term
   single: field;vat_exempt
   single: field;item_vat

.. _igen.contacts.Contact:

-----------------
Model ``Contact``
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
   pair: model; Person
   single: field;id
   single: field;name
   single: field;addr1
   single: field;street
   single: field;street_no
   single: field;street_box
   single: field;addr2
   single: field;country
   single: field;city
   single: field;zip_code
   single: field;region
   single: field;language
   single: field;email
   single: field;url
   single: field;phone
   single: field;gsm
   single: field;fax
   single: field;remarks
   single: field;first_name
   single: field;last_name
   single: field;title

.. _igen.contacts.Person:

----------------
Model ``Person``
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

    
Defined in :srcref:`/lino/sites/igen/models.py`


.. index::
   pair: model; Company
   single: field;id
   single: field;name
   single: field;addr1
   single: field;street
   single: field;street_no
   single: field;street_box
   single: field;addr2
   single: field;country
   single: field;city
   single: field;zip_code
   single: field;region
   single: field;language
   single: field;email
   single: field;url
   single: field;phone
   single: field;gsm
   single: field;fax
   single: field;remarks
   single: field;vat_id
   single: field;type

.. _igen.contacts.Company:

-----------------
Model ``Company``
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

    
Defined in :srcref:`/lino/sites/igen/models.py`


