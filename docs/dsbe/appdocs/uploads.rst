=======
uploads
=======



.. currentmodule:: uploads

Defined in :srcref:`/lino/modlib/uploads/models.py`




.. contents:: Table of Contents



.. index::
   pair: model; UploadType

.. _dsbe.uploads.UploadType:

--------------------
Model **UploadType**
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
   single: field;id
   
.. _dsbe.uploads.UploadType.id:

Field **UploadType.id**
=======================





Type: AutoField

   
.. index::
   single: field;name
   
.. _dsbe.uploads.UploadType.name:

Field **UploadType.name**
=========================





Type: CharField

   


.. index::
   pair: model; Upload

.. _dsbe.uploads.Upload:

----------------
Model **Upload**
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

.. index::
   single: field;id
   
.. _dsbe.uploads.Upload.id:

Field **Upload.id**
===================





Type: AutoField

   
.. index::
   single: field;user
   
.. _dsbe.uploads.Upload.user:

Field **Upload.user**
=====================





Type: ForeignKey

   
.. index::
   single: field;reminder_date
   
.. _dsbe.uploads.Upload.reminder_date:

Field **Upload.reminder_date**
==============================





Type: DateField

   
.. index::
   single: field;reminder_text
   
.. _dsbe.uploads.Upload.reminder_text:

Field **Upload.reminder_text**
==============================





Type: CharField

   
.. index::
   single: field;delay_value
   
.. _dsbe.uploads.Upload.delay_value:

Field **Upload.delay_value**
============================





Type: IntegerField

   
.. index::
   single: field;delay_type
   
.. _dsbe.uploads.Upload.delay_type:

Field **Upload.delay_type**
===========================





Type: CharField

   
.. index::
   single: field;file
   
.. _dsbe.uploads.Upload.file:

Field **Upload.file**
=====================





Type: FileField

   
.. index::
   single: field;mimetype
   
.. _dsbe.uploads.Upload.mimetype:

Field **Upload.mimetype**
=========================





Type: CharField

   
.. index::
   single: field;created
   
.. _dsbe.uploads.Upload.created:

Field **Upload.created**
========================





Type: DateTimeField

   
.. index::
   single: field;modified
   
.. _dsbe.uploads.Upload.modified:

Field **Upload.modified**
=========================





Type: DateTimeField

   
.. index::
   single: field;description
   
.. _dsbe.uploads.Upload.description:

Field **Upload.description**
============================





Type: CharField

   
.. index::
   single: field;person
   
.. _dsbe.uploads.Upload.person:

Field **Upload.person**
=======================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _dsbe.uploads.Upload.company:

Field **Upload.company**
========================





Type: ForeignKey

   
.. index::
   single: field;type
   
.. _dsbe.uploads.Upload.type:

Field **Upload.type**
=====================





Type: ForeignKey

   


