============
contenttypes
============



.. currentmodule:: contenttypes

Defined in :srcref:`/django/contrib/contenttypes/models.py`



.. contents:: Table of Contents



.. index::
   pair: model; ContentType

.. _lino.contenttypes.ContentType:

---------------------
Model **ContentType**
---------------------



ContentType(id, name, app_label, model)
  
========= ========= ================================================================================================================
name      type      verbose name                                                                                                    
========= ========= ================================================================================================================
id        AutoField ID                                                                                                              
name      CharField name                                                                                                            
app_label CharField app label                                                                                                       
model     CharField python model class name (Python Modell-Klassenname,nom de la classe python du modèle,klassenaam van pythonmodel)
========= ========= ================================================================================================================

    
Defined in :srcref:`/django/contrib/contenttypes/models.py`

Referenced from
`lino.uploads.Upload.owner_type`_, `lino.cal.Task.owner_type`_, `lino.thirds.Third.owner_type`_



.. index::
   single: field;id
   
.. _lino.contenttypes.ContentType.id:

Field **ContentType.id**
========================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.contenttypes.ContentType.name:

Field **ContentType.name**
==========================





Type: CharField

   
.. index::
   single: field;app_label
   
.. _lino.contenttypes.ContentType.app_label:

Field **ContentType.app_label**
===============================





Type: CharField

   
.. index::
   single: field;model
   
.. _lino.contenttypes.ContentType.model:

Field **ContentType.model**
===========================





Type: CharField

   


