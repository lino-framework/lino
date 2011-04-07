=====
links
=====



.. currentmodule:: links

Defined in :srcref:`/lino/modlib/links/models.py`



.. contents:: Table of Contents



.. index::
   pair: model; LinkType

.. _std.links.LinkType:

------------------
Model **LinkType**
------------------



Implements :class:`links.LinkType`.
  
==== ========= ============
name type      verbose name
==== ========= ============
id   AutoField ID          
name CharField Name        
==== ========= ============

    
Defined in :srcref:`/lino/modlib/links/models.py`

.. index::
   single: field;id
   
.. _std.links.LinkType.id:

Field **LinkType.id**
=====================





Type: AutoField

   
.. index::
   single: field;name
   
.. _std.links.LinkType.name:

Field **LinkType.name**
=======================





Type: CharField

   


.. index::
   pair: model; Link

.. _std.links.Link:

--------------
Model **Link**
--------------



Link(id, user_id, reminder_date, reminder_text, delay_value, delay_type, person_id, company_id, type_id, date, url, name)
  
============= ============= ===============================
name          type          verbose name                   
============= ============= ===============================
id            AutoField     ID                             
user          ForeignKey    user (Benutzer)                
reminder_date DateField     Due date (Fällig am)           
reminder_text CharField     Reminder text (Erinnerungstext)
delay_value   IntegerField  Delay (value) (Frist (Wert))   
delay_type    CharField     Delay (unit) (Frist (Einheit)) 
person        ForeignKey    Person                         
company       ForeignKey    Company                        
type          ForeignKey    Link type (Verweisart)         
date          DateTimeField Date (Datum)                   
url           URLField      url                            
name          CharField     Name                           
============= ============= ===============================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

.. index::
   single: field;id
   
.. _std.links.Link.id:

Field **Link.id**
=================





Type: AutoField

   
.. index::
   single: field;user
   
.. _std.links.Link.user:

Field **Link.user**
===================





Type: ForeignKey

   
.. index::
   single: field;reminder_date
   
.. _std.links.Link.reminder_date:

Field **Link.reminder_date**
============================





Type: DateField

   
.. index::
   single: field;reminder_text
   
.. _std.links.Link.reminder_text:

Field **Link.reminder_text**
============================





Type: CharField

   
.. index::
   single: field;delay_value
   
.. _std.links.Link.delay_value:

Field **Link.delay_value**
==========================





Type: IntegerField

   
.. index::
   single: field;delay_type
   
.. _std.links.Link.delay_type:

Field **Link.delay_type**
=========================





Type: CharField

   
.. index::
   single: field;person
   
.. _std.links.Link.person:

Field **Link.person**
=====================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _std.links.Link.company:

Field **Link.company**
======================





Type: ForeignKey

   
.. index::
   single: field;type
   
.. _std.links.Link.type:

Field **Link.type**
===================





Type: ForeignKey

   
.. index::
   single: field;date
   
.. _std.links.Link.date:

Field **Link.date**
===================





Type: DateTimeField

   
.. index::
   single: field;url
   
.. _std.links.Link.url:

Field **Link.url**
==================





Type: URLField

   
.. index::
   single: field;name
   
.. _std.links.Link.name:

Field **Link.name**
===================





Type: CharField

   


