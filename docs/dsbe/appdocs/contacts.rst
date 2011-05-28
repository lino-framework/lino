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

.. _std.contacts.CompanyType:

---------------------
Model **CompanyType**
---------------------




Represents a possible choice for the :class:`Company`.type
field.
Implemented by 
:ref:`dsbe.contacts.CompanyType`
:ref:`igen.contacts.CompanyType`

  
============= ============== ===========================================
name          type           verbose name                               
============= ============== ===========================================
id            AutoField      ID                                         
name          BabelCharField Designation (Beschreibung,Désignation)     
abbr          BabelCharField Abbreviation (Abkürzung,Abbréviation)      
name_fr       CharField      Designation (fr)                           
name_nl       CharField      Designation (nl)                           
name_en       CharField      Designation (en)                           
abbr_fr       CharField      Abbreviation (fr)                          
abbr_nl       CharField      Abbreviation (nl)                          
abbr_en       CharField      Abbreviation (en)                          
contract_type ForeignKey     contract type (Vertragsart,type de contrat)
============= ============== ===========================================

    
Defined in :srcref:`/lino/modlib/contacts/models.py`

.. index::
   single: field;id
   
.. _std.contacts.CompanyType.id:

Field **CompanyType.id**
========================





Type: AutoField

   
.. index::
   single: field;name
   
.. _std.contacts.CompanyType.name:

Field **CompanyType.name**
==========================





Type: BabelCharField

   
.. index::
   single: field;abbr
   
.. _std.contacts.CompanyType.abbr:

Field **CompanyType.abbr**
==========================





Type: BabelCharField

   
.. index::
   single: field;name_fr
   
.. _std.contacts.CompanyType.name_fr:

Field **CompanyType.name_fr**
=============================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _std.contacts.CompanyType.name_nl:

Field **CompanyType.name_nl**
=============================





Type: CharField

   
.. index::
   single: field;name_en
   
.. _std.contacts.CompanyType.name_en:

Field **CompanyType.name_en**
=============================





Type: CharField

   
.. index::
   single: field;abbr_fr
   
.. _std.contacts.CompanyType.abbr_fr:

Field **CompanyType.abbr_fr**
=============================





Type: CharField

   
.. index::
   single: field;abbr_nl
   
.. _std.contacts.CompanyType.abbr_nl:

Field **CompanyType.abbr_nl**
=============================





Type: CharField

   
.. index::
   single: field;abbr_en
   
.. _std.contacts.CompanyType.abbr_en:

Field **CompanyType.abbr_en**
=============================





Type: CharField

   
.. index::
   single: field;contract_type
   
.. _std.contacts.CompanyType.contract_type:

Field **CompanyType.contract_type**
===================================





Type: ForeignKey

   


.. index::
   pair: model; ContactType

.. _std.contacts.ContactType:

---------------------
Model **ContactType**
---------------------




Implements the :class:`contacts.ContactType` convention.

  
======= ============== ======================================
name    type           verbose name                          
======= ============== ======================================
id      AutoField      ID                                    
name    BabelCharField Designation (Beschreibung,Désignation)
name_fr CharField      Designation (fr)                      
name_nl CharField      Designation (nl)                      
name_en CharField      Designation (en)                      
======= ============== ======================================

    
Defined in :srcref:`/lino/modlib/contacts/models.py`

.. index::
   single: field;id
   
.. _std.contacts.ContactType.id:

Field **ContactType.id**
========================





Type: AutoField

   
.. index::
   single: field;name
   
.. _std.contacts.ContactType.name:

Field **ContactType.name**
==========================





Type: BabelCharField

   
.. index::
   single: field;name_fr
   
.. _std.contacts.ContactType.name_fr:

Field **ContactType.name_fr**
=============================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _std.contacts.ContactType.name_nl:

Field **ContactType.name_nl**
=============================





Type: CharField

   
.. index::
   single: field;name_en
   
.. _std.contacts.ContactType.name_en:

Field **ContactType.name_en**
=============================





Type: CharField

   


.. index::
   pair: model; Contact

.. _std.contacts.Contact:

-----------------
Model **Contact**
-----------------




Represents a :class:`Person` having a (more or less known) 
role in a :class:`Company`.

  
======= ========== =========================================
name    type       verbose name                             
======= ========== =========================================
id      AutoField  ID                                       
person  ForeignKey person (Person,personne)                 
company ForeignKey company (Firma,Société)                  
type    ForeignKey contact type (Kontaktart,type de contact)
======= ========== =========================================

    
Defined in :srcref:`/lino/modlib/contacts/models.py`

.. index::
   single: field;id
   
.. _std.contacts.Contact.id:

Field **Contact.id**
====================





Type: AutoField

   
.. index::
   single: field;person
   
.. _std.contacts.Contact.person:

Field **Contact.person**
========================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _std.contacts.Contact.company:

Field **Contact.company**
=========================





Type: ForeignKey

   
.. index::
   single: field;type
   
.. _std.contacts.Contact.type:

Field **Contact.type**
======================





Type: ForeignKey

   


.. index::
   pair: model; Person

.. _std.contacts.Person:

----------------
Model **Person**
----------------




Represents a physical person.


  
=========================== ================= ====================================================================================
name                        type              verbose name                                                                        
=========================== ================= ====================================================================================
country                     ForeignKey        Country (Land,Pays)                                                                 
city                        ForeignKey        City                                                                                
name                        CharField         Name (Nom)                                                                          
addr1                       CharField         Address line before street (Adresszeile vor Straße,Ligne avant le nom de rue)       
street                      CharField         Street (Straße,Rue)                                                                 
street_no                   CharField         No. (Nr.,N°)                                                                        
street_box                  CharField         Box (boîte)                                                                         
addr2                       CharField         Address line after street (Adresszeile nach Straße,Ligne après le nom de rue)       
zip_code                    CharField         Zip code (Postleitzahl,Code postal)                                                 
region                      CharField         Region (Région)                                                                     
language                    LanguageField     Language (Sprache,Langue)                                                           
email                       EmailField        E-Mail (E-mail)                                                                     
url                         URLField          URL                                                                                 
phone                       CharField         Phone (Telefon,Téléphone)                                                           
gsm                         CharField         GSM                                                                                 
fax                         CharField         Fax                                                                                 
remarks                     TextField         Remarks (Bemerkungen,Remarques)                                                     
first_name                  CharField         First name (Vorname,Prénom)                                                         
last_name                   CharField         Last name (Familienname,Nom de famille)                                             
title                       CharField         Title (Anrede,Intitulé)                                                             
id                          AutoField         Partner # (Partnernummer,Partenaire #)                                              
is_active                   BooleanField      is active (aktiv,est actif)                                                         
activity                    ForeignKey        Activity (Beruf,Activité)                                                           
bank_account1               CharField         Bank account 1 (Bankkonto 1,Compte en banque 1)                                     
bank_account2               CharField         Bank account 2 (Bankkonto 2,Compte en banque 2)                                     
remarks2                    TextField         Remarks (Social Office) (Bemerkungen (Sozialsekretariat),Remarque (Bureau Social))  
gesdos_id                   CharField         Gesdos ID (Gesdos-Nr)                                                               
is_cpas                     BooleanField      receives social help (Sozialhilfeempfänger,reçoit de l'aide sociale)                
is_senior                   BooleanField      is senior (Altenheim)                                                               
group                       ForeignKey        Group (Gruppe,Groupe)                                                               
coached_from                DateField         Coached from (Begleitet seit)                                                       
coached_until               DateField         until (bis,jusque)                                                                  
coach1                      ForeignKey        Coach 1 (Begleiter 1)                                                               
coach2                      ForeignKey        Coach 2 (Begleiter 2)                                                               
sex                         CharField         Sex (Geschlecht,Sexe)                                                               
birth_date                  DateField         Birth date (Geburtsdatum,Date de naissance)                                         
birth_date_circa            BooleanField      not exact (circa,inexact)                                                           
birth_place                 CharField         Birth place (Geburtsort,Lieu de naissance)                                          
birth_country               ForeignKey        Birth country (Geburtsland,Pays de naissance)                                       
civil_state                 CharField         Civil state (Zivilstand,Etat civil)                                                 
national_id                 CharField         National ID (NR-Nummer,Numéro d'identitification du registre national)              
health_insurance            ForeignKey        Health insurance (Krankenkasse,Assurance santé)                                     
pharmacy                    ForeignKey        Pharmacy (Apotheke,Pharmacie)                                                       
nationality                 ForeignKey        Nationality (Staatsangehörigkeit,Nationalité)                                       
card_number                 CharField         eID card number (eID-Kartennummer,Numéro de carte eID)                              
card_valid_from             DateField         ID card valid from (ID-Karte gültig von,Carte d'identité valable depuis)            
card_valid_until            DateField         until (bis,jusque)                                                                  
card_type                   CharField         eID card type (eID-Kartenart)                                                       
card_issuer                 CharField         eID card issuer (eID-Karte ausgestellt durch,carte eID provenant de)                
noble_condition             CharField         noble condition (Adelstitel)                                                        
residence_type              SmallIntegerField Residence type (Eintragen,Type de séjour)                                           
in_belgium_since            DateField         Lives in Belgium since (Lebt in Belgien seit,Habite en Belgique depuis)             
unemployed_since            DateField         Seeking work since (eingetragen seit,Cherche du travail depuis)                     
needs_residence_permit      BooleanField      Needs residence permit (Braucht Aufenthaltserlaubnis,A besoin d'un permis de séjour)
needs_work_permit           BooleanField      Needs work permit (Braucht Arb.Erl.,A besoin d'un permis de travail)                
work_permit_suspended_until DateField         suspended until (Wartezeit bis,suspendu jusque)                                     
aid_type                    ForeignKey        aid type (Sozialhilfeart)                                                           
income_ag                   BooleanField      Arbeitslosengeld (Indemnités de chômage)                                            
income_wg                   BooleanField      Wartegeld (Indemnité d'attente)                                                     
income_kg                   BooleanField      Krankengeld (Indemnité de maladie)                                                  
income_rente                BooleanField      Rente                                                                               
income_misc                 BooleanField      Andere (Anutre)                                                                     
is_seeking                  BooleanField      is seeking work (Arbeit suchend,cherche du travail)                                 
unavailable_until           DateField         Unavailable until (Nicht verfügbar bis,Indidponible jusque)                         
unavailable_why             CharField         reason (Grund,raison)                                                               
native_language             ForeignKey        Native language (Muttersprache)                                                     
obstacles                   TextField         Obstacles (Hindernisse)                                                             
skills                      TextField         Other skills (Sonstige Fähikeiten,Autres talents)                                   
job_agents                  CharField         Job agents (Interim-Agenturen)                                                      
job_office_contact          ForeignKey        Contact person at local job office (Kontaktperson ADG,Personne de contacte ALE ?)   
=========================== ================= ====================================================================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

.. index::
   single: field;country
   
.. _std.contacts.Person.country:

Field **Person.country**
========================





Type: ForeignKey

   
.. index::
   single: field;city
   
.. _std.contacts.Person.city:

Field **Person.city**
=====================





Type: ForeignKey

   
.. index::
   single: field;name
   
.. _std.contacts.Person.name:

Field **Person.name**
=====================





Type: CharField

   
.. index::
   single: field;addr1
   
.. _std.contacts.Person.addr1:

Field **Person.addr1**
======================



Address line before street

Type: CharField

   
.. index::
   single: field;street
   
.. _std.contacts.Person.street:

Field **Person.street**
=======================



Name of street. Without house number.

Type: CharField

   
.. index::
   single: field;street_no
   
.. _std.contacts.Person.street_no:

Field **Person.street_no**
==========================



House number

Type: CharField

   
.. index::
   single: field;street_box
   
.. _std.contacts.Person.street_box:

Field **Person.street_box**
===========================



Text to print after :attr:`steet_no` on the same line

Type: CharField

   
.. index::
   single: field;addr2
   
.. _std.contacts.Person.addr2:

Field **Person.addr2**
======================



Address line to print below street line

Type: CharField

   
.. index::
   single: field;zip_code
   
.. _std.contacts.Person.zip_code:

Field **Person.zip_code**
=========================





Type: CharField

   
.. index::
   single: field;region
   
.. _std.contacts.Person.region:

Field **Person.region**
=======================





Type: CharField

   
.. index::
   single: field;language
   
.. _std.contacts.Person.language:

Field **Person.language**
=========================





Type: LanguageField

   
.. index::
   single: field;email
   
.. _std.contacts.Person.email:

Field **Person.email**
======================





Type: EmailField

   
.. index::
   single: field;url
   
.. _std.contacts.Person.url:

Field **Person.url**
====================





Type: URLField

   
.. index::
   single: field;phone
   
.. _std.contacts.Person.phone:

Field **Person.phone**
======================





Type: CharField

   
.. index::
   single: field;gsm
   
.. _std.contacts.Person.gsm:

Field **Person.gsm**
====================





Type: CharField

   
.. index::
   single: field;fax
   
.. _std.contacts.Person.fax:

Field **Person.fax**
====================





Type: CharField

   
.. index::
   single: field;remarks
   
.. _std.contacts.Person.remarks:

Field **Person.remarks**
========================





Type: TextField

   
.. index::
   single: field;first_name
   
.. _std.contacts.Person.first_name:

Field **Person.first_name**
===========================





Type: CharField

   
.. index::
   single: field;last_name
   
.. _std.contacts.Person.last_name:

Field **Person.last_name**
==========================





Type: CharField

   
.. index::
   single: field;title
   
.. _std.contacts.Person.title:

Field **Person.title**
======================





Type: CharField

   
.. index::
   single: field;id
   
.. _std.contacts.Person.id:

Field **Person.id**
===================





Type: AutoField

   
.. index::
   single: field;is_active
   
.. _std.contacts.Person.is_active:

Field **Person.is_active**
==========================





Type: BooleanField

   
.. index::
   single: field;activity
   
.. _std.contacts.Person.activity:

Field **Person.activity**
=========================





Type: ForeignKey

   
.. index::
   single: field;bank_account1
   
.. _std.contacts.Person.bank_account1:

Field **Person.bank_account1**
==============================





Type: CharField

   
.. index::
   single: field;bank_account2
   
.. _std.contacts.Person.bank_account2:

Field **Person.bank_account2**
==============================





Type: CharField

   
.. index::
   single: field;remarks2
   
.. _std.contacts.Person.remarks2:

Field **Person.remarks2**
=========================





Type: TextField

   
.. index::
   single: field;gesdos_id
   
.. _std.contacts.Person.gesdos_id:

Field **Person.gesdos_id**
==========================





Type: CharField

   
.. index::
   single: field;is_cpas
   
.. _std.contacts.Person.is_cpas:

Field **Person.is_cpas**
========================





Type: BooleanField

   
.. index::
   single: field;is_senior
   
.. _std.contacts.Person.is_senior:

Field **Person.is_senior**
==========================





Type: BooleanField

   
.. index::
   single: field;group
   
.. _std.contacts.Person.group:

Field **Person.group**
======================





Type: ForeignKey

   
.. index::
   single: field;coached_from
   
.. _std.contacts.Person.coached_from:

Field **Person.coached_from**
=============================





Type: DateField

   
.. index::
   single: field;coached_until
   
.. _std.contacts.Person.coached_until:

Field **Person.coached_until**
==============================





Type: DateField

   
.. index::
   single: field;coach1
   
.. _std.contacts.Person.coach1:

Field **Person.coach1**
=======================





Type: ForeignKey

   
.. index::
   single: field;coach2
   
.. _std.contacts.Person.coach2:

Field **Person.coach2**
=======================





Type: ForeignKey

   
.. index::
   single: field;sex
   
.. _std.contacts.Person.sex:

Field **Person.sex**
====================





Type: CharField

   
.. index::
   single: field;birth_date
   
.. _std.contacts.Person.birth_date:

Field **Person.birth_date**
===========================





Type: DateField

   
.. index::
   single: field;birth_date_circa
   
.. _std.contacts.Person.birth_date_circa:

Field **Person.birth_date_circa**
=================================





Type: BooleanField

   
.. index::
   single: field;birth_place
   
.. _std.contacts.Person.birth_place:

Field **Person.birth_place**
============================





Type: CharField

   
.. index::
   single: field;birth_country
   
.. _std.contacts.Person.birth_country:

Field **Person.birth_country**
==============================





Type: ForeignKey

   
.. index::
   single: field;civil_state
   
.. _std.contacts.Person.civil_state:

Field **Person.civil_state**
============================





Type: CharField

   
.. index::
   single: field;national_id
   
.. _std.contacts.Person.national_id:

Field **Person.national_id**
============================





Type: CharField

   
.. index::
   single: field;health_insurance
   
.. _std.contacts.Person.health_insurance:

Field **Person.health_insurance**
=================================





Type: ForeignKey

   
.. index::
   single: field;pharmacy
   
.. _std.contacts.Person.pharmacy:

Field **Person.pharmacy**
=========================





Type: ForeignKey

   
.. index::
   single: field;nationality
   
.. _std.contacts.Person.nationality:

Field **Person.nationality**
============================





Type: ForeignKey

   
.. index::
   single: field;card_number
   
.. _std.contacts.Person.card_number:

Field **Person.card_number**
============================





Type: CharField

   
.. index::
   single: field;card_valid_from
   
.. _std.contacts.Person.card_valid_from:

Field **Person.card_valid_from**
================================





Type: DateField

   
.. index::
   single: field;card_valid_until
   
.. _std.contacts.Person.card_valid_until:

Field **Person.card_valid_until**
=================================





Type: DateField

   
.. index::
   single: field;card_type
   
.. _std.contacts.Person.card_type:

Field **Person.card_type**
==========================





Type: CharField

   
.. index::
   single: field;card_issuer
   
.. _std.contacts.Person.card_issuer:

Field **Person.card_issuer**
============================





Type: CharField

   
.. index::
   single: field;noble_condition
   
.. _std.contacts.Person.noble_condition:

Field **Person.noble_condition**
================================





Type: CharField

   
.. index::
   single: field;residence_type
   
.. _std.contacts.Person.residence_type:

Field **Person.residence_type**
===============================





Type: SmallIntegerField

   
.. index::
   single: field;in_belgium_since
   
.. _std.contacts.Person.in_belgium_since:

Field **Person.in_belgium_since**
=================================





Type: DateField

   
.. index::
   single: field;unemployed_since
   
.. _std.contacts.Person.unemployed_since:

Field **Person.unemployed_since**
=================================





Type: DateField

   
.. index::
   single: field;needs_residence_permit
   
.. _std.contacts.Person.needs_residence_permit:

Field **Person.needs_residence_permit**
=======================================





Type: BooleanField

   
.. index::
   single: field;needs_work_permit
   
.. _std.contacts.Person.needs_work_permit:

Field **Person.needs_work_permit**
==================================





Type: BooleanField

   
.. index::
   single: field;work_permit_suspended_until
   
.. _std.contacts.Person.work_permit_suspended_until:

Field **Person.work_permit_suspended_until**
============================================





Type: DateField

   
.. index::
   single: field;aid_type
   
.. _std.contacts.Person.aid_type:

Field **Person.aid_type**
=========================





Type: ForeignKey

   
.. index::
   single: field;income_ag
   
.. _std.contacts.Person.income_ag:

Field **Person.income_ag**
==========================





Type: BooleanField

   
.. index::
   single: field;income_wg
   
.. _std.contacts.Person.income_wg:

Field **Person.income_wg**
==========================





Type: BooleanField

   
.. index::
   single: field;income_kg
   
.. _std.contacts.Person.income_kg:

Field **Person.income_kg**
==========================





Type: BooleanField

   
.. index::
   single: field;income_rente
   
.. _std.contacts.Person.income_rente:

Field **Person.income_rente**
=============================





Type: BooleanField

   
.. index::
   single: field;income_misc
   
.. _std.contacts.Person.income_misc:

Field **Person.income_misc**
============================





Type: BooleanField

   
.. index::
   single: field;is_seeking
   
.. _std.contacts.Person.is_seeking:

Field **Person.is_seeking**
===========================





Type: BooleanField

   
.. index::
   single: field;unavailable_until
   
.. _std.contacts.Person.unavailable_until:

Field **Person.unavailable_until**
==================================





Type: DateField

   
.. index::
   single: field;unavailable_why
   
.. _std.contacts.Person.unavailable_why:

Field **Person.unavailable_why**
================================





Type: CharField

   
.. index::
   single: field;native_language
   
.. _std.contacts.Person.native_language:

Field **Person.native_language**
================================





Type: ForeignKey

   
.. index::
   single: field;obstacles
   
.. _std.contacts.Person.obstacles:

Field **Person.obstacles**
==========================





Type: TextField

   
.. index::
   single: field;skills
   
.. _std.contacts.Person.skills:

Field **Person.skills**
=======================





Type: TextField

   
.. index::
   single: field;job_agents
   
.. _std.contacts.Person.job_agents:

Field **Person.job_agents**
===========================





Type: CharField

   
.. index::
   single: field;job_office_contact
   
.. _std.contacts.Person.job_office_contact:

Field **Person.job_office_contact**
===================================





Type: ForeignKey

   


.. index::
   pair: model; Company

.. _std.contacts.Company:

-----------------
Model **Company**
-----------------




Implements :class:`contacts.Company`.

Inner class Meta is necessary because of :doc:`/tickets/14`.

  
============= ============= =============================================================================
name          type          verbose name                                                                 
============= ============= =============================================================================
country       ForeignKey    Country (Land,Pays)                                                          
city          ForeignKey    City                                                                         
name          CharField     Name (Nom)                                                                   
addr1         CharField     Address line before street (Adresszeile vor Straße,Ligne avant le nom de rue)
street        CharField     Street (Straße,Rue)                                                          
street_no     CharField     No. (Nr.,N°)                                                                 
street_box    CharField     Box (boîte)                                                                  
addr2         CharField     Address line after street (Adresszeile nach Straße,Ligne après le nom de rue)
zip_code      CharField     Zip code (Postleitzahl,Code postal)                                          
region        CharField     Region (Région)                                                              
language      LanguageField Language (Sprache,Langue)                                                    
email         EmailField    E-Mail (E-mail)                                                              
url           URLField      URL                                                                          
phone         CharField     Phone (Telefon,Téléphone)                                                    
gsm           CharField     GSM                                                                          
fax           CharField     Fax                                                                          
remarks       TextField     Remarks (Bemerkungen,Remarques)                                              
vat_id        CharField     VAT id (MWSt.-Nr.,N° de TVA)                                                 
type          ForeignKey    Company type (Firmenart)                                                     
id            AutoField     Partner # (Partnernummer,Partenaire #)                                       
is_active     BooleanField  is active (aktiv,est actif)                                                  
activity      ForeignKey    Activity (Beruf,Activité)                                                    
bank_account1 CharField     Bank account 1 (Bankkonto 1,Compte en banque 1)                              
bank_account2 CharField     Bank account 2 (Bankkonto 2,Compte en banque 2)                              
prefix        CharField     prefix                                                                       
hourly_rate   PriceField    hourly rate (Stundensatz,coûr horaire)                                       
============= ============= =============================================================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

.. index::
   single: field;country
   
.. _std.contacts.Company.country:

Field **Company.country**
=========================





Type: ForeignKey

   
.. index::
   single: field;city
   
.. _std.contacts.Company.city:

Field **Company.city**
======================





Type: ForeignKey

   
.. index::
   single: field;name
   
.. _std.contacts.Company.name:

Field **Company.name**
======================





Type: CharField

   
.. index::
   single: field;addr1
   
.. _std.contacts.Company.addr1:

Field **Company.addr1**
=======================



Address line before street

Type: CharField

   
.. index::
   single: field;street
   
.. _std.contacts.Company.street:

Field **Company.street**
========================



Name of street. Without house number.

Type: CharField

   
.. index::
   single: field;street_no
   
.. _std.contacts.Company.street_no:

Field **Company.street_no**
===========================



House number

Type: CharField

   
.. index::
   single: field;street_box
   
.. _std.contacts.Company.street_box:

Field **Company.street_box**
============================



Text to print after :attr:`steet_no` on the same line

Type: CharField

   
.. index::
   single: field;addr2
   
.. _std.contacts.Company.addr2:

Field **Company.addr2**
=======================



Address line to print below street line

Type: CharField

   
.. index::
   single: field;zip_code
   
.. _std.contacts.Company.zip_code:

Field **Company.zip_code**
==========================





Type: CharField

   
.. index::
   single: field;region
   
.. _std.contacts.Company.region:

Field **Company.region**
========================





Type: CharField

   
.. index::
   single: field;language
   
.. _std.contacts.Company.language:

Field **Company.language**
==========================





Type: LanguageField

   
.. index::
   single: field;email
   
.. _std.contacts.Company.email:

Field **Company.email**
=======================





Type: EmailField

   
.. index::
   single: field;url
   
.. _std.contacts.Company.url:

Field **Company.url**
=====================





Type: URLField

   
.. index::
   single: field;phone
   
.. _std.contacts.Company.phone:

Field **Company.phone**
=======================





Type: CharField

   
.. index::
   single: field;gsm
   
.. _std.contacts.Company.gsm:

Field **Company.gsm**
=====================





Type: CharField

   
.. index::
   single: field;fax
   
.. _std.contacts.Company.fax:

Field **Company.fax**
=====================





Type: CharField

   
.. index::
   single: field;remarks
   
.. _std.contacts.Company.remarks:

Field **Company.remarks**
=========================





Type: TextField

   
.. index::
   single: field;vat_id
   
.. _std.contacts.Company.vat_id:

Field **Company.vat_id**
========================





Type: CharField

   
.. index::
   single: field;type
   
.. _std.contacts.Company.type:

Field **Company.type**
======================





Type: ForeignKey

   
.. index::
   single: field;id
   
.. _std.contacts.Company.id:

Field **Company.id**
====================





Type: AutoField

   
.. index::
   single: field;is_active
   
.. _std.contacts.Company.is_active:

Field **Company.is_active**
===========================





Type: BooleanField

   
.. index::
   single: field;activity
   
.. _std.contacts.Company.activity:

Field **Company.activity**
==========================





Type: ForeignKey

   
.. index::
   single: field;bank_account1
   
.. _std.contacts.Company.bank_account1:

Field **Company.bank_account1**
===============================





Type: CharField

   
.. index::
   single: field;bank_account2
   
.. _std.contacts.Company.bank_account2:

Field **Company.bank_account2**
===============================





Type: CharField

   
.. index::
   single: field;prefix
   
.. _std.contacts.Company.prefix:

Field **Company.prefix**
========================





Type: CharField

   
.. index::
   single: field;hourly_rate
   
.. _std.contacts.Company.hourly_rate:

Field **Company.hourly_rate**
=============================





Type: PriceField

   


