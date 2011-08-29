=======
uploads
=======



.. currentmodule:: uploads

Defined in :srcref:`/lino/modlib/uploads/models.py`




.. contents:: Table of Contents



.. index::
   pair: model; UploadType

.. _lino.uploads.UploadType:

--------------------
Model **UploadType**
--------------------



UploadType(id, name)
  
==== ========= ============
name type      verbose name
==== ========= ============
id   AutoField ID          
name CharField Name (Nom)  
==== ========= ============

    
Defined in :srcref:`/lino/modlib/uploads/models.py`

Referenced from
`lino.lino.SiteConfig.residence_permit_upload_type`_, `lino.lino.SiteConfig.work_permit_upload_type`_, `lino.lino.SiteConfig.driving_licence_upload_type`_, `lino.uploads.Upload.type`_



.. index::
   single: field;id
   
.. _lino.uploads.UploadType.id:

Field **UploadType.id**
=======================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.uploads.UploadType.name:

Field **UploadType.name**
=========================





Type: CharField

   


.. index::
   pair: model; Upload

.. _lino.uploads.Upload:

----------------
Model **Upload**
----------------



Upload(id, user_id, created, modified, owner_type_id, owner_id, file, mimetype, type_id, valid_until, description)
  
=========== ======================== =================================================
name        type                     verbose name                                     
=========== ======================== =================================================
id          AutoField                ID                                               
user        ForeignKey               User (Benutzer,Utilisateur)                      
created     DateTimeField            created                                          
modified    DateTimeField            modified                                         
owner_type  ForeignKey               Owner type (Besitzertabelle,type de propriétaire)
owner_id    GenericForeignKeyIdField Owner (Besitzer,Propriétaire)                    
file        FileField                File (Datei,Fichier)                             
mimetype    CharField                MIME type (MIME-Art,type MIME)                   
type        ForeignKey               upload type (Upload-Art,types d'upload)          
valid_until DateField                valid until (gültig bis,valid jusqu'au)          
description CharField                Description (Beschreibung)                       
=========== ======================== =================================================

    
Defined in :srcref:`/lino/modlib/uploads/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.uploads.Upload.id:

Field **Upload.id**
===================





Type: AutoField

   
.. index::
   single: field;user
   
.. _lino.uploads.Upload.user:

Field **Upload.user**
=====================





Type: ForeignKey

   
.. index::
   single: field;created
   
.. _lino.uploads.Upload.created:

Field **Upload.created**
========================





Type: DateTimeField

   
.. index::
   single: field;modified
   
.. _lino.uploads.Upload.modified:

Field **Upload.modified**
=========================





Type: DateTimeField

   
.. index::
   single: field;owner_type
   
.. _lino.uploads.Upload.owner_type:

Field **Upload.owner_type**
===========================





Type: ForeignKey

   
.. index::
   single: field;owner_id
   
.. _lino.uploads.Upload.owner_id:

Field **Upload.owner_id**
=========================





Type: GenericForeignKeyIdField

   
.. index::
   single: field;file
   
.. _lino.uploads.Upload.file:

Field **Upload.file**
=====================





Type: FileField

   
.. index::
   single: field;mimetype
   
.. _lino.uploads.Upload.mimetype:

Field **Upload.mimetype**
=========================





Type: CharField

   
.. index::
   single: field;type
   
.. _lino.uploads.Upload.type:

Field **Upload.type**
=====================





Type: ForeignKey

   
.. index::
   single: field;valid_until
   
.. _lino.uploads.Upload.valid_until:

Field **Upload.valid_until**
============================





Type: DateField

   
.. index::
   single: field;description
   
.. _lino.uploads.Upload.description:

Field **Upload.description**
============================





Type: CharField

   


