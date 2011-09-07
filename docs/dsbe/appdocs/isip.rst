====
isip
====



.. currentmodule:: isip

Defined in :srcref:`/lino/modlib/isip/models.py`


See also :doc:`/dsbe/models`.



.. contents:: Table of Contents



.. index::
   pair: model; ContractType

.. _lino.isip.ContractType:

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

    
Defined in :srcref:`/lino/modlib/isip/models.py`

Referenced from
`lino.isip.Contract.type`_



.. index::
   single: field;id
   
.. _lino.isip.ContractType.id:

Field **ContractType.id**
=========================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.isip.ContractType.name:

Field **ContractType.name**
===========================





Type: BabelCharField

   
.. index::
   single: field;build_method
   
.. _lino.isip.ContractType.build_method:

Field **ContractType.build_method**
===================================





Type: CharField

   
.. index::
   single: field;template
   
.. _lino.isip.ContractType.template:

Field **ContractType.template**
===============================





Type: CharField

   
.. index::
   single: field;ref
   
.. _lino.isip.ContractType.ref:

Field **ContractType.ref**
==========================





Type: CharField

   
.. index::
   single: field;name_fr
   
.. _lino.isip.ContractType.name_fr:

Field **ContractType.name_fr**
==============================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _lino.isip.ContractType.name_nl:

Field **ContractType.name_nl**
==============================





Type: CharField

   
.. index::
   single: field;name_en
   
.. _lino.isip.ContractType.name_en:

Field **ContractType.name_en**
==============================





Type: CharField

   


.. index::
   pair: model; ExamPolicy

.. _lino.isip.ExamPolicy:

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

    
Defined in :srcref:`/lino/modlib/isip/models.py`

Referenced from
`lino.jobs.Contract.exam_policy`_, `lino.isip.Contract.exam_policy`_



.. index::
   single: field;id
   
.. _lino.isip.ExamPolicy.id:

Field **ExamPolicy.id**
=======================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.isip.ExamPolicy.name:

Field **ExamPolicy.name**
=========================





Type: BabelCharField

   
.. index::
   single: field;name_fr
   
.. _lino.isip.ExamPolicy.name_fr:

Field **ExamPolicy.name_fr**
============================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _lino.isip.ExamPolicy.name_nl:

Field **ExamPolicy.name_nl**
============================





Type: CharField

   
.. index::
   single: field;name_en
   
.. _lino.isip.ExamPolicy.name_en:

Field **ExamPolicy.name_en**
============================





Type: CharField

   


.. index::
   pair: model; ContractEnding

.. _lino.isip.ContractEnding:

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

    
Defined in :srcref:`/lino/modlib/isip/models.py`

Referenced from
`lino.jobs.Contract.ending`_, `lino.isip.Contract.ending`_



.. index::
   single: field;id
   
.. _lino.isip.ContractEnding.id:

Field **ContractEnding.id**
===========================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.isip.ContractEnding.name:

Field **ContractEnding.name**
=============================





Type: CharField

   


.. index::
   pair: model; Contract

.. _lino.isip.Contract:

------------------
Model **Contract**
------------------



Contract(id, user_id, must_build, person_id, contact_id, language, applies_from, applies_until, date_decided, date_issued, user_asd_id, exam_policy_id, ending_id, date_ended, type_id, company_id, stages, goals, duties_asd, duties_dsbe, duties_company, duties_person)
  
============== ============= ============================================================
name           type          verbose name                                                
============== ============= ============================================================
id             AutoField     ID                                                          
user           ForeignKey    User (Benutzer,Utilisateur)                                 
must_build     BooleanField  must build (muss generiert werden,doit être construit)      
person         ForeignKey    Person (Personne)                                           
contact        ForeignKey    represented by (Vertreten durch)                            
language       LanguageField Language (Sprache,Langue)                                   
applies_from   DateField     applies from (Laufzeit von,est d'application à partir de)   
applies_until  DateField     applies until (Laufzeit bis,est d'application jusque)       
date_decided   DateField     date decided (Beschlossen am,date de décision)              
date_issued    DateField     date issued (Ausgestellt am,date fournie ?)                 
user_asd       ForeignKey    responsible (ASD) (Verantwortlicher (ASD),Responsable (SSG))
exam_policy    ForeignKey    examination policy (Auswertungsstrategie,Politique d'examen)
ending         ForeignKey    Ending (Beendigung,Fin)                                     
date_ended     DateField     date ended (Beendet am,date de fin)                         
type           ForeignKey    Contract Type (Vertragsart,Type de contrat)                 
company        ForeignKey    Company (Firma,Société)                                     
stages         RichTextField stages (Etappen)                                            
goals          RichTextField goals (Zielsetzungen,buts)                                  
duties_asd     RichTextField duties ASD (Verpflichtungen ASD,devoirs SSG)                
duties_dsbe    RichTextField duties DSBE (Verpflichtungen DSBE,devois ISP)               
duties_company RichTextField duties company (Verpflichtungen Firma,devoirs entreprise)   
duties_person  RichTextField duties person (Verpflichtungen Person,Devoirs personne)     
============== ============= ============================================================

    
Defined in :srcref:`/lino/modlib/isip/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.isip.Contract.id:

Field **Contract.id**
=====================





Type: AutoField

   
.. index::
   single: field;user
   
.. _lino.isip.Contract.user:

Field **Contract.user**
=======================





Type: ForeignKey

   
.. index::
   single: field;must_build
   
.. _lino.isip.Contract.must_build:

Field **Contract.must_build**
=============================





Type: BooleanField

   
.. index::
   single: field;person
   
.. _lino.isip.Contract.person:

Field **Contract.person**
=========================





Type: ForeignKey

   
.. index::
   single: field;contact
   
.. _lino.isip.Contract.contact:

Field **Contract.contact**
==========================





Type: ForeignKey

   
.. index::
   single: field;language
   
.. _lino.isip.Contract.language:

Field **Contract.language**
===========================





Type: LanguageField

   
.. index::
   single: field;applies_from
   
.. _lino.isip.Contract.applies_from:

Field **Contract.applies_from**
===============================





Type: DateField

   
.. index::
   single: field;applies_until
   
.. _lino.isip.Contract.applies_until:

Field **Contract.applies_until**
================================





Type: DateField

   
.. index::
   single: field;date_decided
   
.. _lino.isip.Contract.date_decided:

Field **Contract.date_decided**
===============================





Type: DateField

   
.. index::
   single: field;date_issued
   
.. _lino.isip.Contract.date_issued:

Field **Contract.date_issued**
==============================





Type: DateField

   
.. index::
   single: field;user_asd
   
.. _lino.isip.Contract.user_asd:

Field **Contract.user_asd**
===========================





Type: ForeignKey

   
.. index::
   single: field;exam_policy
   
.. _lino.isip.Contract.exam_policy:

Field **Contract.exam_policy**
==============================





Type: ForeignKey

   
.. index::
   single: field;ending
   
.. _lino.isip.Contract.ending:

Field **Contract.ending**
=========================





Type: ForeignKey

   
.. index::
   single: field;date_ended
   
.. _lino.isip.Contract.date_ended:

Field **Contract.date_ended**
=============================





Type: DateField

   
.. index::
   single: field;type
   
.. _lino.isip.Contract.type:

Field **Contract.type**
=======================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _lino.isip.Contract.company:

Field **Contract.company**
==========================





Type: ForeignKey

   
.. index::
   single: field;stages
   
.. _lino.isip.Contract.stages:

Field **Contract.stages**
=========================





Type: RichTextField

   
.. index::
   single: field;goals
   
.. _lino.isip.Contract.goals:

Field **Contract.goals**
========================





Type: RichTextField

   
.. index::
   single: field;duties_asd
   
.. _lino.isip.Contract.duties_asd:

Field **Contract.duties_asd**
=============================





Type: RichTextField

   
.. index::
   single: field;duties_dsbe
   
.. _lino.isip.Contract.duties_dsbe:

Field **Contract.duties_dsbe**
==============================





Type: RichTextField

   
.. index::
   single: field;duties_company
   
.. _lino.isip.Contract.duties_company:

Field **Contract.duties_company**
=================================





Type: RichTextField

   
.. index::
   single: field;duties_person
   
.. _lino.isip.Contract.duties_person:

Field **Contract.duties_person**
================================





Type: RichTextField

   


