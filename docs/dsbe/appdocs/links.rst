=====
links
=====



.. currentmodule:: links

Defined in :srcref:`/lino/modlib/links/models.py`



.. contents:: Table of Contents



.. index::
   pair: model; LinkType

.. _dsbe.links.LinkType:

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
   
.. _dsbe.links.LinkType.id:

Field **LinkType.id**
=====================





Type: AutoField

   
.. index::
   single: field;name
   
.. _dsbe.links.LinkType.name:

Field **LinkType.name**
=======================





Type: CharField

   


.. index::
   pair: model; Link

.. _dsbe.links.Link:

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

    
Defined in :srcref:`/lino/sites/dsbe/models.py`

.. index::
   single: field;id
   
.. _dsbe.links.Link.id:

Field **Link.id**
=================





Type: AutoField

   
.. index::
   single: field;user
   
.. _dsbe.links.Link.user:

Field **Link.user**
===================





Type: ForeignKey

   
.. index::
   single: field;reminder_date
   
.. _dsbe.links.Link.reminder_date:

Field **Link.reminder_date**
============================





Type: DateField

   
.. index::
   single: field;reminder_text
   
.. _dsbe.links.Link.reminder_text:

Field **Link.reminder_text**
============================





Type: CharField

   
.. index::
   single: field;delay_value
   
.. _dsbe.links.Link.delay_value:

Field **Link.delay_value**
==========================





Type: IntegerField

   
.. index::
   single: field;delay_type
   
.. _dsbe.links.Link.delay_type:

Field **Link.delay_type**
=========================





Type: CharField

   
.. index::
   single: field;person
   
.. _dsbe.links.Link.person:

Field **Link.person**
=====================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _dsbe.links.Link.company:

Field **Link.company**
======================





Type: ForeignKey

   
.. index::
   single: field;type
   
.. _dsbe.links.Link.type:

Field **Link.type**
===================





Type: ForeignKey

   
.. index::
   single: field;date
   
.. _dsbe.links.Link.date:

Field **Link.date**
===================





Type: DateTimeField

   
.. index::
   single: field;url
   
.. _dsbe.links.Link.url:

Field **Link.url**
==================





Type: URLField

   
.. index::
   single: field;name
   
.. _dsbe.links.Link.name:

Field **Link.name**
===================





Type: CharField

   


