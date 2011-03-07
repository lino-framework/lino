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
   single: field;name_fr
   single: field;name_nl
   single: field;name_en
   single: field;abbr_fr
   single: field;abbr_nl
   single: field;abbr_en
   single: field;contract_type

.. _dsbe.contacts.CompanyType:

---------------------
Model ``CompanyType``
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
   pair: model; ContactType
   single: field;id
   single: field;name
   single: field;name_fr
   single: field;name_nl
   single: field;name_en

.. _dsbe.contacts.ContactType:

---------------------
Model ``ContactType``
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
   pair: model; Contact
   single: field;id
   single: field;person
   single: field;company
   single: field;type

.. _dsbe.contacts.Contact:

-----------------
Model ``Contact``
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
   pair: model; Person
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
   single: field;id
   single: field;is_active
   single: field;activity
   single: field;bank_account1
   single: field;bank_account2
   single: field;gesdos_id
   single: field;is_cpas
   single: field;is_senior
   single: field;group
   single: field;coached_from
   single: field;coached_until
   single: field;coach1
   single: field;coach2
   single: field;sex
   single: field;birth_date
   single: field;birth_date_circa
   single: field;birth_place
   single: field;birth_country
   single: field;civil_state
   single: field;national_id
   single: field;health_insurance
   single: field;pharmacy
   single: field;nationality
   single: field;card_number
   single: field;card_valid_from
   single: field;card_valid_until
   single: field;card_type
   single: field;card_issuer
   single: field;noble_condition
   single: field;residence_type
   single: field;in_belgium_since
   single: field;unemployed_since
   single: field;needs_residence_permit
   single: field;needs_work_permit
   single: field;work_permit_suspended_until
   single: field;aid_type
   single: field;income_ag
   single: field;income_wg
   single: field;income_kg
   single: field;income_rente
   single: field;income_misc
   single: field;is_seeking
   single: field;unavailable_until
   single: field;unavailable_why
   single: field;native_language
   single: field;obstacles
   single: field;skills
   single: field;job_agents
   single: field;job_office_contact

.. _dsbe.contacts.Person:

----------------
Model ``Person``
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
   pair: model; Company
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
   single: field;id
   single: field;is_active
   single: field;activity
   single: field;bank_account1
   single: field;bank_account2
   single: field;prefix
   single: field;hourly_rate

.. _dsbe.contacts.Company:

-----------------
Model ``Company``
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


