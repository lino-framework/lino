=====
notes
=====



.. currentmodule:: notes

Defined in :srcref:`/lino/modlib/notes/models.py`



.. contents:: Table of Contents



.. index::
   pair: model; NoteType

.. _std.notes.NoteType:

------------------
Model **NoteType**
------------------



NoteType(id, build_method, template, name, important, remark)
  
============ ============ ===========================================================
name         type         verbose name                                               
============ ============ ===========================================================
id           AutoField    ID                                                         
build_method CharField    Build method (Konstruktionsmethode,Methode de construction)
template     CharField    Template (Vorlage,Modèle)                                  
name         CharField    name                                                       
important    BooleanField important (wichtig)                                        
remark       TextField    Remark (Bemerkung,Remarque)                                
============ ============ ===========================================================

    
Defined in :srcref:`/lino/modlib/notes/models.py`

.. index::
   single: field;id
   
.. _std.notes.NoteType.id:

Field **NoteType.id**
=====================





Type: AutoField

   
.. index::
   single: field;build_method
   
.. _std.notes.NoteType.build_method:

Field **NoteType.build_method**
===============================





Type: CharField

   
.. index::
   single: field;template
   
.. _std.notes.NoteType.template:

Field **NoteType.template**
===========================





Type: CharField

   
.. index::
   single: field;name
   
.. _std.notes.NoteType.name:

Field **NoteType.name**
=======================





Type: CharField

   
.. index::
   single: field;important
   
.. _std.notes.NoteType.important:

Field **NoteType.important**
============================





Type: BooleanField

   
.. index::
   single: field;remark
   
.. _std.notes.NoteType.remark:

Field **NoteType.remark**
=========================





Type: TextField

   


.. index::
   pair: model; EventType

.. _std.notes.EventType:

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

.. index::
   single: field;id
   
.. _std.notes.EventType.id:

Field **EventType.id**
======================





Type: AutoField

   
.. index::
   single: field;name
   
.. _std.notes.EventType.name:

Field **EventType.name**
========================





Type: BabelCharField

   
.. index::
   single: field;remark
   
.. _std.notes.EventType.remark:

Field **EventType.remark**
==========================





Type: TextField

   
.. index::
   single: field;name_fr
   
.. _std.notes.EventType.name_fr:

Field **EventType.name_fr**
===========================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _std.notes.EventType.name_nl:

Field **EventType.name_nl**
===========================





Type: CharField

   
.. index::
   single: field;name_en
   
.. _std.notes.EventType.name_en:

Field **EventType.name_en**
===========================





Type: CharField

   


.. index::
   pair: model; Note

.. _std.notes.Note:

--------------
Model **Note**
--------------



Note(id, user_id, reminder_date, reminder_text, delay_value, delay_type, reminder_done, must_build, person_id, company_id, date, type_id, event_type_id, subject, body, language)
  
============= ============= ======================================================================
name          type          verbose name                                                          
============= ============= ======================================================================
id            AutoField     ID                                                                    
user          ForeignKey    user (Benutzer,utilisateur)                                           
reminder_date DateField     Due date (Fällig am,Terme)                                            
reminder_text CharField     Reminder text (Erinnerungstext,Texte de rappel)                       
delay_value   IntegerField  Delay (value) (Frist (Wert),Delai (valeur))                           
delay_type    CharField     Delay (unit) (Frist (Einheit),Délai (unité))                          
reminder_done BooleanField  Done (Erledigt,Fait)                                                  
must_build    BooleanField  must build (muss generiert werden,doit construire)                    
person        ForeignKey    Person (Personne)                                                     
company       ForeignKey    Company (Firma)                                                       
date          DateField     Date (Datum)                                                          
type          ForeignKey    Note Type (Form) (Notizart (Form),Type de note (Formulaire))          
event_type    ForeignKey    Event Type (Content) (Ereignisart (Inhalt),Type d'événement (contenu))
subject       CharField     Subject (Betreff,Objet)                                               
body          HtmlTextField Body (Inhalt,Corps)                                                   
language      LanguageField Language (Sprache,Langue)                                             
============= ============= ======================================================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

.. index::
   single: field;id
   
.. _std.notes.Note.id:

Field **Note.id**
=================





Type: AutoField

   
.. index::
   single: field;user
   
.. _std.notes.Note.user:

Field **Note.user**
===================





Type: ForeignKey

   
.. index::
   single: field;reminder_date
   
.. _std.notes.Note.reminder_date:

Field **Note.reminder_date**
============================





Type: DateField

   
.. index::
   single: field;reminder_text
   
.. _std.notes.Note.reminder_text:

Field **Note.reminder_text**
============================





Type: CharField

   
.. index::
   single: field;delay_value
   
.. _std.notes.Note.delay_value:

Field **Note.delay_value**
==========================





Type: IntegerField

   
.. index::
   single: field;delay_type
   
.. _std.notes.Note.delay_type:

Field **Note.delay_type**
=========================





Type: CharField

   
.. index::
   single: field;reminder_done
   
.. _std.notes.Note.reminder_done:

Field **Note.reminder_done**
============================





Type: BooleanField

   
.. index::
   single: field;must_build
   
.. _std.notes.Note.must_build:

Field **Note.must_build**
=========================





Type: BooleanField

   
.. index::
   single: field;person
   
.. _std.notes.Note.person:

Field **Note.person**
=====================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _std.notes.Note.company:

Field **Note.company**
======================





Type: ForeignKey

   
.. index::
   single: field;date
   
.. _std.notes.Note.date:

Field **Note.date**
===================





Type: DateField

   
.. index::
   single: field;type
   
.. _std.notes.Note.type:

Field **Note.type**
===================





Type: ForeignKey

   
.. index::
   single: field;event_type
   
.. _std.notes.Note.event_type:

Field **Note.event_type**
=========================





Type: ForeignKey

   
.. index::
   single: field;subject
   
.. _std.notes.Note.subject:

Field **Note.subject**
======================





Type: CharField

   
.. index::
   single: field;body
   
.. _std.notes.Note.body:

Field **Note.body**
===================





Type: HtmlTextField

   
.. index::
   single: field;language
   
.. _std.notes.Note.language:

Field **Note.language**
=======================





Type: LanguageField

   


