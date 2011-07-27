=====
notes
=====



.. currentmodule:: notes

Defined in :srcref:`/lino/modlib/notes/models.py`



.. contents:: Table of Contents



.. index::
   pair: model; NoteType

.. _lino.notes.NoteType:

------------------
Model **NoteType**
------------------



NoteType(id, build_method, template, name, important, remark)
  
============ ============ ===========================================================
name         type         verbose name                                               
============ ============ ===========================================================
id           AutoField    ID                                                         
build_method CharField    Build method (Konstruktionsmethode,Méthode de construction)
template     CharField    Template (Vorlage,Modèle)                                  
name         CharField    name                                                       
important    BooleanField important (wichtig)                                        
remark       TextField    Remark (Bemerkung,Remarque)                                
============ ============ ===========================================================

    
Defined in :srcref:`/lino/modlib/notes/models.py`

Referenced from
`lino.notes.Note.type`_



.. index::
   single: field;id
   
.. _lino.notes.NoteType.id:

Field **NoteType.id**
=====================





Type: AutoField

   
.. index::
   single: field;build_method
   
.. _lino.notes.NoteType.build_method:

Field **NoteType.build_method**
===============================





Type: CharField

   
.. index::
   single: field;template
   
.. _lino.notes.NoteType.template:

Field **NoteType.template**
===========================





Type: CharField

   
.. index::
   single: field;name
   
.. _lino.notes.NoteType.name:

Field **NoteType.name**
=======================





Type: CharField

   
.. index::
   single: field;important
   
.. _lino.notes.NoteType.important:

Field **NoteType.important**
============================





Type: BooleanField

   
.. index::
   single: field;remark
   
.. _lino.notes.NoteType.remark:

Field **NoteType.remark**
=========================





Type: TextField

   


.. index::
   pair: model; EventType

.. _lino.notes.EventType:

-------------------
Model **EventType**
-------------------




    
  
======= ============== ======================================
name    type           verbose name                          
======= ============== ======================================
id      AutoField      ID                                    
name    BabelCharField Designation (Beschreibung,Désignation)
remark  TextField      Remark (Bemerkung,Remarque)           
name_fr CharField      Designation (fr)                      
name_nl CharField      Designation (nl)                      
name_en CharField      Designation (en)                      
======= ============== ======================================

    
Defined in :srcref:`/lino/modlib/notes/models.py`

Referenced from
`lino.notes.Note.event_type`_



.. index::
   single: field;id
   
.. _lino.notes.EventType.id:

Field **EventType.id**
======================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.notes.EventType.name:

Field **EventType.name**
========================





Type: BabelCharField

   
.. index::
   single: field;remark
   
.. _lino.notes.EventType.remark:

Field **EventType.remark**
==========================





Type: TextField

   
.. index::
   single: field;name_fr
   
.. _lino.notes.EventType.name_fr:

Field **EventType.name_fr**
===========================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _lino.notes.EventType.name_nl:

Field **EventType.name_nl**
===========================





Type: CharField

   
.. index::
   single: field;name_en
   
.. _lino.notes.EventType.name_en:

Field **EventType.name_en**
===========================





Type: CharField

   


.. index::
   pair: model; Note

.. _lino.notes.Note:

--------------
Model **Note**
--------------



Note(id, user_id, must_build, person_id, company_id, date, type_id, event_type_id, subject, body, language)
  
========== ============= ======================================================================
name       type          verbose name                                                          
========== ============= ======================================================================
id         AutoField     ID                                                                    
user       ForeignKey    user (Benutzer,utilisateur)                                           
must_build BooleanField  must build (muss generiert werden,doit être construit)                
person     ForeignKey    Person (Personne)                                                     
company    ForeignKey    Company (Firma,Société)                                               
date       DateField     Date (Datum)                                                          
type       ForeignKey    Note Type (Form) (Notizart (Form),Type de note (Formulaire))          
event_type ForeignKey    Event Type (Content) (Ereignisart (Inhalt),Type d'événement (contenu))
subject    CharField     Subject (Betreff,Objet)                                               
body       RichTextField Body (Inhalt,Corps)                                                   
language   LanguageField Language (Sprache,Langue)                                             
========== ============= ======================================================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.notes.Note.id:

Field **Note.id**
=================





Type: AutoField

   
.. index::
   single: field;user
   
.. _lino.notes.Note.user:

Field **Note.user**
===================





Type: ForeignKey

   
.. index::
   single: field;must_build
   
.. _lino.notes.Note.must_build:

Field **Note.must_build**
=========================





Type: BooleanField

   
.. index::
   single: field;person
   
.. _lino.notes.Note.person:

Field **Note.person**
=====================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _lino.notes.Note.company:

Field **Note.company**
======================





Type: ForeignKey

   
.. index::
   single: field;date
   
.. _lino.notes.Note.date:

Field **Note.date**
===================





Type: DateField

   
.. index::
   single: field;type
   
.. _lino.notes.Note.type:

Field **Note.type**
===================





Type: ForeignKey

   
.. index::
   single: field;event_type
   
.. _lino.notes.Note.event_type:

Field **Note.event_type**
=========================





Type: ForeignKey

   
.. index::
   single: field;subject
   
.. _lino.notes.Note.subject:

Field **Note.subject**
======================





Type: CharField

   
.. index::
   single: field;body
   
.. _lino.notes.Note.body:

Field **Note.body**
===================





Type: RichTextField

   
.. index::
   single: field;language
   
.. _lino.notes.Note.language:

Field **Note.language**
=======================





Type: LanguageField

   


