=====
notes
=====



.. currentmodule:: notes

Defined in :srcref:`/lino/modlib/notes/models.py`




.. index::
   pair: model; NoteType
   single: field;id
   single: field;build_method
   single: field;template
   single: field;name
   single: field;important
   single: field;remark

.. _dsbe.notes.NoteType:

------------------
Model ``NoteType``
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
   pair: model; Note
   single: field;id
   single: field;user
   single: field;reminder_date
   single: field;reminder_text
   single: field;delay_value
   single: field;delay_type
   single: field;must_build
   single: field;person
   single: field;company
   single: field;date
   single: field;type
   single: field;subject
   single: field;body
   single: field;language

.. _dsbe.notes.Note:

--------------
Model ``Note``
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

    
Defined in :srcref:`/lino/sites/dsbe/models.py`


