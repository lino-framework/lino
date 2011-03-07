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

.. _dsbe.contacts.CompanyType:

---------------------
Model **CompanyType**
---------------------




Implements the :class:`contacts.CompanyType` convention.

  
============= ============== ===========================
name          type           verbose name               
============= ============== ===========================
id            AutoField      ID                         
name          BabelCharField Designation (Beschreibung) 
abbr          BabelCharField Abbreviation (Abkürzung)   
name_fr       CharField      Designation (fr)           
name_nl       CharField      Designation (nl)           
name_en       CharField      Designation (en)           
abbr_fr       CharField      Abbreviation (fr)          
abbr_nl       CharField      Abbreviation (nl)          
abbr_en       CharField      Abbreviation (en)          
contract_type ForeignKey     contract type (Vertragsart)
============= ============== ===========================

    
Defined in :srcref:`/lino/modlib/contacts/models.py`

.. index::
   single: field;id
   
.. _dsbe.contacts.CompanyType.id:

Field **CompanyType.id**
========================





Type: AutoField

   
.. index::
   single: field;name
   
.. _dsbe.contacts.CompanyType.name:

Field **CompanyType.name**
==========================





Type: BabelCharField

   
.. index::
   single: field;abbr
   
.. _dsbe.contacts.CompanyType.abbr:

Field **CompanyType.abbr**
==========================





Type: BabelCharField

   
.. index::
   single: field;name_fr
   
.. _dsbe.contacts.CompanyType.name_fr:

Field **CompanyType.name_fr**
=============================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _dsbe.contacts.CompanyType.name_nl:

Field **CompanyType.name_nl**
=============================





Type: CharField

   
.. index::
   single: field;name_en
   
.. _dsbe.contacts.CompanyType.name_en:

Field **CompanyType.name_en**
=============================





Type: CharField

   
.. index::
   single: field;abbr_fr
   
.. _dsbe.contacts.CompanyType.abbr_fr:

Field **CompanyType.abbr_fr**
=============================





Type: CharField

   
.. index::
   single: field;abbr_nl
   
.. _dsbe.contacts.CompanyType.abbr_nl:

Field **CompanyType.abbr_nl**
=============================





Type: CharField

   
.. index::
   single: field;abbr_en
   
.. _dsbe.contacts.CompanyType.abbr_en:

Field **CompanyType.abbr_en**
=============================





Type: CharField

   
.. index::
   single: field;contract_type
   
.. _dsbe.contacts.CompanyType.contract_type:

Field **CompanyType.contract_type**
===================================





Type: ForeignKey

   


.. index::
   pair: model; ContactType

.. _dsbe.contacts.ContactType:

---------------------
Model **ContactType**
---------------------




Implements the :class:`contacts.ContactType` convention.

  
======= ============== ==========================
name    type           verbose name              
======= ============== ==========================
id      AutoField      ID                        
name    BabelCharField Designation (Beschreibung)
name_fr CharField      Designation (fr)          
name_nl CharField      Designation (nl)          
name_en CharField      Designation (en)          
======= ============== ==========================

    
Defined in :srcref:`/lino/modlib/contacts/models.py`

.. index::
   single: field;id
   
.. _dsbe.contacts.ContactType.id:

Field **ContactType.id**
========================





Type: AutoField

   
.. index::
   single: field;name
   
.. _dsbe.contacts.ContactType.name:

Field **ContactType.name**
==========================





Type: BabelCharField

   
.. index::
   single: field;name_fr
   
.. _dsbe.contacts.ContactType.name_fr:

Field **ContactType.name_fr**
=============================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _dsbe.contacts.ContactType.name_nl:

Field **ContactType.name_nl**
=============================





Type: CharField

   
.. index::
   single: field;name_en
   
.. _dsbe.contacts.ContactType.name_en:

Field **ContactType.name_en**
=============================





Type: CharField

   


.. index::
   pair: model; Contact

.. _dsbe.contacts.Contact:

-----------------
Model **Contact**
-----------------




Represents a :class:`Person` having a (more or less known) 
role in a :class:`Company`.

  
======= ========== =========================
name    type       verbose name             
======= ========== =========================
id      AutoField  ID                       
person  ForeignKey person (Person)          
company ForeignKey company (Firma)          
type    ForeignKey contact type (Kontaktart)
======= ========== =========================

    
Defined in :srcref:`/lino/modlib/contacts/models.py`

.. index::
   single: field;id
   
.. _dsbe.contacts.Contact.id:

Field **Contact.id**
====================





Type: AutoField

   
.. index::
   single: field;person
   
.. _dsbe.contacts.Contact.person:

Field **Contact.person**
========================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _dsbe.contacts.Contact.company:

Field **Contact.company**
=========================





Type: ForeignKey

   
.. index::
   single: field;type
   
.. _dsbe.contacts.Contact.type:

Field **Contact.type**
======================





Type: ForeignKey

   


.. index::
   pair: model; Person

.. _dsbe.contacts.Person:

----------------
Model **Person**
----------------




Represents a physical person.


  
=========================== ================= ======================================================
name                        type              verbose name                                          
=========================== ================= ======================================================
name                        CharField         Name                                                  
addr1                       CharField         Address line before street                            
street                      CharField         Street (Straße,Rue)                                   
street_no                   CharField         No. (Nr.,N°)                                          
street_box                  CharField         Box (boîte)                                           
addr2                       CharField         Address line after street                             
country                     ForeignKey        Country (Land)                                        
city                        ForeignKey        City (Stadt)                                          
zip_code                    CharField         Zip code (Postleitzahl)                               
region                      CharField         Region                                                
language                    LanguageField     Language (Sprache)                                    
email                       EmailField        E-Mail                                                
url                         URLField          URL                                                   
phone                       CharField         Phone (Telefon)                                       
gsm                         CharField         GSM                                                   
fax                         CharField         Fax                                                   
remarks                     TextField         Remarks (Bemerkungen)                                 
first_name                  CharField         First name (Vorname)                                  
last_name                   CharField         Last name (Familienname)                              
title                       CharField         Title (Anrede)                                        
id                          AutoField         Partner # (Partnernummer)                             
is_active                   BooleanField      is active (aktiv)                                     
activity                    ForeignKey        Activity (Beruf)                                      
bank_account1               CharField         Bank account 1 (Bankkonto 1)                          
bank_account2               CharField         Bank account 2 (Bankkonto 2)                          
gesdos_id                   CharField         Gesdos ID (Gesdos-Nr)                                 
is_cpas                     BooleanField      receives social help (Sozialhilfeempfänger)           
is_senior                   BooleanField      is senior (Altenheim)                                 
group                       ForeignKey        Group (Gruppe)                                        
coached_from                DateField         Coached from (Begleitet seit)                         
coached_until               DateField         until (bis)                                           
coach1                      ForeignKey        Coach 1 (Begleiter 1)                                 
coach2                      ForeignKey        Coach 2 (Begleiter 2)                                 
sex                         CharField         Sex (Geschlecht)                                      
birth_date                  DateField         Birth date (Geburtsdatum)                             
birth_date_circa            BooleanField      not exact (circa)                                     
birth_place                 CharField         Birth place (Geburtsort)                              
birth_country               ForeignKey        Birth country (Geburtsland)                           
civil_state                 CharField         Civil state (Zivilstand)                              
national_id                 CharField         National ID (NR-Nummer)                               
health_insurance            ForeignKey        Health insurance (Krankenkasse)                       
pharmacy                    ForeignKey        Pharmacy (Apotheke)                                   
nationality                 ForeignKey        Nationality (Staatsangehörigkeit)                     
card_number                 CharField         eID card number (eID-Kartennummer)                    
card_valid_from             DateField         ID card valid from (ID-Karte gültig von)              
card_valid_until            DateField         until (bis)                                           
card_type                   CharField         eID card type (eID-Kartenart)                         
card_issuer                 CharField         eID card issuer (eID-Karte ausgestellt durch)         
noble_condition             CharField         noble condition (Adelstitel)                          
residence_type              SmallIntegerField Residence type (Eintragen)                            
in_belgium_since            DateField         Lives in Belgium since (Lebt in Belgien seit)         
unemployed_since            DateField         Seeking work since (eingetragen seit)                 
needs_residence_permit      BooleanField      Needs residence permit (Braucht Aufenthaltserlaubnis) 
needs_work_permit           BooleanField      Needs work permit (Braucht Arb.Erl.)                  
work_permit_suspended_until DateField         suspended until (Wartezeit bis)                       
aid_type                    ForeignKey        aid type (Sozialhilfeart)                             
income_ag                   BooleanField      Arbeitslosengeld                                      
income_wg                   BooleanField      Wartegeld                                             
income_kg                   BooleanField      Krankengeld                                           
income_rente                BooleanField      Rente                                                 
income_misc                 BooleanField      Andere                                                
is_seeking                  BooleanField      is seeking work (Arbeit suchend)                      
unavailable_until           DateField         Unavailable until (Nicht verfügbar bis)               
unavailable_why             CharField         reason (Grund)                                        
native_language             ForeignKey        Native language (Muttersprache)                       
obstacles                   TextField         Obstacles (Hindernisse)                               
skills                      TextField         Other skills (Sonstige Fähikeiten)                    
job_agents                  CharField         Job agents (Interim-Agenturen)                        
job_office_contact          ForeignKey        Contact person at local job office (Kontaktperson ADG)
=========================== ================= ======================================================

    
Defined in :srcref:`/lino/sites/dsbe/models.py`

.. index::
   single: field;name
   
.. _dsbe.contacts.Person.name:

Field **Person.name**
=====================





Type: CharField

   
.. index::
   single: field;addr1
   
.. _dsbe.contacts.Person.addr1:

Field **Person.addr1**
======================



Address line before street

Type: CharField

   
.. index::
   single: field;street
   
.. _dsbe.contacts.Person.street:

Field **Person.street**
=======================



Name of street. Without house number.

Type: CharField

   
.. index::
   single: field;street_no
   
.. _dsbe.contacts.Person.street_no:

Field **Person.street_no**
==========================



House number

Type: CharField

   
.. index::
   single: field;street_box
   
.. _dsbe.contacts.Person.street_box:

Field **Person.street_box**
===========================



Text to print after :attr:`steet_no` on the same line

Type: CharField

   
.. index::
   single: field;addr2
   
.. _dsbe.contacts.Person.addr2:

Field **Person.addr2**
======================



Address line to print below street line

Type: CharField

   
.. index::
   single: field;country
   
.. _dsbe.contacts.Person.country:

Field **Person.country**
========================



The country where this contact is located.

Type: ForeignKey

   
.. index::
   single: field;city
   
.. _dsbe.contacts.Person.city:

Field **Person.city**
=====================




        The city where this contact is located.
        The list of choices for this field is context-sensitive
        and depends on the :attr:`country`.
        

Type: ForeignKey

   
.. index::
   single: field;zip_code
   
.. _dsbe.contacts.Person.zip_code:

Field **Person.zip_code**
=========================





Type: CharField

   
.. index::
   single: field;region
   
.. _dsbe.contacts.Person.region:

Field **Person.region**
=======================





Type: CharField

   
.. index::
   single: field;language
   
.. _dsbe.contacts.Person.language:

Field **Person.language**
=========================





Type: LanguageField

   
.. index::
   single: field;email
   
.. _dsbe.contacts.Person.email:

Field **Person.email**
======================





Type: EmailField

   
.. index::
   single: field;url
   
.. _dsbe.contacts.Person.url:

Field **Person.url**
====================





Type: URLField

   
.. index::
   single: field;phone
   
.. _dsbe.contacts.Person.phone:

Field **Person.phone**
======================





Type: CharField

   
.. index::
   single: field;gsm
   
.. _dsbe.contacts.Person.gsm:

Field **Person.gsm**
====================





Type: CharField

   
.. index::
   single: field;fax
   
.. _dsbe.contacts.Person.fax:

Field **Person.fax**
====================





Type: CharField

   
.. index::
   single: field;remarks
   
.. _dsbe.contacts.Person.remarks:

Field **Person.remarks**
========================





Type: TextField

   
.. index::
   single: field;first_name
   
.. _dsbe.contacts.Person.first_name:

Field **Person.first_name**
===========================





Type: CharField

   
.. index::
   single: field;last_name
   
.. _dsbe.contacts.Person.last_name:

Field **Person.last_name**
==========================





Type: CharField

   
.. index::
   single: field;title
   
.. _dsbe.contacts.Person.title:

Field **Person.title**
======================





Type: CharField

   
.. index::
   single: field;id
   
.. _dsbe.contacts.Person.id:

Field **Person.id**
===================





Type: AutoField

   
.. index::
   single: field;is_active
   
.. _dsbe.contacts.Person.is_active:

Field **Person.is_active**
==========================





Type: BooleanField

   
.. index::
   single: field;activity
   
.. _dsbe.contacts.Person.activity:

Field **Person.activity**
=========================





Type: ForeignKey

   
.. index::
   single: field;bank_account1
   
.. _dsbe.contacts.Person.bank_account1:

Field **Person.bank_account1**
==============================





Type: CharField

   
.. index::
   single: field;bank_account2
   
.. _dsbe.contacts.Person.bank_account2:

Field **Person.bank_account2**
==============================





Type: CharField

   
.. index::
   single: field;gesdos_id
   
.. _dsbe.contacts.Person.gesdos_id:

Field **Person.gesdos_id**
==========================





Type: CharField

   
.. index::
   single: field;is_cpas
   
.. _dsbe.contacts.Person.is_cpas:

Field **Person.is_cpas**
========================





Type: BooleanField

   
.. index::
   single: field;is_senior
   
.. _dsbe.contacts.Person.is_senior:

Field **Person.is_senior**
==========================





Type: BooleanField

   
.. index::
   single: field;group
   
.. _dsbe.contacts.Person.group:

Field **Person.group**
======================





Type: ForeignKey

   
.. index::
   single: field;coached_from
   
.. _dsbe.contacts.Person.coached_from:

Field **Person.coached_from**
=============================





Type: DateField

   
.. index::
   single: field;coached_until
   
.. _dsbe.contacts.Person.coached_until:

Field **Person.coached_until**
==============================





Type: DateField

   
.. index::
   single: field;coach1
   
.. _dsbe.contacts.Person.coach1:

Field **Person.coach1**
=======================





Type: ForeignKey

   
.. index::
   single: field;coach2
   
.. _dsbe.contacts.Person.coach2:

Field **Person.coach2**
=======================





Type: ForeignKey

   
.. index::
   single: field;sex
   
.. _dsbe.contacts.Person.sex:

Field **Person.sex**
====================





Type: CharField

   
.. index::
   single: field;birth_date
   
.. _dsbe.contacts.Person.birth_date:

Field **Person.birth_date**
===========================





Type: DateField

   
.. index::
   single: field;birth_date_circa
   
.. _dsbe.contacts.Person.birth_date_circa:

Field **Person.birth_date_circa**
=================================





Type: BooleanField

   
.. index::
   single: field;birth_place
   
.. _dsbe.contacts.Person.birth_place:

Field **Person.birth_place**
============================





Type: CharField

   
.. index::
   single: field;birth_country
   
.. _dsbe.contacts.Person.birth_country:

Field **Person.birth_country**
==============================





Type: ForeignKey

   
.. index::
   single: field;civil_state
   
.. _dsbe.contacts.Person.civil_state:

Field **Person.civil_state**
============================





Type: CharField

   
.. index::
   single: field;national_id
   
.. _dsbe.contacts.Person.national_id:

Field **Person.national_id**
============================





Type: CharField

   
.. index::
   single: field;health_insurance
   
.. _dsbe.contacts.Person.health_insurance:

Field **Person.health_insurance**
=================================





Type: ForeignKey

   
.. index::
   single: field;pharmacy
   
.. _dsbe.contacts.Person.pharmacy:

Field **Person.pharmacy**
=========================





Type: ForeignKey

   
.. index::
   single: field;nationality
   
.. _dsbe.contacts.Person.nationality:

Field **Person.nationality**
============================





Type: ForeignKey

   
.. index::
   single: field;card_number
   
.. _dsbe.contacts.Person.card_number:

Field **Person.card_number**
============================





Type: CharField

   
.. index::
   single: field;card_valid_from
   
.. _dsbe.contacts.Person.card_valid_from:

Field **Person.card_valid_from**
================================





Type: DateField

   
.. index::
   single: field;card_valid_until
   
.. _dsbe.contacts.Person.card_valid_until:

Field **Person.card_valid_until**
=================================





Type: DateField

   
.. index::
   single: field;card_type
   
.. _dsbe.contacts.Person.card_type:

Field **Person.card_type**
==========================





Type: CharField

   
.. index::
   single: field;card_issuer
   
.. _dsbe.contacts.Person.card_issuer:

Field **Person.card_issuer**
============================





Type: CharField

   
.. index::
   single: field;noble_condition
   
.. _dsbe.contacts.Person.noble_condition:

Field **Person.noble_condition**
================================





Type: CharField

   
.. index::
   single: field;residence_type
   
.. _dsbe.contacts.Person.residence_type:

Field **Person.residence_type**
===============================





Type: SmallIntegerField

   
.. index::
   single: field;in_belgium_since
   
.. _dsbe.contacts.Person.in_belgium_since:

Field **Person.in_belgium_since**
=================================





Type: DateField

   
.. index::
   single: field;unemployed_since
   
.. _dsbe.contacts.Person.unemployed_since:

Field **Person.unemployed_since**
=================================





Type: DateField

   
.. index::
   single: field;needs_residence_permit
   
.. _dsbe.contacts.Person.needs_residence_permit:

Field **Person.needs_residence_permit**
=======================================





Type: BooleanField

   
.. index::
   single: field;needs_work_permit
   
.. _dsbe.contacts.Person.needs_work_permit:

Field **Person.needs_work_permit**
==================================





Type: BooleanField

   
.. index::
   single: field;work_permit_suspended_until
   
.. _dsbe.contacts.Person.work_permit_suspended_until:

Field **Person.work_permit_suspended_until**
============================================





Type: DateField

   
.. index::
   single: field;aid_type
   
.. _dsbe.contacts.Person.aid_type:

Field **Person.aid_type**
=========================





Type: ForeignKey

   
.. index::
   single: field;income_ag
   
.. _dsbe.contacts.Person.income_ag:

Field **Person.income_ag**
==========================





Type: BooleanField

   
.. index::
   single: field;income_wg
   
.. _dsbe.contacts.Person.income_wg:

Field **Person.income_wg**
==========================





Type: BooleanField

   
.. index::
   single: field;income_kg
   
.. _dsbe.contacts.Person.income_kg:

Field **Person.income_kg**
==========================





Type: BooleanField

   
.. index::
   single: field;income_rente
   
.. _dsbe.contacts.Person.income_rente:

Field **Person.income_rente**
=============================





Type: BooleanField

   
.. index::
   single: field;income_misc
   
.. _dsbe.contacts.Person.income_misc:

Field **Person.income_misc**
============================





Type: BooleanField

   
.. index::
   single: field;is_seeking
   
.. _dsbe.contacts.Person.is_seeking:

Field **Person.is_seeking**
===========================





Type: BooleanField

   
.. index::
   single: field;unavailable_until
   
.. _dsbe.contacts.Person.unavailable_until:

Field **Person.unavailable_until**
==================================





Type: DateField

   
.. index::
   single: field;unavailable_why
   
.. _dsbe.contacts.Person.unavailable_why:

Field **Person.unavailable_why**
================================





Type: CharField

   
.. index::
   single: field;native_language
   
.. _dsbe.contacts.Person.native_language:

Field **Person.native_language**
================================





Type: ForeignKey

   
.. index::
   single: field;obstacles
   
.. _dsbe.contacts.Person.obstacles:

Field **Person.obstacles**
==========================





Type: TextField

   
.. index::
   single: field;skills
   
.. _dsbe.contacts.Person.skills:

Field **Person.skills**
=======================





Type: TextField

   
.. index::
   single: field;job_agents
   
.. _dsbe.contacts.Person.job_agents:

Field **Person.job_agents**
===========================





Type: CharField

   
.. index::
   single: field;job_office_contact
   
.. _dsbe.contacts.Person.job_office_contact:

Field **Person.job_office_contact**
===================================





Type: ForeignKey

   


.. index::
   pair: model; Company

.. _dsbe.contacts.Company:

-----------------
Model **Company**
-----------------




Implements :class:`contacts.Company`.

Inner class Meta is necessary because of :doc:`/tickets/14`.

  
============= ============= ============================
name          type          verbose name                
============= ============= ============================
name          CharField     Name                        
addr1         CharField     Address line before street  
street        CharField     Street (Straße,Rue)         
street_no     CharField     No. (Nr.,N°)                
street_box    CharField     Box (boîte)                 
addr2         CharField     Address line after street   
country       ForeignKey    Country (Land)              
city          ForeignKey    City (Stadt)                
zip_code      CharField     Zip code (Postleitzahl)     
region        CharField     Region                      
language      LanguageField Language (Sprache)          
email         EmailField    E-Mail                      
url           URLField      URL                         
phone         CharField     Phone (Telefon)             
gsm           CharField     GSM                         
fax           CharField     Fax                         
remarks       TextField     Remarks (Bemerkungen)       
vat_id        CharField     VAT id (MWSt.-Nr.)          
type          ForeignKey    Company type (Firmenart)    
id            AutoField     Partner # (Partnernummer)   
is_active     BooleanField  is active (aktiv)           
activity      ForeignKey    Activity (Beruf)            
bank_account1 CharField     Bank account 1 (Bankkonto 1)
bank_account2 CharField     Bank account 2 (Bankkonto 2)
prefix        CharField     prefix                      
hourly_rate   PriceField    hourly rate (Stundensatz)   
============= ============= ============================

    
Defined in :srcref:`/lino/sites/dsbe/models.py`

.. index::
   single: field;name
   
.. _dsbe.contacts.Company.name:

Field **Company.name**
======================





Type: CharField

   
.. index::
   single: field;addr1
   
.. _dsbe.contacts.Company.addr1:

Field **Company.addr1**
=======================



Address line before street

Type: CharField

   
.. index::
   single: field;street
   
.. _dsbe.contacts.Company.street:

Field **Company.street**
========================



Name of street. Without house number.

Type: CharField

   
.. index::
   single: field;street_no
   
.. _dsbe.contacts.Company.street_no:

Field **Company.street_no**
===========================



House number

Type: CharField

   
.. index::
   single: field;street_box
   
.. _dsbe.contacts.Company.street_box:

Field **Company.street_box**
============================



Text to print after :attr:`steet_no` on the same line

Type: CharField

   
.. index::
   single: field;addr2
   
.. _dsbe.contacts.Company.addr2:

Field **Company.addr2**
=======================



Address line to print below street line

Type: CharField

   
.. index::
   single: field;country
   
.. _dsbe.contacts.Company.country:

Field **Company.country**
=========================



The country where this contact is located.

Type: ForeignKey

   
.. index::
   single: field;city
   
.. _dsbe.contacts.Company.city:

Field **Company.city**
======================




        The city where this contact is located.
        The list of choices for this field is context-sensitive
        and depends on the :attr:`country`.
        

Type: ForeignKey

   
.. index::
   single: field;zip_code
   
.. _dsbe.contacts.Company.zip_code:

Field **Company.zip_code**
==========================





Type: CharField

   
.. index::
   single: field;region
   
.. _dsbe.contacts.Company.region:

Field **Company.region**
========================





Type: CharField

   
.. index::
   single: field;language
   
.. _dsbe.contacts.Company.language:

Field **Company.language**
==========================





Type: LanguageField

   
.. index::
   single: field;email
   
.. _dsbe.contacts.Company.email:

Field **Company.email**
=======================





Type: EmailField

   
.. index::
   single: field;url
   
.. _dsbe.contacts.Company.url:

Field **Company.url**
=====================





Type: URLField

   
.. index::
   single: field;phone
   
.. _dsbe.contacts.Company.phone:

Field **Company.phone**
=======================





Type: CharField

   
.. index::
   single: field;gsm
   
.. _dsbe.contacts.Company.gsm:

Field **Company.gsm**
=====================





Type: CharField

   
.. index::
   single: field;fax
   
.. _dsbe.contacts.Company.fax:

Field **Company.fax**
=====================





Type: CharField

   
.. index::
   single: field;remarks
   
.. _dsbe.contacts.Company.remarks:

Field **Company.remarks**
=========================





Type: TextField

   
.. index::
   single: field;vat_id
   
.. _dsbe.contacts.Company.vat_id:

Field **Company.vat_id**
========================





Type: CharField

   
.. index::
   single: field;type
   
.. _dsbe.contacts.Company.type:

Field **Company.type**
======================





Type: ForeignKey

   
.. index::
   single: field;id
   
.. _dsbe.contacts.Company.id:

Field **Company.id**
====================





Type: AutoField

   
.. index::
   single: field;is_active
   
.. _dsbe.contacts.Company.is_active:

Field **Company.is_active**
===========================





Type: BooleanField

   
.. index::
   single: field;activity
   
.. _dsbe.contacts.Company.activity:

Field **Company.activity**
==========================





Type: ForeignKey

   
.. index::
   single: field;bank_account1
   
.. _dsbe.contacts.Company.bank_account1:

Field **Company.bank_account1**
===============================





Type: CharField

   
.. index::
   single: field;bank_account2
   
.. _dsbe.contacts.Company.bank_account2:

Field **Company.bank_account2**
===============================





Type: CharField

   
.. index::
   single: field;prefix
   
.. _dsbe.contacts.Company.prefix:

Field **Company.prefix**
========================





Type: CharField

   
.. index::
   single: field;hourly_rate
   
.. _dsbe.contacts.Company.hourly_rate:

Field **Company.hourly_rate**
=============================





Type: PriceField

   


