====
dsbe
====



.. currentmodule:: dsbe

Defined in :srcref:`/lino/sites/dsbe/models.py`


See also :doc:`/dsbe/models`



.. contents:: Table of Contents



.. index::
   pair: model; PersonGroup

.. _dsbe.dsbe.PersonGroup:

---------------------
Model **PersonGroup**
---------------------



PersonGroup(id, name)
  
==== ========= ==========================
name type      verbose name              
==== ========= ==========================
id   AutoField ID                        
name CharField Designation (Beschreibung)
==== ========= ==========================

    
Defined in :srcref:`/lino/sites/dsbe/models.py`

.. index::
   single: field;id
   
.. _dsbe.dsbe.PersonGroup.id:

Field **PersonGroup.id**
========================





Type: AutoField

   
.. index::
   single: field;name
   
.. _dsbe.dsbe.PersonGroup.name:

Field **PersonGroup.name**
==========================





Type: CharField

   


.. index::
   pair: model; StudyType

.. _dsbe.dsbe.StudyType:

-------------------
Model **StudyType**
-------------------



StudyType(id, name)
  
==== ========= ==========================
name type      verbose name              
==== ========= ==========================
id   AutoField ID                        
name CharField Designation (Beschreibung)
==== ========= ==========================

    
Defined in :srcref:`/lino/sites/dsbe/models.py`

.. index::
   single: field;id
   
.. _dsbe.dsbe.StudyType.id:

Field **StudyType.id**
======================





Type: AutoField

   
.. index::
   single: field;name
   
.. _dsbe.dsbe.StudyType.name:

Field **StudyType.name**
========================





Type: CharField

   


.. index::
   pair: model; Study

.. _dsbe.dsbe.Study:

---------------
Model **Study**
---------------



Study(id, person_id, type_id, content, started, stopped, success, country_id, city_id, language_id, school, remarks)
  
======== ============ =================================
name     type         verbose name                     
======== ============ =================================
id       AutoField    ID                               
person   ForeignKey   Person                           
type     ForeignKey   Study type (Ausbildungsart)      
content  CharField    Study content (Ausbildungsinhalt)
started  MonthField   started (begonnen)               
stopped  MonthField   stopped (beendet)                
success  BooleanField Success (Abschluss)              
country  ForeignKey   Country (Land)                   
city     ForeignKey   City (Stadt)                     
language ForeignKey   Language (Sprache)               
school   CharField    School (Schule)                  
remarks  TextField    Remarks (Bemerkungen)            
======== ============ =================================

    
Defined in :srcref:`/lino/sites/dsbe/models.py`

.. index::
   single: field;id
   
.. _dsbe.dsbe.Study.id:

Field **Study.id**
==================





Type: AutoField

   
.. index::
   single: field;person
   
.. _dsbe.dsbe.Study.person:

Field **Study.person**
======================





Type: ForeignKey

   
.. index::
   single: field;type
   
.. _dsbe.dsbe.Study.type:

Field **Study.type**
====================





Type: ForeignKey

   
.. index::
   single: field;content
   
.. _dsbe.dsbe.Study.content:

Field **Study.content**
=======================





Type: CharField

   
.. index::
   single: field;started
   
.. _dsbe.dsbe.Study.started:

Field **Study.started**
=======================





Type: MonthField

   
.. index::
   single: field;stopped
   
.. _dsbe.dsbe.Study.stopped:

Field **Study.stopped**
=======================





Type: MonthField

   
.. index::
   single: field;success
   
.. _dsbe.dsbe.Study.success:

Field **Study.success**
=======================





Type: BooleanField

   
.. index::
   single: field;country
   
.. _dsbe.dsbe.Study.country:

Field **Study.country**
=======================





Type: ForeignKey

   
.. index::
   single: field;city
   
.. _dsbe.dsbe.Study.city:

Field **Study.city**
====================





Type: ForeignKey

   
.. index::
   single: field;language
   
.. _dsbe.dsbe.Study.language:

Field **Study.language**
========================





Type: ForeignKey

   
.. index::
   single: field;school
   
.. _dsbe.dsbe.Study.school:

Field **Study.school**
======================





Type: CharField

   
.. index::
   single: field;remarks
   
.. _dsbe.dsbe.Study.remarks:

Field **Study.remarks**
=======================





Type: TextField

   


.. index::
   pair: model; LanguageKnowledge

.. _dsbe.dsbe.LanguageKnowledge:

---------------------------
Model **LanguageKnowledge**
---------------------------



LanguageKnowledge(id, person_id, language_id, spoken, written)
  
======== =============== ==================
name     type            verbose name      
======== =============== ==================
id       AutoField       ID                
person   ForeignKey      person (Person)   
language ForeignKey      Language (Sprache)
spoken   ChoiceListField spoken (Wort)     
written  ChoiceListField written (Schrift) 
======== =============== ==================

    
Defined in :srcref:`/lino/sites/dsbe/models.py`

.. index::
   single: field;id
   
.. _dsbe.dsbe.LanguageKnowledge.id:

Field **LanguageKnowledge.id**
==============================





Type: AutoField

   
.. index::
   single: field;person
   
.. _dsbe.dsbe.LanguageKnowledge.person:

Field **LanguageKnowledge.person**
==================================





Type: ForeignKey

   
.. index::
   single: field;language
   
.. _dsbe.dsbe.LanguageKnowledge.language:

Field **LanguageKnowledge.language**
====================================





Type: ForeignKey

   
.. index::
   single: field;spoken
   
.. _dsbe.dsbe.LanguageKnowledge.spoken:

Field **LanguageKnowledge.spoken**
==================================





Type: ChoiceListField

   
.. index::
   single: field;written
   
.. _dsbe.dsbe.LanguageKnowledge.written:

Field **LanguageKnowledge.written**
===================================





Type: ChoiceListField

   


.. index::
   pair: model; JobExperience

.. _dsbe.dsbe.JobExperience:

-----------------------
Model **JobExperience**
-----------------------



JobExperience(id, person_id, company, title, country_id, started, stopped, remarks)
  
======= ========== =======================
name    type       verbose name           
======= ========== =======================
id      AutoField  ID                     
person  ForeignKey Person                 
company CharField  company (Firma)        
title   CharField  job title (Bezeichnung)
country ForeignKey Country (Land)         
started MonthField started (begonnen)     
stopped MonthField stopped (beendet)      
remarks TextField  Remarks (Bemerkungen)  
======= ========== =======================

    
Defined in :srcref:`/lino/sites/dsbe/models.py`

.. index::
   single: field;id
   
.. _dsbe.dsbe.JobExperience.id:

Field **JobExperience.id**
==========================





Type: AutoField

   
.. index::
   single: field;person
   
.. _dsbe.dsbe.JobExperience.person:

Field **JobExperience.person**
==============================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _dsbe.dsbe.JobExperience.company:

Field **JobExperience.company**
===============================





Type: CharField

   
.. index::
   single: field;title
   
.. _dsbe.dsbe.JobExperience.title:

Field **JobExperience.title**
=============================





Type: CharField

   
.. index::
   single: field;country
   
.. _dsbe.dsbe.JobExperience.country:

Field **JobExperience.country**
===============================





Type: ForeignKey

   
.. index::
   single: field;started
   
.. _dsbe.dsbe.JobExperience.started:

Field **JobExperience.started**
===============================





Type: MonthField

   
.. index::
   single: field;stopped
   
.. _dsbe.dsbe.JobExperience.stopped:

Field **JobExperience.stopped**
===============================





Type: MonthField

   
.. index::
   single: field;remarks
   
.. _dsbe.dsbe.JobExperience.remarks:

Field **JobExperience.remarks**
===============================





Type: TextField

   


.. index::
   pair: model; Activity

.. _dsbe.dsbe.Activity:

------------------
Model **Activity**
------------------



Activity(id, name, lst104)
  
====== ============ ====================================
name   type         verbose name                        
====== ============ ====================================
id     AutoField    ID                                  
name   CharField    name                                
lst104 BooleanField Appears in Listing 104 (Listing 104)
====== ============ ====================================

    
Defined in :srcref:`/lino/sites/dsbe/models.py`

.. index::
   single: field;id
   
.. _dsbe.dsbe.Activity.id:

Field **Activity.id**
=====================





Type: AutoField

   
.. index::
   single: field;name
   
.. _dsbe.dsbe.Activity.name:

Field **Activity.name**
=======================





Type: CharField

   
.. index::
   single: field;lst104
   
.. _dsbe.dsbe.Activity.lst104:

Field **Activity.lst104**
=========================





Type: BooleanField

   


.. index::
   pair: model; ExclusionType

.. _dsbe.dsbe.ExclusionType:

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

    
Defined in :srcref:`/lino/sites/dsbe/models.py`

.. index::
   single: field;id
   
.. _dsbe.dsbe.ExclusionType.id:

Field **ExclusionType.id**
==========================





Type: AutoField

   
.. index::
   single: field;name
   
.. _dsbe.dsbe.ExclusionType.name:

Field **ExclusionType.name**
============================





Type: CharField

   


.. index::
   pair: model; Exclusion

.. _dsbe.dsbe.Exclusion:

-------------------
Model **Exclusion**
-------------------



Exclusion(id, person_id, type_id, excluded_from, excluded_until, remark)
  
============== ========== ==================
name           type       verbose name      
============== ========== ==================
id             AutoField  ID                
person         ForeignKey person (Person)   
type           ForeignKey Reason (Grund)    
excluded_from  DateField  from (von)        
excluded_until DateField  until (bis)       
remark         CharField  Remark (Bemerkung)
============== ========== ==================

    
Defined in :srcref:`/lino/sites/dsbe/models.py`

.. index::
   single: field;id
   
.. _dsbe.dsbe.Exclusion.id:

Field **Exclusion.id**
======================





Type: AutoField

   
.. index::
   single: field;person
   
.. _dsbe.dsbe.Exclusion.person:

Field **Exclusion.person**
==========================





Type: ForeignKey

   
.. index::
   single: field;type
   
.. _dsbe.dsbe.Exclusion.type:

Field **Exclusion.type**
========================





Type: ForeignKey

   
.. index::
   single: field;excluded_from
   
.. _dsbe.dsbe.Exclusion.excluded_from:

Field **Exclusion.excluded_from**
=================================





Type: DateField

   
.. index::
   single: field;excluded_until
   
.. _dsbe.dsbe.Exclusion.excluded_until:

Field **Exclusion.excluded_until**
==================================





Type: DateField

   
.. index::
   single: field;remark
   
.. _dsbe.dsbe.Exclusion.remark:

Field **Exclusion.remark**
==========================





Type: CharField

   


.. index::
   pair: model; ContractType

.. _dsbe.dsbe.ContractType:

----------------------
Model **ContractType**
----------------------



ContractType(id, build_method, template, ref, name)
  
============ ========= ===================================
name         type      verbose name                       
============ ========= ===================================
id           AutoField ID                                 
build_method CharField Build method (Konstruktionsmethode)
template     CharField Template (Vorlage)                 
ref          CharField reference (Referenz)               
name         CharField contract title (Vertragstitel)     
name_fr      CharField contract title (fr)                
name_nl      CharField contract title (nl)                
name_en      CharField contract title (en)                
============ ========= ===================================

    
Defined in :srcref:`/lino/sites/dsbe/models.py`

.. index::
   single: field;id
   
.. _dsbe.dsbe.ContractType.id:

Field **ContractType.id**
=========================





Type: AutoField

   
.. index::
   single: field;build_method
   
.. _dsbe.dsbe.ContractType.build_method:

Field **ContractType.build_method**
===================================





Type: CharField

   
.. index::
   single: field;template
   
.. _dsbe.dsbe.ContractType.template:

Field **ContractType.template**
===============================





Type: CharField

   
.. index::
   single: field;ref
   
.. _dsbe.dsbe.ContractType.ref:

Field **ContractType.ref**
==========================





Type: CharField

   
.. index::
   single: field;name
   
.. _dsbe.dsbe.ContractType.name:

Field **ContractType.name**
===========================





Type: CharField

   
.. index::
   single: field;name_fr
   
.. _dsbe.dsbe.ContractType.name_fr:

Field **ContractType.name_fr**
==============================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _dsbe.dsbe.ContractType.name_nl:

Field **ContractType.name_nl**
==============================





Type: CharField

   
.. index::
   single: field;name_en
   
.. _dsbe.dsbe.ContractType.name_en:

Field **ContractType.name_en**
==============================





Type: CharField

   


.. index::
   pair: model; ExamPolicy

.. _dsbe.dsbe.ExamPolicy:

--------------------
Model **ExamPolicy**
--------------------



ExamPolicy(id, name)
  
======= ========= =========================
name    type      verbose name             
======= ========= =========================
id      AutoField ID                       
name    CharField designation (Bezeichnung)
name_fr CharField designation (fr)         
name_nl CharField designation (nl)         
name_en CharField designation (en)         
======= ========= =========================

    
Defined in :srcref:`/lino/sites/dsbe/models.py`

.. index::
   single: field;id
   
.. _dsbe.dsbe.ExamPolicy.id:

Field **ExamPolicy.id**
=======================





Type: AutoField

   
.. index::
   single: field;name
   
.. _dsbe.dsbe.ExamPolicy.name:

Field **ExamPolicy.name**
=========================





Type: CharField

   
.. index::
   single: field;name_fr
   
.. _dsbe.dsbe.ExamPolicy.name_fr:

Field **ExamPolicy.name_fr**
============================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _dsbe.dsbe.ExamPolicy.name_nl:

Field **ExamPolicy.name_nl**
============================





Type: CharField

   
.. index::
   single: field;name_en
   
.. _dsbe.dsbe.ExamPolicy.name_en:

Field **ExamPolicy.name_en**
============================





Type: CharField

   


.. index::
   pair: model; ContractEnding

.. _dsbe.dsbe.ContractEnding:

------------------------
Model **ContractEnding**
------------------------



ContractEnding(id, name)
  
==== ========= =========================
name type      verbose name             
==== ========= =========================
id   AutoField ID                       
name CharField designation (Bezeichnung)
==== ========= =========================

    
Defined in :srcref:`/lino/sites/dsbe/models.py`

.. index::
   single: field;id
   
.. _dsbe.dsbe.ContractEnding.id:

Field **ContractEnding.id**
===========================





Type: AutoField

   
.. index::
   single: field;name
   
.. _dsbe.dsbe.ContractEnding.name:

Field **ContractEnding.name**
=============================





Type: CharField

   


.. index::
   pair: model; CourseEnding

.. _dsbe.dsbe.CourseEnding:

----------------------
Model **CourseEnding**
----------------------




Eine Kursbeendigung ist eine *Art und Weise, wie eine Kursanfrage beendet wurde*.
Später können wir dann Statistiken machen, wieviele Anfragen auf welche Art und 
Weise beendet wurden.

  
==== ========= =========================
name type      verbose name             
==== ========= =========================
id   AutoField ID                       
name CharField designation (Bezeichnung)
==== ========= =========================

    
Defined in :srcref:`/lino/sites/dsbe/models.py`

.. index::
   single: field;id
   
.. _dsbe.dsbe.CourseEnding.id:

Field **CourseEnding.id**
=========================





Type: AutoField

   
.. index::
   single: field;name
   
.. _dsbe.dsbe.CourseEnding.name:

Field **CourseEnding.name**
===========================





Type: CharField

   


.. index::
   pair: model; AidType

.. _dsbe.dsbe.AidType:

-----------------
Model **AidType**
-----------------



AidType(id, name)
  
======= ========= =========================
name    type      verbose name             
======= ========= =========================
id      AutoField ID                       
name    CharField designation (Bezeichnung)
name_fr CharField designation (fr)         
name_nl CharField designation (nl)         
name_en CharField designation (en)         
======= ========= =========================

    
Defined in :srcref:`/lino/sites/dsbe/models.py`

.. index::
   single: field;id
   
.. _dsbe.dsbe.AidType.id:

Field **AidType.id**
====================





Type: AutoField

   
.. index::
   single: field;name
   
.. _dsbe.dsbe.AidType.name:

Field **AidType.name**
======================





Type: CharField

   
.. index::
   single: field;name_fr
   
.. _dsbe.dsbe.AidType.name_fr:

Field **AidType.name_fr**
=========================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _dsbe.dsbe.AidType.name_nl:

Field **AidType.name_nl**
=========================





Type: CharField

   
.. index::
   single: field;name_en
   
.. _dsbe.dsbe.AidType.name_en:

Field **AidType.name_en**
=========================





Type: CharField

   


.. index::
   pair: model; Contract

.. _dsbe.dsbe.Contract:

------------------
Model **Contract**
------------------




A Contract

  
================ ============= ============================================
name             type          verbose name                                
================ ============= ============================================
id               AutoField     ID                                          
user             ForeignKey    responsible (DSBE) (Verantwortlicher (DSBE))
reminder_date    DateField     Due date (Fällig am)                        
reminder_text    CharField     Reminder text (Erinnerungstext)             
delay_value      IntegerField  Delay (value) (Frist (Wert))                
delay_type       CharField     Delay (unit) (Frist (Einheit))              
must_build       BooleanField  must build (muss generiert werden)          
person           ForeignKey    Person                                      
company          ForeignKey    Company                                     
contact          ForeignKey    represented by                              
language         LanguageField Language (Sprache)                          
type             ForeignKey    contract type (Vertragsart)                 
applies_from     DateField     applies from (Laufzeit von)                 
applies_until    DateField     applies until (Laufzeit bis)                
date_decided     DateField     date decided (Beschlossen am)               
date_issued      DateField     date issued (Ausgestellt am)                
duration         IntegerField  duration (days) (Dauer (Arbeitstage))       
regime           CharField     regime (Regime)                             
schedule         CharField     schedule (Stundenplan)                      
hourly_rate      PriceField    hourly rate (Stundensatz)                   
refund_rate      CharField     refund rate (Rückzahlung)                   
reference_person CharField     reference person (Referenzperson)           
responsibilities TextField     responsibilities (Aufgabenbereich)          
stages           HtmlTextField stages (Etappen)                            
goals            HtmlTextField goals (Zielsetzungen)                       
duties_asd       HtmlTextField duties ASD (Verpflichtungen ASD)            
duties_dsbe      HtmlTextField duties DSBE (Verpflichtungen DSBE)          
duties_company   HtmlTextField duties company (Verpflichtungen Firma)      
user_asd         ForeignKey    responsible (ASD) (Verantwortlicher (ASD))  
exam_policy      ForeignKey    examination policy (Auswertungsstrategie)   
ending           ForeignKey    Ending (Beendigung)                         
date_ended       DateField     date ended (Beendet am)                     
================ ============= ============================================

    
Defined in :srcref:`/lino/sites/dsbe/models.py`

.. index::
   single: field;id
   
.. _dsbe.dsbe.Contract.id:

Field **Contract.id**
=====================





Type: AutoField

   
.. index::
   single: field;user
   
.. _dsbe.dsbe.Contract.user:

Field **Contract.user**
=======================





Type: ForeignKey

   
.. index::
   single: field;reminder_date
   
.. _dsbe.dsbe.Contract.reminder_date:

Field **Contract.reminder_date**
================================





Type: DateField

   
.. index::
   single: field;reminder_text
   
.. _dsbe.dsbe.Contract.reminder_text:

Field **Contract.reminder_text**
================================





Type: CharField

   
.. index::
   single: field;delay_value
   
.. _dsbe.dsbe.Contract.delay_value:

Field **Contract.delay_value**
==============================





Type: IntegerField

   
.. index::
   single: field;delay_type
   
.. _dsbe.dsbe.Contract.delay_type:

Field **Contract.delay_type**
=============================





Type: CharField

   
.. index::
   single: field;must_build
   
.. _dsbe.dsbe.Contract.must_build:

Field **Contract.must_build**
=============================





Type: BooleanField

   
.. index::
   single: field;person
   
.. _dsbe.dsbe.Contract.person:

Field **Contract.person**
=========================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _dsbe.dsbe.Contract.company:

Field **Contract.company**
==========================





Type: ForeignKey

   
.. index::
   single: field;contact
   
.. _dsbe.dsbe.Contract.contact:

Field **Contract.contact**
==========================





Type: ForeignKey

   
.. index::
   single: field;language
   
.. _dsbe.dsbe.Contract.language:

Field **Contract.language**
===========================





Type: LanguageField

   
.. index::
   single: field;type
   
.. _dsbe.dsbe.Contract.type:

Field **Contract.type**
=======================





Type: ForeignKey

   
.. index::
   single: field;applies_from
   
.. _dsbe.dsbe.Contract.applies_from:

Field **Contract.applies_from**
===============================





Type: DateField

   
.. index::
   single: field;applies_until
   
.. _dsbe.dsbe.Contract.applies_until:

Field **Contract.applies_until**
================================





Type: DateField

   
.. index::
   single: field;date_decided
   
.. _dsbe.dsbe.Contract.date_decided:

Field **Contract.date_decided**
===============================





Type: DateField

   
.. index::
   single: field;date_issued
   
.. _dsbe.dsbe.Contract.date_issued:

Field **Contract.date_issued**
==============================





Type: DateField

   
.. index::
   single: field;duration
   
.. _dsbe.dsbe.Contract.duration:

Field **Contract.duration**
===========================





Type: IntegerField

   
.. index::
   single: field;regime
   
.. _dsbe.dsbe.Contract.regime:

Field **Contract.regime**
=========================





Type: CharField

   
.. index::
   single: field;schedule
   
.. _dsbe.dsbe.Contract.schedule:

Field **Contract.schedule**
===========================





Type: CharField

   
.. index::
   single: field;hourly_rate
   
.. _dsbe.dsbe.Contract.hourly_rate:

Field **Contract.hourly_rate**
==============================





Type: PriceField

   
.. index::
   single: field;refund_rate
   
.. _dsbe.dsbe.Contract.refund_rate:

Field **Contract.refund_rate**
==============================





Type: CharField

   
.. index::
   single: field;reference_person
   
.. _dsbe.dsbe.Contract.reference_person:

Field **Contract.reference_person**
===================================





Type: CharField

   
.. index::
   single: field;responsibilities
   
.. _dsbe.dsbe.Contract.responsibilities:

Field **Contract.responsibilities**
===================================





Type: TextField

   
.. index::
   single: field;stages
   
.. _dsbe.dsbe.Contract.stages:

Field **Contract.stages**
=========================





Type: HtmlTextField

   
.. index::
   single: field;goals
   
.. _dsbe.dsbe.Contract.goals:

Field **Contract.goals**
========================





Type: HtmlTextField

   
.. index::
   single: field;duties_asd
   
.. _dsbe.dsbe.Contract.duties_asd:

Field **Contract.duties_asd**
=============================





Type: HtmlTextField

   
.. index::
   single: field;duties_dsbe
   
.. _dsbe.dsbe.Contract.duties_dsbe:

Field **Contract.duties_dsbe**
==============================





Type: HtmlTextField

   
.. index::
   single: field;duties_company
   
.. _dsbe.dsbe.Contract.duties_company:

Field **Contract.duties_company**
=================================





Type: HtmlTextField

   
.. index::
   single: field;user_asd
   
.. _dsbe.dsbe.Contract.user_asd:

Field **Contract.user_asd**
===========================





Type: ForeignKey

   
.. index::
   single: field;exam_policy
   
.. _dsbe.dsbe.Contract.exam_policy:

Field **Contract.exam_policy**
==============================





Type: ForeignKey

   
.. index::
   single: field;ending
   
.. _dsbe.dsbe.Contract.ending:

Field **Contract.ending**
=========================





Type: ForeignKey

   
.. index::
   single: field;date_ended
   
.. _dsbe.dsbe.Contract.date_ended:

Field **Contract.date_ended**
=============================





Type: DateField

   


.. index::
   pair: model; CourseProvider

.. _dsbe.dsbe.CourseProvider:

------------------------
Model **CourseProvider**
------------------------



Kursanbieter (KAP, Oikos, Lupe, ...) 
    
  
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
company_ptr   OneToOneField company ptr                 
============= ============= ============================

    
Defined in :srcref:`/lino/sites/dsbe/models.py`

.. index::
   single: field;name
   
.. _dsbe.dsbe.CourseProvider.name:

Field **CourseProvider.name**
=============================





Type: CharField

   
.. index::
   single: field;addr1
   
.. _dsbe.dsbe.CourseProvider.addr1:

Field **CourseProvider.addr1**
==============================



Address line before street

Type: CharField

   
.. index::
   single: field;street
   
.. _dsbe.dsbe.CourseProvider.street:

Field **CourseProvider.street**
===============================



Name of street. Without house number.

Type: CharField

   
.. index::
   single: field;street_no
   
.. _dsbe.dsbe.CourseProvider.street_no:

Field **CourseProvider.street_no**
==================================



House number

Type: CharField

   
.. index::
   single: field;street_box
   
.. _dsbe.dsbe.CourseProvider.street_box:

Field **CourseProvider.street_box**
===================================



Text to print after :attr:`steet_no` on the same line

Type: CharField

   
.. index::
   single: field;addr2
   
.. _dsbe.dsbe.CourseProvider.addr2:

Field **CourseProvider.addr2**
==============================



Address line to print below street line

Type: CharField

   
.. index::
   single: field;country
   
.. _dsbe.dsbe.CourseProvider.country:

Field **CourseProvider.country**
================================



The country where this contact is located.

Type: ForeignKey

   
.. index::
   single: field;city
   
.. _dsbe.dsbe.CourseProvider.city:

Field **CourseProvider.city**
=============================




        The city where this contact is located.
        The list of choices for this field is context-sensitive
        and depends on the :attr:`country`.
        

Type: ForeignKey

   
.. index::
   single: field;zip_code
   
.. _dsbe.dsbe.CourseProvider.zip_code:

Field **CourseProvider.zip_code**
=================================





Type: CharField

   
.. index::
   single: field;region
   
.. _dsbe.dsbe.CourseProvider.region:

Field **CourseProvider.region**
===============================





Type: CharField

   
.. index::
   single: field;language
   
.. _dsbe.dsbe.CourseProvider.language:

Field **CourseProvider.language**
=================================





Type: LanguageField

   
.. index::
   single: field;email
   
.. _dsbe.dsbe.CourseProvider.email:

Field **CourseProvider.email**
==============================





Type: EmailField

   
.. index::
   single: field;url
   
.. _dsbe.dsbe.CourseProvider.url:

Field **CourseProvider.url**
============================





Type: URLField

   
.. index::
   single: field;phone
   
.. _dsbe.dsbe.CourseProvider.phone:

Field **CourseProvider.phone**
==============================





Type: CharField

   
.. index::
   single: field;gsm
   
.. _dsbe.dsbe.CourseProvider.gsm:

Field **CourseProvider.gsm**
============================





Type: CharField

   
.. index::
   single: field;fax
   
.. _dsbe.dsbe.CourseProvider.fax:

Field **CourseProvider.fax**
============================





Type: CharField

   
.. index::
   single: field;remarks
   
.. _dsbe.dsbe.CourseProvider.remarks:

Field **CourseProvider.remarks**
================================





Type: TextField

   
.. index::
   single: field;vat_id
   
.. _dsbe.dsbe.CourseProvider.vat_id:

Field **CourseProvider.vat_id**
===============================





Type: CharField

   
.. index::
   single: field;type
   
.. _dsbe.dsbe.CourseProvider.type:

Field **CourseProvider.type**
=============================





Type: ForeignKey

   
.. index::
   single: field;id
   
.. _dsbe.dsbe.CourseProvider.id:

Field **CourseProvider.id**
===========================





Type: AutoField

   
.. index::
   single: field;is_active
   
.. _dsbe.dsbe.CourseProvider.is_active:

Field **CourseProvider.is_active**
==================================





Type: BooleanField

   
.. index::
   single: field;activity
   
.. _dsbe.dsbe.CourseProvider.activity:

Field **CourseProvider.activity**
=================================





Type: ForeignKey

   
.. index::
   single: field;bank_account1
   
.. _dsbe.dsbe.CourseProvider.bank_account1:

Field **CourseProvider.bank_account1**
======================================





Type: CharField

   
.. index::
   single: field;bank_account2
   
.. _dsbe.dsbe.CourseProvider.bank_account2:

Field **CourseProvider.bank_account2**
======================================





Type: CharField

   
.. index::
   single: field;prefix
   
.. _dsbe.dsbe.CourseProvider.prefix:

Field **CourseProvider.prefix**
===============================





Type: CharField

   
.. index::
   single: field;hourly_rate
   
.. _dsbe.dsbe.CourseProvider.hourly_rate:

Field **CourseProvider.hourly_rate**
====================================





Type: PriceField

   
.. index::
   single: field;company_ptr
   
.. _dsbe.dsbe.CourseProvider.company_ptr:

Field **CourseProvider.company_ptr**
====================================





Type: OneToOneField

   


.. index::
   pair: model; CourseContent

.. _dsbe.dsbe.CourseContent:

-----------------------
Model **CourseContent**
-----------------------




Ein Kursinhalt (z.B. "Französisch", "Deutsch", "Alphabétisation",...)

  
==== ========= ============
name type      verbose name
==== ========= ============
id   AutoField ID          
name CharField Name        
==== ========= ============

    
Defined in :srcref:`/lino/sites/dsbe/models.py`

.. index::
   single: field;id
   
.. _dsbe.dsbe.CourseContent.id:

Field **CourseContent.id**
==========================





Type: AutoField

   
.. index::
   single: field;name
   
.. _dsbe.dsbe.CourseContent.name:

Field **CourseContent.name**
============================





Type: CharField

   


.. index::
   pair: model; Course

.. _dsbe.dsbe.Course:

----------------
Model **Course**
----------------




Ein konkreter Kurs, der an einem bestimmten Datum beginnt 
und bei einem bestimmten 
:class:`Kursanbieter <CourseProvider>` stattfindet
(und für den ihr Kandidaten zu vermitteln plant).

  
========== ========== ==============================
name       type       verbose name                  
========== ========== ==============================
id         AutoField  ID                            
title      CharField  Name                          
content    ForeignKey Course content (Kursinhalt)   
provider   ForeignKey Course provider (Kursanbieter)
start_date DateField  start date (beginnt am)       
remark     CharField  Remark (Bemerkung)            
========== ========== ==============================

    
Defined in :srcref:`/lino/sites/dsbe/models.py`

.. index::
   single: field;id
   
.. _dsbe.dsbe.Course.id:

Field **Course.id**
===================





Type: AutoField

   
.. index::
   single: field;title
   
.. _dsbe.dsbe.Course.title:

Field **Course.title**
======================





Type: CharField

   
.. index::
   single: field;content
   
.. _dsbe.dsbe.Course.content:

Field **Course.content**
========================





Type: ForeignKey

   
.. index::
   single: field;provider
   
.. _dsbe.dsbe.Course.provider:

Field **Course.provider**
=========================





Type: ForeignKey

   
.. index::
   single: field;start_date
   
.. _dsbe.dsbe.Course.start_date:

Field **Course.start_date**
===========================





Type: DateField

   
.. index::
   single: field;remark
   
.. _dsbe.dsbe.Course.remark:

Field **Course.remark**
=======================





Type: CharField

   


.. index::
   pair: model; CourseRequest

.. _dsbe.dsbe.CourseRequest:

-----------------------
Model **CourseRequest**
-----------------------




A Course Request is created when a certain Person expresses her 
wish to participate in a Course with a certain CourseContent.

  
============== ========== ================================
name           type       verbose name                    
============== ========== ================================
id             AutoField  ID                              
person         ForeignKey Person                          
content        ForeignKey Course content (Kursinhalt)     
date_submitted DateField  date submitted (eingereicht am )
course         ForeignKey Course found (Kurs gefunden)    
remark         CharField  Remark (Bemerkung)              
date_ended     DateField  date ended (Beendet am)         
ending         ForeignKey Ending (Beendigung)             
============== ========== ================================

    
Defined in :srcref:`/lino/sites/dsbe/models.py`

.. index::
   single: field;id
   
.. _dsbe.dsbe.CourseRequest.id:

Field **CourseRequest.id**
==========================





Type: AutoField

   
.. index::
   single: field;person
   
.. _dsbe.dsbe.CourseRequest.person:

Field **CourseRequest.person**
==============================





Type: ForeignKey

   
.. index::
   single: field;content
   
.. _dsbe.dsbe.CourseRequest.content:

Field **CourseRequest.content**
===============================





Type: ForeignKey

   
.. index::
   single: field;date_submitted
   
.. _dsbe.dsbe.CourseRequest.date_submitted:

Field **CourseRequest.date_submitted**
======================================





Type: DateField

   
.. index::
   single: field;course
   
.. _dsbe.dsbe.CourseRequest.course:

Field **CourseRequest.course**
==============================





Type: ForeignKey

   
.. index::
   single: field;remark
   
.. _dsbe.dsbe.CourseRequest.remark:

Field **CourseRequest.remark**
==============================





Type: CharField

   
.. index::
   single: field;date_ended
   
.. _dsbe.dsbe.CourseRequest.date_ended:

Field **CourseRequest.date_ended**
==================================





Type: DateField

   
.. index::
   single: field;ending
   
.. _dsbe.dsbe.CourseRequest.ending:

Field **CourseRequest.ending**
==============================





Type: ForeignKey

   


.. index::
   pair: model; PersonSearch

.. _dsbe.dsbe.PersonSearch:

----------------------
Model **PersonSearch**
----------------------



PersonSearch(id, user_id, title, aged_from, aged_to, sex, only_my_persons)
  
=============== ============ =================================
name            type         verbose name                     
=============== ============ =================================
id              AutoField    ID                               
user            ForeignKey   user (Benutzer)                  
title           CharField    Search Title (Titel Suchliste)   
aged_from       IntegerField Aged from (Alter von)            
aged_to         IntegerField Aged to (Alter bis)              
sex             CharField    Sex (Geschlecht)                 
only_my_persons BooleanField Only my persons (nur meine Leute)
=============== ============ =================================

    
Defined in :srcref:`/lino/sites/dsbe/models.py`

.. index::
   single: field;id
   
.. _dsbe.dsbe.PersonSearch.id:

Field **PersonSearch.id**
=========================





Type: AutoField

   
.. index::
   single: field;user
   
.. _dsbe.dsbe.PersonSearch.user:

Field **PersonSearch.user**
===========================





Type: ForeignKey

   
.. index::
   single: field;title
   
.. _dsbe.dsbe.PersonSearch.title:

Field **PersonSearch.title**
============================





Type: CharField

   
.. index::
   single: field;aged_from
   
.. _dsbe.dsbe.PersonSearch.aged_from:

Field **PersonSearch.aged_from**
================================





Type: IntegerField

   
.. index::
   single: field;aged_to
   
.. _dsbe.dsbe.PersonSearch.aged_to:

Field **PersonSearch.aged_to**
==============================





Type: IntegerField

   
.. index::
   single: field;sex
   
.. _dsbe.dsbe.PersonSearch.sex:

Field **PersonSearch.sex**
==========================





Type: CharField

   
.. index::
   single: field;only_my_persons
   
.. _dsbe.dsbe.PersonSearch.only_my_persons:

Field **PersonSearch.only_my_persons**
======================================





Type: BooleanField

   


.. index::
   pair: model; WantedLanguageKnowledge

.. _dsbe.dsbe.WantedLanguageKnowledge:

---------------------------------
Model **WantedLanguageKnowledge**
---------------------------------



WantedLanguageKnowledge(id, search_id, language_id, spoken, written)
  
======== =============== ==================
name     type            verbose name      
======== =============== ==================
id       AutoField       ID                
search   ForeignKey      search            
language ForeignKey      Language (Sprache)
spoken   ChoiceListField spoken (Wort)     
written  ChoiceListField written (Schrift) 
======== =============== ==================

    
Defined in :srcref:`/lino/sites/dsbe/models.py`

.. index::
   single: field;id
   
.. _dsbe.dsbe.WantedLanguageKnowledge.id:

Field **WantedLanguageKnowledge.id**
====================================





Type: AutoField

   
.. index::
   single: field;search
   
.. _dsbe.dsbe.WantedLanguageKnowledge.search:

Field **WantedLanguageKnowledge.search**
========================================





Type: ForeignKey

   
.. index::
   single: field;language
   
.. _dsbe.dsbe.WantedLanguageKnowledge.language:

Field **WantedLanguageKnowledge.language**
==========================================





Type: ForeignKey

   
.. index::
   single: field;spoken
   
.. _dsbe.dsbe.WantedLanguageKnowledge.spoken:

Field **WantedLanguageKnowledge.spoken**
========================================





Type: ChoiceListField

   
.. index::
   single: field;written
   
.. _dsbe.dsbe.WantedLanguageKnowledge.written:

Field **WantedLanguageKnowledge.written**
=========================================





Type: ChoiceListField

   


