=====
notes
=====



.. currentmodule:: notes

Defined in :srcref:`/lino/modlib/notes/models.py`



.. contents:: Table of Contents



.. index::
   pair: model; NoteType

.. _dsbe.notes.NoteType:

------------------
Model **NoteType**
------------------



NoteType(id, build_method, template, name, important, remark)
  
============ ============ ===================================
name         type         verbose name                       
============ ============ ===================================
id           AutoField    ID                                 
build_method CharField    Build method (Konstruktionsmethode)
template     CharField    Template (Vorlage)                 
name         CharField    name                               
important    BooleanField important (wichtig)                
remark       TextField    Remark (Bemerkung)                 
============ ============ ===================================

    
Defined in :srcref:`/lino/modlib/notes/models.py`

.. index::
   single: field;id
   
.. _dsbe.notes.NoteType.id:

Field **NoteType.id**
=====================





Type: AutoField

   
.. index::
   single: field;build_method
   
.. _dsbe.notes.NoteType.build_method:

Field **NoteType.build_method**
===============================





Type: CharField

   
.. index::
   single: field;template
   
.. _dsbe.notes.NoteType.template:

Field **NoteType.template**
===========================





Type: CharField

   
.. index::
   single: field;name
   
.. _dsbe.notes.NoteType.name:

Field **NoteType.name**
=======================





Type: CharField

   
.. index::
   single: field;important
   
.. _dsbe.notes.NoteType.important:

Field **NoteType.important**
============================





Type: BooleanField

   
.. index::
   single: field;remark
   
.. _dsbe.notes.NoteType.remark:

Field **NoteType.remark**
=========================





Type: TextField

   


.. index::
   pair: model; Note

.. _dsbe.notes.Note:

--------------
Model **Note**
--------------



Note(id, user_id, reminder_date, reminder_text, delay_value, delay_type, must_build, person_id, company_id, date, type_id, subject, body, language)
  
============= ============= ==================================
name          type          verbose name                      
============= ============= ==================================
id            AutoField     ID                                
user          ForeignKey    user (Benutzer)                   
reminder_date DateField     Due date (Fällig am)              
reminder_text CharField     Reminder text (Erinnerungstext)   
delay_value   IntegerField  Delay (value) (Frist (Wert))      
delay_type    CharField     Delay (unit) (Frist (Einheit))    
must_build    BooleanField  must build (muss generiert werden)
person        ForeignKey    Person                            
company       ForeignKey    Company                           
date          DateField     Date (Datum)                      
type          ForeignKey    Note type (Notizart)              
subject       CharField     Subject (Betreff)                 
body          TextField     Body (Inhalt)                     
language      LanguageField Language (Sprache)                
============= ============= ==================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

.. index::
   single: field;id
   
.. _dsbe.notes.Note.id:

Field **Note.id**
=================





Type: AutoField

   
.. index::
   single: field;user
   
.. _dsbe.notes.Note.user:

Field **Note.user**
===================





Type: ForeignKey

   
.. index::
   single: field;reminder_date
   
.. _dsbe.notes.Note.reminder_date:

Field **Note.reminder_date**
============================





Type: DateField

   
.. index::
   single: field;reminder_text
   
.. _dsbe.notes.Note.reminder_text:

Field **Note.reminder_text**
============================





Type: CharField

   
.. index::
   single: field;delay_value
   
.. _dsbe.notes.Note.delay_value:

Field **Note.delay_value**
==========================





Type: IntegerField

   
.. index::
   single: field;delay_type
   
.. _dsbe.notes.Note.delay_type:

Field **Note.delay_type**
=========================





Type: CharField

   
.. index::
   single: field;must_build
   
.. _dsbe.notes.Note.must_build:

Field **Note.must_build**
=========================





Type: BooleanField

   
.. index::
   single: field;person
   
.. _dsbe.notes.Note.person:

Field **Note.person**
=====================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _dsbe.notes.Note.company:

Field **Note.company**
======================





Type: ForeignKey

   
.. index::
   single: field;date
   
.. _dsbe.notes.Note.date:

Field **Note.date**
===================





Type: DateField

   
.. index::
   single: field;type
   
.. _dsbe.notes.Note.type:

Field **Note.type**
===================





Type: ForeignKey

   
.. index::
   single: field;subject
   
.. _dsbe.notes.Note.subject:

Field **Note.subject**
======================





Type: CharField

   
.. index::
   single: field;body
   
.. _dsbe.notes.Note.body:

Field **Note.body**
===================





Type: TextField

   
.. index::
   single: field;language
   
.. _dsbe.notes.Note.language:

Field **Note.language**
=======================





Type: LanguageField

   


