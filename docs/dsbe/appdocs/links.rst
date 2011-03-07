=====
links
=====



.. currentmodule:: links

Defined in :srcref:`/lino/modlib/links/models.py`




.. index::
   pair: model; LinkType
   single: field;id
   single: field;name

.. _dsbe.links.LinkType:

------------------
Model ``LinkType``
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
   pair: model; Link
   single: field;id
   single: field;user
   single: field;reminder_date
   single: field;reminder_text
   single: field;delay_value
   single: field;delay_type
   single: field;person
   single: field;company
   single: field;type
   single: field;date
   single: field;url
   single: field;name

.. _dsbe.links.Link:

--------------
Model ``Link``
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


