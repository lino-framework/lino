=======
uploads
=======



.. currentmodule:: uploads

Defined in :srcref:`/lino/modlib/uploads/models.py`





.. index::
   pair: model; UploadType
   single: field;id
   single: field;name

.. _dsbe.uploads.UploadType:

--------------------
Model ``UploadType``
--------------------



UploadType(id, name)
  
==== ========= ============
name type      verbose name
==== ========= ============
id   AutoField ID          
name CharField Name        
==== ========= ============

    
Defined in :srcref:`/lino/modlib/uploads/models.py`


.. index::
   pair: model; Upload
   single: field;id
   single: field;user
   single: field;reminder_date
   single: field;reminder_text
   single: field;delay_value
   single: field;delay_type
   single: field;file
   single: field;mimetype
   single: field;created
   single: field;modified
   single: field;description
   single: field;person
   single: field;company
   single: field;type

.. _dsbe.uploads.Upload:

----------------
Model ``Upload``
----------------



Upload(id, user_id, reminder_date, reminder_text, delay_value, delay_type, file, mimetype, created, modified, description, person_id, company_id, type_id)
  
============= ============= ===============================
name          type          verbose name                   
============= ============= ===============================
id            AutoField     ID                             
user          ForeignKey    user (Benutzer)                
reminder_date DateField     Due date (Fällig am)           
reminder_text CharField     Reminder text (Erinnerungstext)
delay_value   IntegerField  Delay (value) (Frist (Wert))   
delay_type    CharField     Delay (unit) (Frist (Einheit)) 
file          FileField     File (Datei)                   
mimetype      CharField     MIME type (MIME-Art)           
created       DateTimeField Created (Erstellt)             
modified      DateTimeField Modified (Bearbeitet)          
description   CharField     Description (Beschreibung)     
person        ForeignKey    Person                         
company       ForeignKey    Company                        
type          ForeignKey    type                           
============= ============= ===============================

    
Defined in :srcref:`/lino/modlib/uploads/models.py`


