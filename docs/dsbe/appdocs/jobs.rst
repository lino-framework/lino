====
jobs
====



.. currentmodule:: jobs

Defined in :srcref:`/lino/modlib/jobs/models.py`


See also :doc:`/dsbe/models`.



.. contents:: Table of Contents



.. index::
   pair: model; JobProvider

.. _lino.jobs.JobProvider:

---------------------
Model **JobProvider**
---------------------



Stellenanbieter (BISA, BW, ...) 
    
  
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
contact_ptr   OneToOneField contact ptr                                                                  
vat_id        CharField     VAT id (MWSt.-Nr.,N° de TVA)                                                 
type          ForeignKey    Company type (Firmenart,Type de société)                                     
is_active     BooleanField  is active (aktiv,est actif)                                                  
activity      ForeignKey    Activity (Beruf,Activité)                                                    
bank_account1 CharField     Bank account 1 (Bankkonto 1,Compte en banque 1)                              
bank_account2 CharField     Bank account 2 (Bankkonto 2,Compte en banque 2)                              
prefix        CharField     prefix                                                                       
hourly_rate   PriceField    hourly rate (Stundensatz,coûr horaire)                                       
company_ptr   OneToOneField company ptr                                                                  
============= ============= =============================================================================

    
Defined in :srcref:`/lino/modlib/jobs/models.py`

Referenced from
`lino.jobs.Contract.provider`_, `lino.jobs.Job.provider`_



.. index::
   single: field;id
   
.. _lino.jobs.JobProvider.id:

Field **JobProvider.id**
========================





Type: AutoField

   
.. index::
   single: field;country
   
.. _lino.jobs.JobProvider.country:

Field **JobProvider.country**
=============================





Type: ForeignKey

   
.. index::
   single: field;city
   
.. _lino.jobs.JobProvider.city:

Field **JobProvider.city**
==========================





Type: ForeignKey

   
.. index::
   single: field;name
   
.. _lino.jobs.JobProvider.name:

Field **JobProvider.name**
==========================





Type: CharField

   
.. index::
   single: field;addr1
   
.. _lino.jobs.JobProvider.addr1:

Field **JobProvider.addr1**
===========================



Address line before street

Type: CharField

   
.. index::
   single: field;street_prefix
   
.. _lino.jobs.JobProvider.street_prefix:

Field **JobProvider.street_prefix**
===================================



Text to print before name of street, but to ignore for sorting.

Type: CharField

   
.. index::
   single: field;street
   
.. _lino.jobs.JobProvider.street:

Field **JobProvider.street**
============================



Name of street. Without house number.

Type: CharField

   
.. index::
   single: field;street_no
   
.. _lino.jobs.JobProvider.street_no:

Field **JobProvider.street_no**
===============================



House number

Type: CharField

   
.. index::
   single: field;street_box
   
.. _lino.jobs.JobProvider.street_box:

Field **JobProvider.street_box**
================================



Text to print after :attr:`steet_no` on the same line

Type: CharField

   
.. index::
   single: field;addr2
   
.. _lino.jobs.JobProvider.addr2:

Field **JobProvider.addr2**
===========================



Address line to print below street line

Type: CharField

   
.. index::
   single: field;zip_code
   
.. _lino.jobs.JobProvider.zip_code:

Field **JobProvider.zip_code**
==============================





Type: CharField

   
.. index::
   single: field;region
   
.. _lino.jobs.JobProvider.region:

Field **JobProvider.region**
============================





Type: CharField

   
.. index::
   single: field;language
   
.. _lino.jobs.JobProvider.language:

Field **JobProvider.language**
==============================





Type: LanguageField

   
.. index::
   single: field;email
   
.. _lino.jobs.JobProvider.email:

Field **JobProvider.email**
===========================





Type: EmailField

   
.. index::
   single: field;url
   
.. _lino.jobs.JobProvider.url:

Field **JobProvider.url**
=========================





Type: URLField

   
.. index::
   single: field;phone
   
.. _lino.jobs.JobProvider.phone:

Field **JobProvider.phone**
===========================





Type: CharField

   
.. index::
   single: field;gsm
   
.. _lino.jobs.JobProvider.gsm:

Field **JobProvider.gsm**
=========================





Type: CharField

   
.. index::
   single: field;fax
   
.. _lino.jobs.JobProvider.fax:

Field **JobProvider.fax**
=========================





Type: CharField

   
.. index::
   single: field;remarks
   
.. _lino.jobs.JobProvider.remarks:

Field **JobProvider.remarks**
=============================





Type: TextField

   
.. index::
   single: field;contact_ptr
   
.. _lino.jobs.JobProvider.contact_ptr:

Field **JobProvider.contact_ptr**
=================================





Type: OneToOneField

   
.. index::
   single: field;vat_id
   
.. _lino.jobs.JobProvider.vat_id:

Field **JobProvider.vat_id**
============================





Type: CharField

   
.. index::
   single: field;type
   
.. _lino.jobs.JobProvider.type:

Field **JobProvider.type**
==========================





Type: ForeignKey

   
.. index::
   single: field;is_active
   
.. _lino.jobs.JobProvider.is_active:

Field **JobProvider.is_active**
===============================





Type: BooleanField

   
.. index::
   single: field;activity
   
.. _lino.jobs.JobProvider.activity:

Field **JobProvider.activity**
==============================





Type: ForeignKey

   
.. index::
   single: field;bank_account1
   
.. _lino.jobs.JobProvider.bank_account1:

Field **JobProvider.bank_account1**
===================================





Type: CharField

   
.. index::
   single: field;bank_account2
   
.. _lino.jobs.JobProvider.bank_account2:

Field **JobProvider.bank_account2**
===================================





Type: CharField

   
.. index::
   single: field;prefix
   
.. _lino.jobs.JobProvider.prefix:

Field **JobProvider.prefix**
============================





Type: CharField

   
.. index::
   single: field;hourly_rate
   
.. _lino.jobs.JobProvider.hourly_rate:

Field **JobProvider.hourly_rate**
=================================





Type: PriceField

   
.. index::
   single: field;company_ptr
   
.. _lino.jobs.JobProvider.company_ptr:

Field **JobProvider.company_ptr**
=================================





Type: OneToOneField

   


.. index::
   pair: model; ContractType

.. _lino.jobs.ContractType:

----------------------
Model **ContractType**
----------------------



ContractType(id, name, build_method, template, ref, name_fr, name_nl, name_en)
  
============ ============== ===========================================================
name         type           verbose name                                               
============ ============== ===========================================================
id           AutoField      ID                                                         
name         BabelCharField Designation (Beschreibung,Désignation)                     
build_method CharField      Build method (Konstruktionsmethode,Méthode de construction)
template     CharField      Template (Vorlage,Modèle)                                  
ref          CharField      reference (Referenz,référence)                             
name_fr      CharField      Designation (fr)                                           
name_nl      CharField      Designation (nl)                                           
name_en      CharField      Designation (en)                                           
============ ============== ===========================================================

    
Defined in :srcref:`/lino/modlib/jobs/models.py`

Referenced from
`lino.jobs.Contract.type`_, `lino.jobs.Job.contract_type`_, `lino.jobs.ContractsSituation.contract_type`_



.. index::
   single: field;id
   
.. _lino.jobs.ContractType.id:

Field **ContractType.id**
=========================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.jobs.ContractType.name:

Field **ContractType.name**
===========================





Type: BabelCharField

   
.. index::
   single: field;build_method
   
.. _lino.jobs.ContractType.build_method:

Field **ContractType.build_method**
===================================





Type: CharField

   
.. index::
   single: field;template
   
.. _lino.jobs.ContractType.template:

Field **ContractType.template**
===============================





Type: CharField

   
.. index::
   single: field;ref
   
.. _lino.jobs.ContractType.ref:

Field **ContractType.ref**
==========================





Type: CharField

   
.. index::
   single: field;name_fr
   
.. _lino.jobs.ContractType.name_fr:

Field **ContractType.name_fr**
==============================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _lino.jobs.ContractType.name_nl:

Field **ContractType.name_nl**
==============================





Type: CharField

   
.. index::
   single: field;name_en
   
.. _lino.jobs.ContractType.name_en:

Field **ContractType.name_en**
==============================





Type: CharField

   


.. index::
   pair: model; ExamPolicy

.. _lino.jobs.ExamPolicy:

--------------------
Model **ExamPolicy**
--------------------



ExamPolicy(id, name, name_fr, name_nl, name_en)
  
======= ============== ======================================
name    type           verbose name                          
======= ============== ======================================
id      AutoField      ID                                    
name    BabelCharField Designation (Beschreibung,Désignation)
name_fr CharField      Designation (fr)                      
name_nl CharField      Designation (nl)                      
name_en CharField      Designation (en)                      
======= ============== ======================================

    
Defined in :srcref:`/lino/modlib/jobs/models.py`

Referenced from
`lino.jobs.Contract.exam_policy`_



.. index::
   single: field;id
   
.. _lino.jobs.ExamPolicy.id:

Field **ExamPolicy.id**
=======================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.jobs.ExamPolicy.name:

Field **ExamPolicy.name**
=========================





Type: BabelCharField

   
.. index::
   single: field;name_fr
   
.. _lino.jobs.ExamPolicy.name_fr:

Field **ExamPolicy.name_fr**
============================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _lino.jobs.ExamPolicy.name_nl:

Field **ExamPolicy.name_nl**
============================





Type: CharField

   
.. index::
   single: field;name_en
   
.. _lino.jobs.ExamPolicy.name_en:

Field **ExamPolicy.name_en**
============================





Type: CharField

   


.. index::
   pair: model; ContractEnding

.. _lino.jobs.ContractEnding:

------------------------
Model **ContractEnding**
------------------------



ContractEnding(id, name)
  
==== ========= =====================================
name type      verbose name                         
==== ========= =====================================
id   AutoField ID                                   
name CharField designation (Bezeichnung,désignation)
==== ========= =====================================

    
Defined in :srcref:`/lino/modlib/jobs/models.py`

Referenced from
`lino.jobs.Contract.ending`_



.. index::
   single: field;id
   
.. _lino.jobs.ContractEnding.id:

Field **ContractEnding.id**
===========================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.jobs.ContractEnding.name:

Field **ContractEnding.name**
=============================





Type: CharField

   


.. index::
   pair: model; Contract

.. _lino.jobs.Contract:

------------------
Model **Contract**
------------------




A Contract

  
================ ============= ==============================================================
name             type          verbose name                                                  
================ ============= ==============================================================
id               AutoField     ID                                                            
user             ForeignKey    responsible (DSBE) (Verantwortlicher (DSBE),Responsable (ISP))
must_build       BooleanField  must build (muss generiert werden,doit être construit)        
person           ForeignKey    Person (Personne)                                             
provider         ForeignKey    Job Provider (Stellenanbieter)                                
contact          ForeignKey    represented by (Vertreten durch,représenté par)               
language         LanguageField Language (Sprache,Langue)                                     
job              ForeignKey    Job (Stelle)                                                  
type             ForeignKey    Contract Type (Vertragsart,Type de contrat)                   
applies_from     DateField     applies from (Laufzeit von,est d'application à partir de)     
applies_until    DateField     applies until (Laufzeit bis,est d'application jusque)         
date_decided     DateField     date decided (Beschlossen am,date de décision)                
date_issued      DateField     date issued (Ausgestellt am,date fournie ?)                   
duration         IntegerField  duration (days) (Dauer (Arbeitstage),durée (jours))           
regime           CharField     regime (Regime,régime)                                        
schedule         CharField     schedule (Stundenplan,horaire)                                
hourly_rate      PriceField    hourly rate (Stundensatz,coûr horaire)                        
refund_rate      CharField     refund rate (Rückzahlung,tarif de remboursement)              
reference_person CharField     reference person (Referenzperson,persone de référence)        
responsibilities RichTextField responsibilities (Aufgabenbereich,responsabilités)            
stages           RichTextField stages (Etappen)                                              
goals            RichTextField goals (Zielsetzungen,buts)                                    
duties_asd       RichTextField duties ASD (Verpflichtungen ASD,devoirs SSG)                  
duties_dsbe      RichTextField duties DSBE (Verpflichtungen DSBE,devois ISP)                 
duties_company   RichTextField duties company (Verpflichtungen Firma,devoirs entreprise)     
duties_person    RichTextField duties person (Verpflichtungen Person,Devoirs personne)       
user_asd         ForeignKey    responsible (ASD) (Verantwortlicher (ASD),Responsable (SSG))  
exam_policy      ForeignKey    examination policy (Auswertungsstrategie,Politique d'examen)  
ending           ForeignKey    Ending (Beendigung,Fin)                                       
date_ended       DateField     date ended (Beendet am,date de fin)                           
================ ============= ==============================================================

    
Defined in :srcref:`/lino/modlib/jobs/models.py`

Referenced from
`lino.jobs.JobRequest.contract`_



.. index::
   single: field;id
   
.. _lino.jobs.Contract.id:

Field **Contract.id**
=====================





Type: AutoField

   
.. index::
   single: field;user
   
.. _lino.jobs.Contract.user:

Field **Contract.user**
=======================





Type: ForeignKey

   
.. index::
   single: field;must_build
   
.. _lino.jobs.Contract.must_build:

Field **Contract.must_build**
=============================





Type: BooleanField

   
.. index::
   single: field;person
   
.. _lino.jobs.Contract.person:

Field **Contract.person**
=========================





Type: ForeignKey

   
.. index::
   single: field;provider
   
.. _lino.jobs.Contract.provider:

Field **Contract.provider**
===========================





Type: ForeignKey

   
.. index::
   single: field;contact
   
.. _lino.jobs.Contract.contact:

Field **Contract.contact**
==========================





Type: ForeignKey

   
.. index::
   single: field;language
   
.. _lino.jobs.Contract.language:

Field **Contract.language**
===========================





Type: LanguageField

   
.. index::
   single: field;job
   
.. _lino.jobs.Contract.job:

Field **Contract.job**
======================





Type: ForeignKey

   
.. index::
   single: field;type
   
.. _lino.jobs.Contract.type:

Field **Contract.type**
=======================





Type: ForeignKey

   
.. index::
   single: field;applies_from
   
.. _lino.jobs.Contract.applies_from:

Field **Contract.applies_from**
===============================





Type: DateField

   
.. index::
   single: field;applies_until
   
.. _lino.jobs.Contract.applies_until:

Field **Contract.applies_until**
================================





Type: DateField

   
.. index::
   single: field;date_decided
   
.. _lino.jobs.Contract.date_decided:

Field **Contract.date_decided**
===============================





Type: DateField

   
.. index::
   single: field;date_issued
   
.. _lino.jobs.Contract.date_issued:

Field **Contract.date_issued**
==============================





Type: DateField

   
.. index::
   single: field;duration
   
.. _lino.jobs.Contract.duration:

Field **Contract.duration**
===========================





Type: IntegerField

   
.. index::
   single: field;regime
   
.. _lino.jobs.Contract.regime:

Field **Contract.regime**
=========================





Type: CharField

   
.. index::
   single: field;schedule
   
.. _lino.jobs.Contract.schedule:

Field **Contract.schedule**
===========================





Type: CharField

   
.. index::
   single: field;hourly_rate
   
.. _lino.jobs.Contract.hourly_rate:

Field **Contract.hourly_rate**
==============================





Type: PriceField

   
.. index::
   single: field;refund_rate
   
.. _lino.jobs.Contract.refund_rate:

Field **Contract.refund_rate**
==============================





Type: CharField

   
.. index::
   single: field;reference_person
   
.. _lino.jobs.Contract.reference_person:

Field **Contract.reference_person**
===================================





Type: CharField

   
.. index::
   single: field;responsibilities
   
.. _lino.jobs.Contract.responsibilities:

Field **Contract.responsibilities**
===================================





Type: RichTextField

   
.. index::
   single: field;stages
   
.. _lino.jobs.Contract.stages:

Field **Contract.stages**
=========================





Type: RichTextField

   
.. index::
   single: field;goals
   
.. _lino.jobs.Contract.goals:

Field **Contract.goals**
========================





Type: RichTextField

   
.. index::
   single: field;duties_asd
   
.. _lino.jobs.Contract.duties_asd:

Field **Contract.duties_asd**
=============================





Type: RichTextField

   
.. index::
   single: field;duties_dsbe
   
.. _lino.jobs.Contract.duties_dsbe:

Field **Contract.duties_dsbe**
==============================





Type: RichTextField

   
.. index::
   single: field;duties_company
   
.. _lino.jobs.Contract.duties_company:

Field **Contract.duties_company**
=================================





Type: RichTextField

   
.. index::
   single: field;duties_person
   
.. _lino.jobs.Contract.duties_person:

Field **Contract.duties_person**
================================





Type: RichTextField

   
.. index::
   single: field;user_asd
   
.. _lino.jobs.Contract.user_asd:

Field **Contract.user_asd**
===========================





Type: ForeignKey

   
.. index::
   single: field;exam_policy
   
.. _lino.jobs.Contract.exam_policy:

Field **Contract.exam_policy**
==============================





Type: ForeignKey

   
.. index::
   single: field;ending
   
.. _lino.jobs.Contract.ending:

Field **Contract.ending**
=========================





Type: ForeignKey

   
.. index::
   single: field;date_ended
   
.. _lino.jobs.Contract.date_ended:

Field **Contract.date_ended**
=============================





Type: DateField

   


.. index::
   pair: model; JobType

.. _lino.jobs.JobType:

-----------------
Model **JobType**
-----------------




A work place at some job provider

  
===== ============ ======================================
name  type         verbose name                          
===== ============ ======================================
id    AutoField    ID                                    
seqno IntegerField Seq.No. (Seq.-Nr.,N° de séq)          
name  CharField    Designation (Beschreibung,Désignation)
===== ============ ======================================

    
Defined in :srcref:`/lino/modlib/jobs/models.py`

Referenced from
`lino.jobs.Job.type`_, `lino.jobs.ContractsSituation.job_type`_



.. index::
   single: field;id
   
.. _lino.jobs.JobType.id:

Field **JobType.id**
====================





Type: AutoField

   
.. index::
   single: field;seqno
   
.. _lino.jobs.JobType.seqno:

Field **JobType.seqno**
=======================





Type: IntegerField

   
.. index::
   single: field;name
   
.. _lino.jobs.JobType.name:

Field **JobType.name**
======================





Type: CharField

   


.. index::
   pair: model; Job

.. _lino.jobs.Job:

-------------
Model **Job**
-------------




    
  
============= ============ ===========================================
name          type         verbose name                               
============= ============ ===========================================
id            AutoField    ID                                         
name          CharField    Name (Nom)                                 
type          ForeignKey   Job Type (Stellenart)                      
provider      ForeignKey   Job Provider (Stellenanbieter)             
contract_type ForeignKey   Contract Type (Vertragsart,Type de contrat)
hourly_rate   PriceField   hourly rate (Stundensatz,coûr horaire)     
capacity      IntegerField capacity (Kapazität)                       
remark        CharField    Remark (Bemerkung,Remarque)                
============= ============ ===========================================

    
Defined in :srcref:`/lino/modlib/jobs/models.py`

Referenced from
`lino.jobs.Contract.job`_, `lino.jobs.JobRequest.job`_



.. index::
   single: field;id
   
.. _lino.jobs.Job.id:

Field **Job.id**
================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.jobs.Job.name:

Field **Job.name**
==================





Type: CharField

   
.. index::
   single: field;type
   
.. _lino.jobs.Job.type:

Field **Job.type**
==================





Type: ForeignKey

   
.. index::
   single: field;provider
   
.. _lino.jobs.Job.provider:

Field **Job.provider**
======================





Type: ForeignKey

   
.. index::
   single: field;contract_type
   
.. _lino.jobs.Job.contract_type:

Field **Job.contract_type**
===========================





Type: ForeignKey

   
.. index::
   single: field;hourly_rate
   
.. _lino.jobs.Job.hourly_rate:

Field **Job.hourly_rate**
=========================





Type: PriceField

   
.. index::
   single: field;capacity
   
.. _lino.jobs.Job.capacity:

Field **Job.capacity**
======================





Type: IntegerField

   
.. index::
   single: field;remark
   
.. _lino.jobs.Job.remark:

Field **Job.remark**
====================





Type: CharField

   


.. index::
   pair: model; JobRequest

.. _lino.jobs.JobRequest:

--------------------
Model **JobRequest**
--------------------



JobRequest(id, person_id, job_id, date_submitted, contract_id, remark)
  
============== ========== =============================================
name           type       verbose name                                 
============== ========== =============================================
id             AutoField  ID                                           
person         ForeignKey Person (Personne)                            
job            ForeignKey Requested Job (Angefragte Stelle)            
date_submitted DateField  date submitted (eingereicht am ,date d'envoi)
contract       ForeignKey Contract found (Vertrag)                     
remark         TextField  Remark (Bemerkung,Remarque)                  
============== ========== =============================================

    
Defined in :srcref:`/lino/modlib/jobs/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.jobs.JobRequest.id:

Field **JobRequest.id**
=======================





Type: AutoField

   
.. index::
   single: field;person
   
.. _lino.jobs.JobRequest.person:

Field **JobRequest.person**
===========================





Type: ForeignKey

   
.. index::
   single: field;job
   
.. _lino.jobs.JobRequest.job:

Field **JobRequest.job**
========================





Type: ForeignKey

   
.. index::
   single: field;date_submitted
   
.. _lino.jobs.JobRequest.date_submitted:

Field **JobRequest.date_submitted**
===================================





Type: DateField

   
.. index::
   single: field;contract
   
.. _lino.jobs.JobRequest.contract:

Field **JobRequest.contract**
=============================





Type: ForeignKey

   
.. index::
   single: field;remark
   
.. _lino.jobs.JobRequest.remark:

Field **JobRequest.remark**
===========================





Type: TextField

   


.. index::
   pair: model; ContractsSituation

.. _lino.jobs.ContractsSituation:

----------------------------
Model **ContractsSituation**
----------------------------



ContractsSituation(id, must_build, date, contract_type_id, job_type_id)
  
============= ============ ======================================================
name          type         verbose name                                          
============= ============ ======================================================
id            AutoField    ID                                                    
must_build    BooleanField must build (muss generiert werden,doit être construit)
date          DateField    Date (Datum)                                          
contract_type ForeignKey   contract type (Vertragsart,type de contrat)           
job_type      ForeignKey   job type                                              
============= ============ ======================================================

    
Defined in :srcref:`/lino/modlib/jobs/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.jobs.ContractsSituation.id:

Field **ContractsSituation.id**
===============================





Type: AutoField

   
.. index::
   single: field;must_build
   
.. _lino.jobs.ContractsSituation.must_build:

Field **ContractsSituation.must_build**
=======================================





Type: BooleanField

   
.. index::
   single: field;date
   
.. _lino.jobs.ContractsSituation.date:

Field **ContractsSituation.date**
=================================





Type: DateField

   
.. index::
   single: field;contract_type
   
.. _lino.jobs.ContractsSituation.contract_type:

Field **ContractsSituation.contract_type**
==========================================





Type: ForeignKey

   
.. index::
   single: field;job_type
   
.. _lino.jobs.ContractsSituation.job_type:

Field **ContractsSituation.job_type**
=====================================





Type: ForeignKey

   


