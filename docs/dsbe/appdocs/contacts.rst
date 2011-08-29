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


  
============= ============= =============================================================================
name          type          verbose name                                                                 
============= ============= =============================================================================
id            AutoField     ID                                                                           
country       ForeignKey    Country (Land,Pays)                                                          
city          ForeignKey    City (Stadt)                                                                 
name          CharField     Name (Nom)                                                                   
addr1         CharField     Address line before street (Adresszeile vor Straße,Ligne avant le nom de rue)
street_prefix CharField     Street prefix (Präfix Straße,Préfixe rue)                                    
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
============= ============= =============================================================================

    
Defined in :srcref:`/lino/modlib/contacts/models.py`

Referenced from
`lino.mails.Recipient.contact`_, `lino.jobs.JobProvider.contact_ptr`_, `lino.users.User.contact_ptr`_, `lino.contacts.Role.parent`_, `lino.contacts.Role.child`_, `lino.contacts.Person.contact_ptr`_, `lino.contacts.Company.contact_ptr`_, `lino.dsbe.CourseProvider.contact_ptr`_, `lino.cal.Guest.contact`_



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

  
======= ============== ======================================
name    type           verbose name                          
======= ============== ======================================
id      AutoField      ID                                    
name    BabelCharField Designation (Beschreibung,Désignation)
abbr    BabelCharField Abbreviation (Abkürzung,Abbréviation) 
abbr_fr CharField      Abbreviation (fr)                     
abbr_nl CharField      Abbreviation (nl)                     
abbr_en CharField      Abbreviation (en)                     
name_fr CharField      Designation (fr)                      
name_nl CharField      Designation (nl)                      
name_en CharField      Designation (en)                      
======= ============== ======================================

    
Defined in :srcref:`/lino/modlib/contacts/models.py`

Referenced from
`lino.jobs.JobProvider.type`_, `lino.contacts.Company.type`_, `lino.dsbe.CourseProvider.type`_



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
   single: field;abbr_en
   
.. _lino.contacts.CompanyType.abbr_en:

Field **CompanyType.abbr_en**
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
   single: field;name_en
   
.. _lino.contacts.CompanyType.name_en:

Field **CompanyType.name_en**
=============================





Type: CharField

   


.. index::
   pair: model; RoleType

.. _lino.contacts.RoleType:

------------------
Model **RoleType**
------------------




Deserves more documentation.

  
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
   single: field;name_en
   
.. _lino.contacts.RoleType.name_en:

Field **RoleType.name_en**
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
`lino.jobs.Contract.contact`_, `lino.contacts.Person.job_office_contact`_



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




Represents a physical person.


  
=========================== ================= ====================================================================================
name                        type              verbose name                                                                        
=========================== ================= ====================================================================================
id                          AutoField         ID                                                                                  
country                     ForeignKey        Country (Land,Pays)                                                                 
city                        ForeignKey        City (Stadt)                                                                        
name                        CharField         Name (Nom)                                                                          
addr1                       CharField         Address line before street (Adresszeile vor Straße,Ligne avant le nom de rue)       
street_prefix               CharField         Street prefix (Präfix Straße,Préfixe rue)                                           
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
contact_ptr                 OneToOneField     Contact (Kontakt)                                                                   
birth_date                  DateField         Birth date (Geburtsdatum)                                                           
birth_date_circa            BooleanField      not exact (ungenau)                                                                 
first_name                  CharField         First name (Vorname,Prénom)                                                         
last_name                   CharField         Last name (Familienname,Nom de famille)                                             
title                       CharField         Title (Anrede,Allocution)                                                           
sex                         CharField         Sex (Geschlecht,Sexe)                                                               
is_active                   BooleanField      is active (aktiv,est actif)                                                         
activity                    ForeignKey        Activity (Beruf,Activité)                                                           
bank_account1               CharField         Bank account 1 (Bankkonto 1,Compte en banque 1)                                     
bank_account2               CharField         Bank account 2 (Bankkonto 2,Compte en banque 2)                                     
remarks2                    TextField         Remarks (Social Office) (Bemerkungen (Sozialsekretariat),Remarque (Bureau Social))  
gesdos_id                   CharField         Gesdos ID (Gesdos-Nr,N° GesDos)                                                     
is_cpas                     BooleanField      receives social help (Sozialhilfeempfänger,reçoit de l'aide sociale)                
is_senior                   BooleanField      is senior (Altenheim)                                                               
group                       ForeignKey        Integration phase (Integrationsphase,Phase d'intégration)                           
coached_from                DateField         Coached from (Begleitet seit,Début de l'accompagnement)                             
coached_until               DateField         until (bis,jusque)                                                                  
coach1                      ForeignKey        Coach 1 (Begleiter 1,Agent ISP)                                                     
coach2                      ForeignKey        Coach 2 (Begleiter 2,Agent SSP)                                                     
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
card_type                   CharField         eID card type (eID-Kartenart,Type de carte eID)                                     
card_issuer                 CharField         eID card issuer (eID-Karte ausgestellt durch,carte eID provenant de)                
noble_condition             CharField         noble condition (Adelstitel)                                                        
residence_type              SmallIntegerField Residence type (Eintragen,Type de séjour)                                           
in_belgium_since            DateField         Lives in Belgium since (Lebt in Belgien seit,Habite en Belgique depuis)             
unemployed_since            DateField         Seeking work since (eingetragen seit,Cherche du travail depuis)                     
needs_residence_permit      BooleanField      Needs residence permit (Braucht Aufenthaltserlaubnis,A besoin d'un permis de séjour)
needs_work_permit           BooleanField      Needs work permit (Braucht Arb.Erl.,A besoin d'un permis de travail)                
work_permit_suspended_until DateField         suspended until (Wartezeit bis,suspendu jusque)                                     
aid_type                    ForeignKey        aid type (Sozialhilfeart,Type d'aide sociale)                                       
income_ag                   BooleanField      unemployment benefit (Arbeitslosengeld)                                             
income_wg                   BooleanField      waiting pay (Wartegeld)                                                             
income_kg                   BooleanField      sickness benefit (Krankengeld)                                                      
income_rente                BooleanField      retirement pension (Rente)                                                          
income_misc                 BooleanField      other incomes (andere Einkommen)                                                    
is_seeking                  BooleanField      is seeking work (Arbeit suchend,cherche du travail)                                 
unavailable_until           DateField         Unavailable until (Nicht verfügbar bis,Indidponible jusque)                         
unavailable_why             CharField         reason (Grund,raison)                                                               
obstacles                   TextField         Obstacles (Hindernisse)                                                             
skills                      TextField         Other skills (Sonstige Fähikeiten,Autres talents)                                   
job_agents                  CharField         Job agents (Interim-Agenturen)                                                      
job_office_contact          ForeignKey        Contact person at local job office (Kontaktperson ADG,Personne de contacte ALE ?)   
=========================== ================= ====================================================================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from
`lino.jobs.Contract.person`_, `lino.jobs.JobRequest.person`_, `lino.links.Link.person`_, `lino.dsbe.Study.person`_, `lino.dsbe.LanguageKnowledge.person`_, `lino.dsbe.JobExperience.person`_, `lino.dsbe.Exclusion.person`_, `lino.dsbe.CourseRequest.person`_, `lino.notes.Note.person`_, `lino.cal.Event.project`_, `lino.cal.Task.project`_, `lino.thirds.Third.person`_, `lino.properties.PersonProperty.person`_



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
   single: field;is_active
   
.. _lino.contacts.Person.is_active:

Field **Person.is_active**
==========================





Type: BooleanField

   
.. index::
   single: field;activity
   
.. _lino.contacts.Person.activity:

Field **Person.activity**
=========================





Type: ForeignKey

   
.. index::
   single: field;bank_account1
   
.. _lino.contacts.Person.bank_account1:

Field **Person.bank_account1**
==============================





Type: CharField

   
.. index::
   single: field;bank_account2
   
.. _lino.contacts.Person.bank_account2:

Field **Person.bank_account2**
==============================





Type: CharField

   
.. index::
   single: field;remarks2
   
.. _lino.contacts.Person.remarks2:

Field **Person.remarks2**
=========================





Type: TextField

   
.. index::
   single: field;gesdos_id
   
.. _lino.contacts.Person.gesdos_id:

Field **Person.gesdos_id**
==========================





Type: CharField

   
.. index::
   single: field;is_cpas
   
.. _lino.contacts.Person.is_cpas:

Field **Person.is_cpas**
========================





Type: BooleanField

   
.. index::
   single: field;is_senior
   
.. _lino.contacts.Person.is_senior:

Field **Person.is_senior**
==========================





Type: BooleanField

   
.. index::
   single: field;group
   
.. _lino.contacts.Person.group:

Field **Person.group**
======================





Type: ForeignKey

   
.. index::
   single: field;coached_from
   
.. _lino.contacts.Person.coached_from:

Field **Person.coached_from**
=============================





Type: DateField

   
.. index::
   single: field;coached_until
   
.. _lino.contacts.Person.coached_until:

Field **Person.coached_until**
==============================





Type: DateField

   
.. index::
   single: field;coach1
   
.. _lino.contacts.Person.coach1:

Field **Person.coach1**
=======================





Type: ForeignKey

   
.. index::
   single: field;coach2
   
.. _lino.contacts.Person.coach2:

Field **Person.coach2**
=======================





Type: ForeignKey

   
.. index::
   single: field;birth_place
   
.. _lino.contacts.Person.birth_place:

Field **Person.birth_place**
============================





Type: CharField

   
.. index::
   single: field;birth_country
   
.. _lino.contacts.Person.birth_country:

Field **Person.birth_country**
==============================





Type: ForeignKey

   
.. index::
   single: field;civil_state
   
.. _lino.contacts.Person.civil_state:

Field **Person.civil_state**
============================





Type: CharField

   
.. index::
   single: field;national_id
   
.. _lino.contacts.Person.national_id:

Field **Person.national_id**
============================





Type: CharField

   
.. index::
   single: field;health_insurance
   
.. _lino.contacts.Person.health_insurance:

Field **Person.health_insurance**
=================================





Type: ForeignKey

   
.. index::
   single: field;pharmacy
   
.. _lino.contacts.Person.pharmacy:

Field **Person.pharmacy**
=========================





Type: ForeignKey

   
.. index::
   single: field;nationality
   
.. _lino.contacts.Person.nationality:

Field **Person.nationality**
============================





Type: ForeignKey

   
.. index::
   single: field;card_number
   
.. _lino.contacts.Person.card_number:

Field **Person.card_number**
============================





Type: CharField

   
.. index::
   single: field;card_valid_from
   
.. _lino.contacts.Person.card_valid_from:

Field **Person.card_valid_from**
================================





Type: DateField

   
.. index::
   single: field;card_valid_until
   
.. _lino.contacts.Person.card_valid_until:

Field **Person.card_valid_until**
=================================





Type: DateField

   
.. index::
   single: field;card_type
   
.. _lino.contacts.Person.card_type:

Field **Person.card_type**
==========================





Type: CharField

   
.. index::
   single: field;card_issuer
   
.. _lino.contacts.Person.card_issuer:

Field **Person.card_issuer**
============================





Type: CharField

   
.. index::
   single: field;noble_condition
   
.. _lino.contacts.Person.noble_condition:

Field **Person.noble_condition**
================================





Type: CharField

   
.. index::
   single: field;residence_type
   
.. _lino.contacts.Person.residence_type:

Field **Person.residence_type**
===============================





Type: SmallIntegerField

   
.. index::
   single: field;in_belgium_since
   
.. _lino.contacts.Person.in_belgium_since:

Field **Person.in_belgium_since**
=================================





Type: DateField

   
.. index::
   single: field;unemployed_since
   
.. _lino.contacts.Person.unemployed_since:

Field **Person.unemployed_since**
=================================





Type: DateField

   
.. index::
   single: field;needs_residence_permit
   
.. _lino.contacts.Person.needs_residence_permit:

Field **Person.needs_residence_permit**
=======================================





Type: BooleanField

   
.. index::
   single: field;needs_work_permit
   
.. _lino.contacts.Person.needs_work_permit:

Field **Person.needs_work_permit**
==================================





Type: BooleanField

   
.. index::
   single: field;work_permit_suspended_until
   
.. _lino.contacts.Person.work_permit_suspended_until:

Field **Person.work_permit_suspended_until**
============================================





Type: DateField

   
.. index::
   single: field;aid_type
   
.. _lino.contacts.Person.aid_type:

Field **Person.aid_type**
=========================





Type: ForeignKey

   
.. index::
   single: field;income_ag
   
.. _lino.contacts.Person.income_ag:

Field **Person.income_ag**
==========================





Type: BooleanField

   
.. index::
   single: field;income_wg
   
.. _lino.contacts.Person.income_wg:

Field **Person.income_wg**
==========================





Type: BooleanField

   
.. index::
   single: field;income_kg
   
.. _lino.contacts.Person.income_kg:

Field **Person.income_kg**
==========================





Type: BooleanField

   
.. index::
   single: field;income_rente
   
.. _lino.contacts.Person.income_rente:

Field **Person.income_rente**
=============================





Type: BooleanField

   
.. index::
   single: field;income_misc
   
.. _lino.contacts.Person.income_misc:

Field **Person.income_misc**
============================





Type: BooleanField

   
.. index::
   single: field;is_seeking
   
.. _lino.contacts.Person.is_seeking:

Field **Person.is_seeking**
===========================





Type: BooleanField

   
.. index::
   single: field;unavailable_until
   
.. _lino.contacts.Person.unavailable_until:

Field **Person.unavailable_until**
==================================





Type: DateField

   
.. index::
   single: field;unavailable_why
   
.. _lino.contacts.Person.unavailable_why:

Field **Person.unavailable_why**
================================





Type: CharField

   
.. index::
   single: field;obstacles
   
.. _lino.contacts.Person.obstacles:

Field **Person.obstacles**
==========================





Type: TextField

   
.. index::
   single: field;skills
   
.. _lino.contacts.Person.skills:

Field **Person.skills**
=======================





Type: TextField

   
.. index::
   single: field;job_agents
   
.. _lino.contacts.Person.job_agents:

Field **Person.job_agents**
===========================





Type: CharField

   
.. index::
   single: field;job_office_contact
   
.. _lino.contacts.Person.job_office_contact:

Field **Person.job_office_contact**
===================================





Type: ForeignKey

   


.. index::
   pair: model; Company

.. _lino.contacts.Company:

-----------------
Model **Company**
-----------------




Implements :class:`contacts.Company`.

Inner class Meta is necessary because of :doc:`/tickets/14`.

  
============= ============= =============================================================================
name          type          verbose name                                                                 
============= ============= =============================================================================
id            AutoField     ID                                                                           
country       ForeignKey    Country (Land,Pays)                                                          
city          ForeignKey    City (Stadt)                                                                 
name          CharField     Name (Nom)                                                                   
addr1         CharField     Address line before street (Adresszeile vor Straße,Ligne avant le nom de rue)
street_prefix CharField     Street prefix (Präfix Straße,Préfixe rue)                                    
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
contact_ptr   OneToOneField Contact (Kontakt)                                                            
vat_id        CharField     VAT id (MWSt.-Nr.,N° de TVA)                                                 
type          ForeignKey    Company type (Firmenart,Type de société)                                     
is_active     BooleanField  is active (aktiv,est actif)                                                  
activity      ForeignKey    Activity (Beruf,Activité)                                                    
bank_account1 CharField     Bank account 1 (Bankkonto 1,Compte en banque 1)                              
bank_account2 CharField     Bank account 2 (Bankkonto 2,Compte en banque 2)                              
prefix        CharField     prefix                                                                       
hourly_rate   PriceField    hourly rate (Stundensatz,coûr horaire)                                       
============= ============= =============================================================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from
`lino.jobs.JobProvider.company_ptr`_, `lino.links.Link.company`_, `lino.contacts.Person.health_insurance`_, `lino.contacts.Person.pharmacy`_, `lino.dsbe.CourseProvider.company_ptr`_, `lino.notes.Note.company`_, `lino.lino.SiteConfig.site_company`_, `lino.lino.SiteConfig.job_office`_, `lino.thirds.Third.company`_



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

   
.. index::
   single: field;is_active
   
.. _lino.contacts.Company.is_active:

Field **Company.is_active**
===========================





Type: BooleanField

   
.. index::
   single: field;activity
   
.. _lino.contacts.Company.activity:

Field **Company.activity**
==========================





Type: ForeignKey

   
.. index::
   single: field;bank_account1
   
.. _lino.contacts.Company.bank_account1:

Field **Company.bank_account1**
===============================





Type: CharField

   
.. index::
   single: field;bank_account2
   
.. _lino.contacts.Company.bank_account2:

Field **Company.bank_account2**
===============================





Type: CharField

   
.. index::
   single: field;prefix
   
.. _lino.contacts.Company.prefix:

Field **Company.prefix**
========================





Type: CharField

   
.. index::
   single: field;hourly_rate
   
.. _lino.contacts.Company.hourly_rate:

Field **Company.hourly_rate**
=============================





Type: PriceField

   


