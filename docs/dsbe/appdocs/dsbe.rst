====
dsbe
====



.. currentmodule:: dsbe

Defined in :srcref:`/lino/apps/dsbe/models.py`


See also :doc:`/dsbe/models`.



.. contents:: Table of Contents



.. index::
   pair: model; PersonGroup

.. _lino.dsbe.PersonGroup:

---------------------
Model **PersonGroup**
---------------------



Integration Phase (previously "Person Group")
    
  
======== ========= ==============================================
name     type      verbose name                                  
======== ========= ==============================================
id       AutoField ID                                            
name     CharField Designation (Beschreibung,Désignation)        
ref_name CharField Reference name (Referenzname,Nom de référence)
======== ========= ==============================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from
`lino.contacts.Person.group`_



.. index::
   single: field;id
   
.. _lino.dsbe.PersonGroup.id:

Field **PersonGroup.id**
========================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.dsbe.PersonGroup.name:

Field **PersonGroup.name**
==========================





Type: CharField

   
.. index::
   single: field;ref_name
   
.. _lino.dsbe.PersonGroup.ref_name:

Field **PersonGroup.ref_name**
==============================





Type: CharField

   


.. index::
   pair: model; StudyType

.. _lino.dsbe.StudyType:

-------------------
Model **StudyType**
-------------------



StudyType(id, name, name_fr, name_nl, name_en)
  
======= ============== ======================================
name    type           verbose name                          
======= ============== ======================================
id      AutoField      ID                                    
name    BabelCharField Designation (Beschreibung,Désignation)
name_fr CharField      Designation (fr)                      
name_nl CharField      Designation (nl)                      
name_en CharField      Designation (en)                      
======= ============== ======================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from
`lino.dsbe.Study.type`_



.. index::
   single: field;id
   
.. _lino.dsbe.StudyType.id:

Field **StudyType.id**
======================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.dsbe.StudyType.name:

Field **StudyType.name**
========================





Type: BabelCharField

   
.. index::
   single: field;name_fr
   
.. _lino.dsbe.StudyType.name_fr:

Field **StudyType.name_fr**
===========================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _lino.dsbe.StudyType.name_nl:

Field **StudyType.name_nl**
===========================





Type: CharField

   
.. index::
   single: field;name_en
   
.. _lino.dsbe.StudyType.name_en:

Field **StudyType.name_en**
===========================





Type: CharField

   


.. index::
   pair: model; Study

.. _lino.dsbe.Study:

---------------
Model **Study**
---------------



Study(id, country_id, city_id, person_id, type_id, content, started, stopped, success, language_id, school, remarks)
  
======== ============ ====================================================
name     type         verbose name                                        
======== ============ ====================================================
id       AutoField    ID                                                  
country  ForeignKey   Country (Land,Pays)                                 
city     ForeignKey   City (Stadt)                                        
person   ForeignKey   Person (Personne)                                   
type     ForeignKey   Study type (Ausbildungsart,Type d'études)           
content  CharField    Study content (Ausbildungsinhalt,Contenu des études)
started  MonthField   started (begonnen,commencé)                         
stopped  MonthField   stopped (beendet,arrêté)                            
success  BooleanField Success (Abschluss,Réussi)                          
language ForeignKey   Language (Sprache,Langue)                           
school   CharField    School (Schule,Ecole)                               
remarks  TextField    Remarks (Bemerkungen,Remarques)                     
======== ============ ====================================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.dsbe.Study.id:

Field **Study.id**
==================





Type: AutoField

   
.. index::
   single: field;country
   
.. _lino.dsbe.Study.country:

Field **Study.country**
=======================





Type: ForeignKey

   
.. index::
   single: field;city
   
.. _lino.dsbe.Study.city:

Field **Study.city**
====================





Type: ForeignKey

   
.. index::
   single: field;person
   
.. _lino.dsbe.Study.person:

Field **Study.person**
======================





Type: ForeignKey

   
.. index::
   single: field;type
   
.. _lino.dsbe.Study.type:

Field **Study.type**
====================





Type: ForeignKey

   
.. index::
   single: field;content
   
.. _lino.dsbe.Study.content:

Field **Study.content**
=======================





Type: CharField

   
.. index::
   single: field;started
   
.. _lino.dsbe.Study.started:

Field **Study.started**
=======================





Type: MonthField

   
.. index::
   single: field;stopped
   
.. _lino.dsbe.Study.stopped:

Field **Study.stopped**
=======================





Type: MonthField

   
.. index::
   single: field;success
   
.. _lino.dsbe.Study.success:

Field **Study.success**
=======================





Type: BooleanField

   
.. index::
   single: field;language
   
.. _lino.dsbe.Study.language:

Field **Study.language**
========================





Type: ForeignKey

   
.. index::
   single: field;school
   
.. _lino.dsbe.Study.school:

Field **Study.school**
======================





Type: CharField

   
.. index::
   single: field;remarks
   
.. _lino.dsbe.Study.remarks:

Field **Study.remarks**
=======================





Type: TextField

   


.. index::
   pair: model; LanguageKnowledge

.. _lino.dsbe.LanguageKnowledge:

---------------------------
Model **LanguageKnowledge**
---------------------------



Specifies how well a certain Person knows a certain Language.
    Deserves more documentation.
  
========= =============== =================================================
name      type            verbose name                                     
========= =============== =================================================
id        AutoField       ID                                               
person    ForeignKey      Person (Personne)                                
language  ForeignKey      Language (Sprache,Langue)                        
spoken    ChoiceListField spoken (Wort,oral)                               
written   ChoiceListField written (Schrift,écrit)                          
native    BooleanField    native language (Muttersprache,Langue maternelle)
cef_level ChoiceListField CEF level (CEF-Kategorie)                        
========= =============== =================================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.dsbe.LanguageKnowledge.id:

Field **LanguageKnowledge.id**
==============================





Type: AutoField

   
.. index::
   single: field;person
   
.. _lino.dsbe.LanguageKnowledge.person:

Field **LanguageKnowledge.person**
==================================





Type: ForeignKey

   
.. index::
   single: field;language
   
.. _lino.dsbe.LanguageKnowledge.language:

Field **LanguageKnowledge.language**
====================================





Type: ForeignKey

   
.. index::
   single: field;spoken
   
.. _lino.dsbe.LanguageKnowledge.spoken:

Field **LanguageKnowledge.spoken**
==================================





Type: ChoiceListField

   
.. index::
   single: field;written
   
.. _lino.dsbe.LanguageKnowledge.written:

Field **LanguageKnowledge.written**
===================================





Type: ChoiceListField

   
.. index::
   single: field;native
   
.. _lino.dsbe.LanguageKnowledge.native:

Field **LanguageKnowledge.native**
==================================





Type: BooleanField

   
.. index::
   single: field;cef_level
   
.. _lino.dsbe.LanguageKnowledge.cef_level:

Field **LanguageKnowledge.cef_level**
=====================================





Type: ChoiceListField

   


.. index::
   pair: model; JobExperience

.. _lino.dsbe.JobExperience:

-----------------------
Model **JobExperience**
-----------------------



JobExperience(id, person_id, company, title, country_id, started, stopped, remarks)
  
======= ========== ===============================================
name    type       verbose name                                   
======= ========== ===============================================
id      AutoField  ID                                             
person  ForeignKey Person (Personne)                              
company CharField  company (Firma,Société)                        
title   CharField  job title (Bezeichnung,Intitulé de la fonction)
country ForeignKey Country (Land,Pays)                            
started MonthField started (begonnen,commencé)                    
stopped MonthField stopped (beendet,arrêté)                       
remarks TextField  Remarks (Bemerkungen,Remarques)                
======= ========== ===============================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.dsbe.JobExperience.id:

Field **JobExperience.id**
==========================





Type: AutoField

   
.. index::
   single: field;person
   
.. _lino.dsbe.JobExperience.person:

Field **JobExperience.person**
==============================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _lino.dsbe.JobExperience.company:

Field **JobExperience.company**
===============================





Type: CharField

   
.. index::
   single: field;title
   
.. _lino.dsbe.JobExperience.title:

Field **JobExperience.title**
=============================





Type: CharField

   
.. index::
   single: field;country
   
.. _lino.dsbe.JobExperience.country:

Field **JobExperience.country**
===============================





Type: ForeignKey

   
.. index::
   single: field;started
   
.. _lino.dsbe.JobExperience.started:

Field **JobExperience.started**
===============================





Type: MonthField

   
.. index::
   single: field;stopped
   
.. _lino.dsbe.JobExperience.stopped:

Field **JobExperience.stopped**
===============================





Type: MonthField

   
.. index::
   single: field;remarks
   
.. _lino.dsbe.JobExperience.remarks:

Field **JobExperience.remarks**
===============================





Type: TextField

   


.. index::
   pair: model; Activity

.. _lino.dsbe.Activity:

------------------
Model **Activity**
------------------



Activity(id, name, lst104)
  
====== ============ ===============================================================
name   type         verbose name                                                   
====== ============ ===============================================================
id     AutoField    ID                                                             
name   CharField    name                                                           
lst104 BooleanField Appears in Listing 104 (Listing 104,Apparaît dans la liste 104)
====== ============ ===============================================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from
`lino.jobs.JobProvider.activity`_, `lino.contacts.Person.activity`_, `lino.contacts.Company.activity`_, `lino.dsbe.CourseProvider.activity`_



.. index::
   single: field;id
   
.. _lino.dsbe.Activity.id:

Field **Activity.id**
=====================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.dsbe.Activity.name:

Field **Activity.name**
=======================





Type: CharField

   
.. index::
   single: field;lst104
   
.. _lino.dsbe.Activity.lst104:

Field **Activity.lst104**
=========================





Type: BooleanField

   


.. index::
   pair: model; ExclusionType

.. _lino.dsbe.ExclusionType:

-----------------------
Model **ExclusionType**
-----------------------



ExclusionType(id, name)
  
==== ========= ============
name type      verbose name
==== ========= ============
id   AutoField ID          
name CharField name        
==== ========= ============

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from
`lino.dsbe.Exclusion.type`_



.. index::
   single: field;id
   
.. _lino.dsbe.ExclusionType.id:

Field **ExclusionType.id**
==========================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.dsbe.ExclusionType.name:

Field **ExclusionType.name**
============================





Type: CharField

   


.. index::
   pair: model; Exclusion

.. _lino.dsbe.Exclusion:

-------------------
Model **Exclusion**
-------------------



Exclusion(id, person_id, type_id, excluded_from, excluded_until, remark)
  
============== ========== ===========================
name           type       verbose name               
============== ========== ===========================
id             AutoField  ID                         
person         ForeignKey Person (Personne)          
type           ForeignKey Reason (Grund,Motif)       
excluded_from  DateField  from (von,de)              
excluded_until DateField  until (bis,jusque)         
remark         CharField  Remark (Bemerkung,Remarque)
============== ========== ===========================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.dsbe.Exclusion.id:

Field **Exclusion.id**
======================





Type: AutoField

   
.. index::
   single: field;person
   
.. _lino.dsbe.Exclusion.person:

Field **Exclusion.person**
==========================





Type: ForeignKey

   
.. index::
   single: field;type
   
.. _lino.dsbe.Exclusion.type:

Field **Exclusion.type**
========================





Type: ForeignKey

   
.. index::
   single: field;excluded_from
   
.. _lino.dsbe.Exclusion.excluded_from:

Field **Exclusion.excluded_from**
=================================





Type: DateField

   
.. index::
   single: field;excluded_until
   
.. _lino.dsbe.Exclusion.excluded_until:

Field **Exclusion.excluded_until**
==================================





Type: DateField

   
.. index::
   single: field;remark
   
.. _lino.dsbe.Exclusion.remark:

Field **Exclusion.remark**
==========================





Type: CharField

   


.. index::
   pair: model; CourseEnding

.. _lino.dsbe.CourseEnding:

----------------------
Model **CourseEnding**
----------------------




Eine Kursbeendigung ist eine *Art und Weise, wie eine Kursanfrage beendet wurde*.
Später können wir dann Statistiken machen, wieviele Anfragen auf welche Art und 
Weise beendet wurden.

  
==== ========= =====================================
name type      verbose name                         
==== ========= =====================================
id   AutoField ID                                   
name CharField designation (Bezeichnung,désignation)
==== ========= =====================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from
`lino.dsbe.CourseRequest.ending`_



.. index::
   single: field;id
   
.. _lino.dsbe.CourseEnding.id:

Field **CourseEnding.id**
=========================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.dsbe.CourseEnding.name:

Field **CourseEnding.name**
===========================





Type: CharField

   


.. index::
   pair: model; AidType

.. _lino.dsbe.AidType:

-----------------
Model **AidType**
-----------------



AidType(id, name, name_fr, name_nl, name_en)
  
======= ============== ======================================
name    type           verbose name                          
======= ============== ======================================
id      AutoField      ID                                    
name    BabelCharField Designation (Beschreibung,Désignation)
name_fr CharField      Designation (fr)                      
name_nl CharField      Designation (nl)                      
name_en CharField      Designation (en)                      
======= ============== ======================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from
`lino.contacts.Person.aid_type`_



.. index::
   single: field;id
   
.. _lino.dsbe.AidType.id:

Field **AidType.id**
====================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.dsbe.AidType.name:

Field **AidType.name**
======================





Type: BabelCharField

   
.. index::
   single: field;name_fr
   
.. _lino.dsbe.AidType.name_fr:

Field **AidType.name_fr**
=========================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _lino.dsbe.AidType.name_nl:

Field **AidType.name_nl**
=========================





Type: CharField

   
.. index::
   single: field;name_en
   
.. _lino.dsbe.AidType.name_en:

Field **AidType.name_en**
=========================





Type: CharField

   


.. index::
   pair: model; CourseProvider

.. _lino.dsbe.CourseProvider:

------------------------
Model **CourseProvider**
------------------------



Kursanbieter (KAP, Oikos, Lupe, ...) 
    
  
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
company_ptr   OneToOneField Company (Firma,Société)                                                      
============= ============= =============================================================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from
`lino.dsbe.Course.provider`_



.. index::
   single: field;id
   
.. _lino.dsbe.CourseProvider.id:

Field **CourseProvider.id**
===========================





Type: AutoField

   
.. index::
   single: field;country
   
.. _lino.dsbe.CourseProvider.country:

Field **CourseProvider.country**
================================





Type: ForeignKey

   
.. index::
   single: field;city
   
.. _lino.dsbe.CourseProvider.city:

Field **CourseProvider.city**
=============================





Type: ForeignKey

   
.. index::
   single: field;name
   
.. _lino.dsbe.CourseProvider.name:

Field **CourseProvider.name**
=============================





Type: CharField

   
.. index::
   single: field;addr1
   
.. _lino.dsbe.CourseProvider.addr1:

Field **CourseProvider.addr1**
==============================



Address line before street

Type: CharField

   
.. index::
   single: field;street_prefix
   
.. _lino.dsbe.CourseProvider.street_prefix:

Field **CourseProvider.street_prefix**
======================================



Text to print before name of street, but to ignore for sorting.

Type: CharField

   
.. index::
   single: field;street
   
.. _lino.dsbe.CourseProvider.street:

Field **CourseProvider.street**
===============================



Name of street. Without house number.

Type: CharField

   
.. index::
   single: field;street_no
   
.. _lino.dsbe.CourseProvider.street_no:

Field **CourseProvider.street_no**
==================================



House number

Type: CharField

   
.. index::
   single: field;street_box
   
.. _lino.dsbe.CourseProvider.street_box:

Field **CourseProvider.street_box**
===================================



Text to print after :attr:`steet_no` on the same line

Type: CharField

   
.. index::
   single: field;addr2
   
.. _lino.dsbe.CourseProvider.addr2:

Field **CourseProvider.addr2**
==============================



Address line to print below street line

Type: CharField

   
.. index::
   single: field;zip_code
   
.. _lino.dsbe.CourseProvider.zip_code:

Field **CourseProvider.zip_code**
=================================





Type: CharField

   
.. index::
   single: field;region
   
.. _lino.dsbe.CourseProvider.region:

Field **CourseProvider.region**
===============================





Type: CharField

   
.. index::
   single: field;language
   
.. _lino.dsbe.CourseProvider.language:

Field **CourseProvider.language**
=================================





Type: LanguageField

   
.. index::
   single: field;email
   
.. _lino.dsbe.CourseProvider.email:

Field **CourseProvider.email**
==============================





Type: EmailField

   
.. index::
   single: field;url
   
.. _lino.dsbe.CourseProvider.url:

Field **CourseProvider.url**
============================





Type: URLField

   
.. index::
   single: field;phone
   
.. _lino.dsbe.CourseProvider.phone:

Field **CourseProvider.phone**
==============================





Type: CharField

   
.. index::
   single: field;gsm
   
.. _lino.dsbe.CourseProvider.gsm:

Field **CourseProvider.gsm**
============================





Type: CharField

   
.. index::
   single: field;fax
   
.. _lino.dsbe.CourseProvider.fax:

Field **CourseProvider.fax**
============================





Type: CharField

   
.. index::
   single: field;remarks
   
.. _lino.dsbe.CourseProvider.remarks:

Field **CourseProvider.remarks**
================================





Type: TextField

   
.. index::
   single: field;contact_ptr
   
.. _lino.dsbe.CourseProvider.contact_ptr:

Field **CourseProvider.contact_ptr**
====================================





Type: OneToOneField

   
.. index::
   single: field;vat_id
   
.. _lino.dsbe.CourseProvider.vat_id:

Field **CourseProvider.vat_id**
===============================





Type: CharField

   
.. index::
   single: field;type
   
.. _lino.dsbe.CourseProvider.type:

Field **CourseProvider.type**
=============================





Type: ForeignKey

   
.. index::
   single: field;is_active
   
.. _lino.dsbe.CourseProvider.is_active:

Field **CourseProvider.is_active**
==================================





Type: BooleanField

   
.. index::
   single: field;activity
   
.. _lino.dsbe.CourseProvider.activity:

Field **CourseProvider.activity**
=================================





Type: ForeignKey

   
.. index::
   single: field;bank_account1
   
.. _lino.dsbe.CourseProvider.bank_account1:

Field **CourseProvider.bank_account1**
======================================





Type: CharField

   
.. index::
   single: field;bank_account2
   
.. _lino.dsbe.CourseProvider.bank_account2:

Field **CourseProvider.bank_account2**
======================================





Type: CharField

   
.. index::
   single: field;prefix
   
.. _lino.dsbe.CourseProvider.prefix:

Field **CourseProvider.prefix**
===============================





Type: CharField

   
.. index::
   single: field;hourly_rate
   
.. _lino.dsbe.CourseProvider.hourly_rate:

Field **CourseProvider.hourly_rate**
====================================





Type: PriceField

   
.. index::
   single: field;company_ptr
   
.. _lino.dsbe.CourseProvider.company_ptr:

Field **CourseProvider.company_ptr**
====================================





Type: OneToOneField

   


.. index::
   pair: model; CourseContent

.. _lino.dsbe.CourseContent:

-----------------------
Model **CourseContent**
-----------------------




Ein Kursinhalt (z.B. "Französisch", "Deutsch", "Alphabétisation",...)

  
==== ========= ============
name type      verbose name
==== ========= ============
id   AutoField ID          
name CharField Name (Nom)  
==== ========= ============

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from
`lino.dsbe.Course.content`_, `lino.dsbe.CourseRequest.content`_



.. index::
   single: field;id
   
.. _lino.dsbe.CourseContent.id:

Field **CourseContent.id**
==========================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.dsbe.CourseContent.name:

Field **CourseContent.name**
============================





Type: CharField

   


.. index::
   pair: model; Course

.. _lino.dsbe.Course:

----------------
Model **Course**
----------------




Ein konkreter Kurs, der an einem bestimmten Datum beginnt 
und bei einem bestimmten 
:class:`Kursanbieter <CourseProvider>` stattfindet
(und für den ihr Kandidaten zu vermitteln plant).

  
========== ========== ==================================================
name       type       verbose name                                      
========== ========== ==================================================
id         AutoField  ID                                                
title      CharField  Name (Nom)                                        
content    ForeignKey Course content (Kursinhalt,Contenu du cours)      
provider   ForeignKey Course provider (Kursanbieter,dispenseur de cours)
start_date DateField  start date (beginnt am,Date de début)             
remark     CharField  Remark (Bemerkung,Remarque)                       
========== ========== ==================================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from
`lino.dsbe.CourseRequest.course`_



.. index::
   single: field;id
   
.. _lino.dsbe.Course.id:

Field **Course.id**
===================





Type: AutoField

   
.. index::
   single: field;title
   
.. _lino.dsbe.Course.title:

Field **Course.title**
======================





Type: CharField

   
.. index::
   single: field;content
   
.. _lino.dsbe.Course.content:

Field **Course.content**
========================





Type: ForeignKey

   
.. index::
   single: field;provider
   
.. _lino.dsbe.Course.provider:

Field **Course.provider**
=========================





Type: ForeignKey

   
.. index::
   single: field;start_date
   
.. _lino.dsbe.Course.start_date:

Field **Course.start_date**
===========================





Type: DateField

   
.. index::
   single: field;remark
   
.. _lino.dsbe.Course.remark:

Field **Course.remark**
=======================





Type: CharField

   


.. index::
   pair: model; CourseRequest

.. _lino.dsbe.CourseRequest:

-----------------------
Model **CourseRequest**
-----------------------




A Course Request is created when a certain Person expresses her 
wish to participate in a Course with a certain CourseContent.

  
============== ========== =============================================
name           type       verbose name                                 
============== ========== =============================================
id             AutoField  ID                                           
person         ForeignKey Person (Personne)                            
content        ForeignKey Course content (Kursinhalt,Contenu du cours) 
date_submitted DateField  date submitted (eingereicht am ,date d'envoi)
course         ForeignKey Course found (Kurs gefunden,Cours trouvé)    
remark         TextField  Remark (Bemerkung,Remarque)                  
date_ended     DateField  date ended (Beendet am,date de fin)          
ending         ForeignKey Ending (Beendigung,Fin)                      
============== ========== =============================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.dsbe.CourseRequest.id:

Field **CourseRequest.id**
==========================





Type: AutoField

   
.. index::
   single: field;person
   
.. _lino.dsbe.CourseRequest.person:

Field **CourseRequest.person**
==============================





Type: ForeignKey

   
.. index::
   single: field;content
   
.. _lino.dsbe.CourseRequest.content:

Field **CourseRequest.content**
===============================





Type: ForeignKey

   
.. index::
   single: field;date_submitted
   
.. _lino.dsbe.CourseRequest.date_submitted:

Field **CourseRequest.date_submitted**
======================================





Type: DateField

   
.. index::
   single: field;course
   
.. _lino.dsbe.CourseRequest.course:

Field **CourseRequest.course**
==============================





Type: ForeignKey

   
.. index::
   single: field;remark
   
.. _lino.dsbe.CourseRequest.remark:

Field **CourseRequest.remark**
==============================





Type: TextField

   
.. index::
   single: field;date_ended
   
.. _lino.dsbe.CourseRequest.date_ended:

Field **CourseRequest.date_ended**
==================================





Type: DateField

   
.. index::
   single: field;ending
   
.. _lino.dsbe.CourseRequest.ending:

Field **CourseRequest.ending**
==============================





Type: ForeignKey

   


.. index::
   pair: model; PersonSearch

.. _lino.dsbe.PersonSearch:

----------------------
Model **PersonSearch**
----------------------



PersonSearch(id, user_id, title, aged_from, aged_to, sex, only_my_persons, coached_by_id, period_from, period_until)
  
=============== ============ =========================================================
name            type         verbose name                                             
=============== ============ =========================================================
id              AutoField    ID                                                       
user            ForeignKey   User (Benutzer,Utilisateur)                              
title           CharField    Search Title (Titel Suchliste,Intitulé de la recherche)  
aged_from       IntegerField Aged from (Alter von,Age: de)                            
aged_to         IntegerField Aged to (Alter bis,Age: jusque)                          
sex             CharField    Sex                                                      
only_my_persons BooleanField Only my persons (nur meine Leute,Seulement mes personnes)
coached_by      ForeignKey   Coached by (Begleitet durch,Accompagné par)              
period_from     DateField    Period from (Periode vom,Période: depuis)                
period_until    DateField    until (bis,jusque)                                       
=============== ============ =========================================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from
`lino.dsbe.WantedLanguageKnowledge.search`_, `lino.properties.WantedSkill.search`_, `lino.properties.UnwantedSkill.search`_



.. index::
   single: field;id
   
.. _lino.dsbe.PersonSearch.id:

Field **PersonSearch.id**
=========================





Type: AutoField

   
.. index::
   single: field;user
   
.. _lino.dsbe.PersonSearch.user:

Field **PersonSearch.user**
===========================





Type: ForeignKey

   
.. index::
   single: field;title
   
.. _lino.dsbe.PersonSearch.title:

Field **PersonSearch.title**
============================





Type: CharField

   
.. index::
   single: field;aged_from
   
.. _lino.dsbe.PersonSearch.aged_from:

Field **PersonSearch.aged_from**
================================





Type: IntegerField

   
.. index::
   single: field;aged_to
   
.. _lino.dsbe.PersonSearch.aged_to:

Field **PersonSearch.aged_to**
==============================





Type: IntegerField

   
.. index::
   single: field;sex
   
.. _lino.dsbe.PersonSearch.sex:

Field **PersonSearch.sex**
==========================





Type: CharField

   
.. index::
   single: field;only_my_persons
   
.. _lino.dsbe.PersonSearch.only_my_persons:

Field **PersonSearch.only_my_persons**
======================================





Type: BooleanField

   
.. index::
   single: field;coached_by
   
.. _lino.dsbe.PersonSearch.coached_by:

Field **PersonSearch.coached_by**
=================================





Type: ForeignKey

   
.. index::
   single: field;period_from
   
.. _lino.dsbe.PersonSearch.period_from:

Field **PersonSearch.period_from**
==================================





Type: DateField

   
.. index::
   single: field;period_until
   
.. _lino.dsbe.PersonSearch.period_until:

Field **PersonSearch.period_until**
===================================





Type: DateField

   


.. index::
   pair: model; WantedLanguageKnowledge

.. _lino.dsbe.WantedLanguageKnowledge:

---------------------------------
Model **WantedLanguageKnowledge**
---------------------------------



WantedLanguageKnowledge(id, search_id, language_id, spoken, written)
  
======== =============== ====================================================
name     type            verbose name                                        
======== =============== ====================================================
id       AutoField       ID                                                  
search   ForeignKey      Person Search (Personensuche,Recherche de personnes)
language ForeignKey      Language (Sprache,Langue)                           
spoken   ChoiceListField spoken (Wort,oral)                                  
written  ChoiceListField written (Schrift,écrit)                             
======== =============== ====================================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.dsbe.WantedLanguageKnowledge.id:

Field **WantedLanguageKnowledge.id**
====================================





Type: AutoField

   
.. index::
   single: field;search
   
.. _lino.dsbe.WantedLanguageKnowledge.search:

Field **WantedLanguageKnowledge.search**
========================================





Type: ForeignKey

   
.. index::
   single: field;language
   
.. _lino.dsbe.WantedLanguageKnowledge.language:

Field **WantedLanguageKnowledge.language**
==========================================





Type: ForeignKey

   
.. index::
   single: field;spoken
   
.. _lino.dsbe.WantedLanguageKnowledge.spoken:

Field **WantedLanguageKnowledge.spoken**
========================================





Type: ChoiceListField

   
.. index::
   single: field;written
   
.. _lino.dsbe.WantedLanguageKnowledge.written:

Field **WantedLanguageKnowledge.written**
=========================================





Type: ChoiceListField

   


