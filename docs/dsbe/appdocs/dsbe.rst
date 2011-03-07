====
dsbe
====



.. currentmodule:: dsbe

Defined in :srcref:`/lino/sites/dsbe/models.py`


See also :doc:`/dsbe/models`




.. index::
   pair: model; PersonGroup
   single: field;id
   single: field;name

.. _dsbe.dsbe.PersonGroup:

---------------------
Model ``PersonGroup``
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
   pair: model; StudyType
   single: field;id
   single: field;name

.. _dsbe.dsbe.StudyType:

-------------------
Model ``StudyType``
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
   pair: model; Study
   single: field;id
   single: field;person
   single: field;type
   single: field;content
   single: field;started
   single: field;stopped
   single: field;success
   single: field;country
   single: field;city
   single: field;language
   single: field;school
   single: field;remarks

.. _dsbe.dsbe.Study:

---------------
Model ``Study``
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
   pair: model; LanguageKnowledge
   single: field;id
   single: field;person
   single: field;language
   single: field;spoken
   single: field;written

.. _dsbe.dsbe.LanguageKnowledge:

---------------------------
Model ``LanguageKnowledge``
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
   pair: model; JobExperience
   single: field;id
   single: field;person
   single: field;company
   single: field;title
   single: field;country
   single: field;started
   single: field;stopped
   single: field;remarks

.. _dsbe.dsbe.JobExperience:

-----------------------
Model ``JobExperience``
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
   pair: model; Activity
   single: field;id
   single: field;name
   single: field;lst104

.. _dsbe.dsbe.Activity:

------------------
Model ``Activity``
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
   pair: model; ExclusionType
   single: field;id
   single: field;name

.. _dsbe.dsbe.ExclusionType:

-----------------------
Model ``ExclusionType``
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
   pair: model; Exclusion
   single: field;id
   single: field;person
   single: field;type
   single: field;excluded_from
   single: field;excluded_until
   single: field;remark

.. _dsbe.dsbe.Exclusion:

-------------------
Model ``Exclusion``
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
   pair: model; ContractType
   single: field;id
   single: field;build_method
   single: field;template
   single: field;ref
   single: field;name
   single: field;name_fr
   single: field;name_nl
   single: field;name_en

.. _dsbe.dsbe.ContractType:

----------------------
Model ``ContractType``
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
   pair: model; ExamPolicy
   single: field;id
   single: field;name
   single: field;name_fr
   single: field;name_nl
   single: field;name_en

.. _dsbe.dsbe.ExamPolicy:

--------------------
Model ``ExamPolicy``
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
   pair: model; ContractEnding
   single: field;id
   single: field;name

.. _dsbe.dsbe.ContractEnding:

------------------------
Model ``ContractEnding``
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
   pair: model; CourseEnding
   single: field;id
   single: field;name

.. _dsbe.dsbe.CourseEnding:

----------------------
Model ``CourseEnding``
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
   pair: model; AidType
   single: field;id
   single: field;name
   single: field;name_fr
   single: field;name_nl
   single: field;name_en

.. _dsbe.dsbe.AidType:

-----------------
Model ``AidType``
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
   pair: model; Contract
   single: field;id
   single: field;user
   single: field;reminder_date
   single: field;reminder_text
   single: field;delay_value
   single: field;delay_type
   single: field;must_build
   single: field;person
   single: field;company
   single: field;contact
   single: field;language
   single: field;type
   single: field;applies_from
   single: field;applies_until
   single: field;date_decided
   single: field;date_issued
   single: field;duration
   single: field;regime
   single: field;schedule
   single: field;hourly_rate
   single: field;refund_rate
   single: field;reference_person
   single: field;responsibilities
   single: field;stages
   single: field;goals
   single: field;duties_asd
   single: field;duties_dsbe
   single: field;duties_company
   single: field;user_asd
   single: field;exam_policy
   single: field;ending
   single: field;date_ended

.. _dsbe.dsbe.Contract:

------------------
Model ``Contract``
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
   pair: model; CourseProvider
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
   single: field;company_ptr

.. _dsbe.dsbe.CourseProvider:

------------------------
Model ``CourseProvider``
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
   pair: model; CourseContent
   single: field;id
   single: field;name

.. _dsbe.dsbe.CourseContent:

-----------------------
Model ``CourseContent``
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
   pair: model; Course
   single: field;id
   single: field;title
   single: field;content
   single: field;provider
   single: field;start_date
   single: field;remark

.. _dsbe.dsbe.Course:

----------------
Model ``Course``
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
   pair: model; CourseRequest
   single: field;id
   single: field;person
   single: field;content
   single: field;date_submitted
   single: field;course
   single: field;remark
   single: field;date_ended
   single: field;ending

.. _dsbe.dsbe.CourseRequest:

-----------------------
Model ``CourseRequest``
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
   pair: model; PersonSearch
   single: field;id
   single: field;user
   single: field;title
   single: field;aged_from
   single: field;aged_to
   single: field;sex
   single: field;only_my_persons

.. _dsbe.dsbe.PersonSearch:

----------------------
Model ``PersonSearch``
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
   pair: model; WantedLanguageKnowledge
   single: field;id
   single: field;search
   single: field;language
   single: field;spoken
   single: field;written

.. _dsbe.dsbe.WantedLanguageKnowledge:

---------------------------------
Model ``WantedLanguageKnowledge``
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


