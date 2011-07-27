===
cal
===



.. currentmodule:: cal

Defined in :srcref:`/lino/modlib/cal/models.py`


This module deserves more documentation.

It defines tables like :class:`Task` and :class:`Event` 



.. contents:: Table of Contents



.. index::
   pair: model; Place

.. _lino.cal.Place:

---------------
Model **Place**
---------------



Place(id, name)
  
==== ========= ============
name type      verbose name
==== ========= ============
id   AutoField ID          
name CharField Name (Nom)  
==== ========= ============

    
Defined in :srcref:`/lino/modlib/cal/models.py`

Referenced from
`lino.cal.Event.place`_



.. index::
   single: field;id
   
.. _lino.cal.Place.id:

Field **Place.id**
==================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.cal.Place.name:

Field **Place.name**
====================





Type: CharField

   


.. index::
   pair: model; EventType

.. _lino.cal.EventType:

-------------------
Model **EventType**
-------------------



EventType(id, build_method, template, name, name_fr, name_nl, name_en)
  
============ ============== ===========================================================
name         type           verbose name                                               
============ ============== ===========================================================
id           AutoField      ID                                                         
build_method CharField      Build method (Konstruktionsmethode,Méthode de construction)
template     CharField      Template (Vorlage,Modèle)                                  
name         BabelCharField Event title                                                
name_fr      CharField      Event title (fr)                                           
name_nl      CharField      Event title (nl)                                           
name_en      CharField      Event title (en)                                           
============ ============== ===========================================================

    
Defined in :srcref:`/lino/modlib/cal/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.cal.EventType.id:

Field **EventType.id**
======================





Type: AutoField

   
.. index::
   single: field;build_method
   
.. _lino.cal.EventType.build_method:

Field **EventType.build_method**
================================





Type: CharField

   
.. index::
   single: field;template
   
.. _lino.cal.EventType.template:

Field **EventType.template**
============================





Type: CharField

   
.. index::
   single: field;name
   
.. _lino.cal.EventType.name:

Field **EventType.name**
========================





Type: BabelCharField

   
.. index::
   single: field;name_fr
   
.. _lino.cal.EventType.name_fr:

Field **EventType.name_fr**
===========================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _lino.cal.EventType.name_nl:

Field **EventType.name_nl**
===========================





Type: CharField

   
.. index::
   single: field;name_en
   
.. _lino.cal.EventType.name_en:

Field **EventType.name_en**
===========================





Type: CharField

   


.. index::
   pair: model; Attendance

.. _lino.cal.Attendance:

--------------------
Model **Attendance**
--------------------



Attendance(id, must_build, person_id, company_id, event_id, confirmed, remark)
  
========== ============ ======================================================
name       type         verbose name                                          
========== ============ ======================================================
id         AutoField    ID                                                    
must_build BooleanField must build (muss generiert werden,doit être construit)
person     ForeignKey   Person (Personne)                                     
company    ForeignKey   Company (Firma,Société)                               
event      ForeignKey   Event (Termin)                                        
confirmed  DateField    Confirmed                                             
remark     CharField    Remark (Bemerkung,Remarque)                           
========== ============ ======================================================

    
Defined in :srcref:`/lino/modlib/cal/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.cal.Attendance.id:

Field **Attendance.id**
=======================





Type: AutoField

   
.. index::
   single: field;must_build
   
.. _lino.cal.Attendance.must_build:

Field **Attendance.must_build**
===============================





Type: BooleanField

   
.. index::
   single: field;person
   
.. _lino.cal.Attendance.person:

Field **Attendance.person**
===========================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _lino.cal.Attendance.company:

Field **Attendance.company**
============================





Type: ForeignKey

   
.. index::
   single: field;event
   
.. _lino.cal.Attendance.event:

Field **Attendance.event**
==========================





Type: ForeignKey

   
.. index::
   single: field;confirmed
   
.. _lino.cal.Attendance.confirmed:

Field **Attendance.confirmed**
==============================





Type: DateField

   
.. index::
   single: field;remark
   
.. _lino.cal.Attendance.remark:

Field **Attendance.remark**
===========================





Type: CharField

   


.. index::
   pair: model; Event

.. _lino.cal.Event:

---------------
Model **Event**
---------------



Event(id, person_id, company_id, componentmixin_ptr_id, user_id, created, modified, must_build, start_date, start_time, summary, description, access_class, sequence, alarm_value, alarm_unit, dt_alarm, end_date, end_time, transparent, place_id, priority, status, duration_value, duration_unit, repeat_value, repeat_unit)
  
================== =============== ======================================================
name               type            verbose name                                          
================== =============== ======================================================
id                 AutoField       ID                                                    
person             ForeignKey      Person (Personne)                                     
company            ForeignKey      Company (Firma,Société)                               
componentmixin_ptr OneToOneField   componentmixin ptr                                    
user               ForeignKey      user (Benutzer,utilisateur)                           
created            DateTimeField   created                                               
modified           DateTimeField   modified                                              
must_build         BooleanField    must build (muss generiert werden,doit être construit)
start_date         DateField       Start date (Beginnt am)                               
start_time         TimeField       Start time (Beginnt um)                               
summary            CharField       Summary (Kurzbeschreibung)                            
description        RichTextField   Description (Beschreibung)                            
access_class       ChoiceListField Access Class (Zugriffsklasse)                         
sequence           IntegerField    Revision (Revisionsnummer)                            
alarm_value        IntegerField    Alarm value (Erinnerung (Anzahl))                     
alarm_unit         ChoiceListField Alarm unit (Erinnerung (Einheit))                     
dt_alarm           DateTimeField   dt alarm                                              
end_date           DateField       End date (Endet am)                                   
end_time           TimeField       End time (Endet um)                                   
transparent        BooleanField    Transparent (nicht blockierend)                       
place              ForeignKey      Place (Ort)                                           
priority           ChoiceListField Priority (Priorität)                                  
status             ChoiceListField Status (Statut)                                       
duration_value     IntegerField    Duration value (Dauer (Anzahl))                       
duration_unit      ChoiceListField Duration Unit (Dauer (Einheit))                       
repeat_value       IntegerField    Repeat every (Wiederholen)                            
repeat_unit        ChoiceListField Repeat every (Wiederholen)                            
================== =============== ======================================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from
`lino.cal.Attendance.event`_



.. index::
   single: field;id
   
.. _lino.cal.Event.id:

Field **Event.id**
==================





Type: AutoField

   
.. index::
   single: field;person
   
.. _lino.cal.Event.person:

Field **Event.person**
======================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _lino.cal.Event.company:

Field **Event.company**
=======================





Type: ForeignKey

   
.. index::
   single: field;componentmixin_ptr
   
.. _lino.cal.Event.componentmixin_ptr:

Field **Event.componentmixin_ptr**
==================================





Type: OneToOneField

   
.. index::
   single: field;user
   
.. _lino.cal.Event.user:

Field **Event.user**
====================





Type: ForeignKey

   
.. index::
   single: field;created
   
.. _lino.cal.Event.created:

Field **Event.created**
=======================





Type: DateTimeField

   
.. index::
   single: field;modified
   
.. _lino.cal.Event.modified:

Field **Event.modified**
========================





Type: DateTimeField

   
.. index::
   single: field;must_build
   
.. _lino.cal.Event.must_build:

Field **Event.must_build**
==========================





Type: BooleanField

   
.. index::
   single: field;start_date
   
.. _lino.cal.Event.start_date:

Field **Event.start_date**
==========================





Type: DateField

   
.. index::
   single: field;start_time
   
.. _lino.cal.Event.start_time:

Field **Event.start_time**
==========================





Type: TimeField

   
.. index::
   single: field;summary
   
.. _lino.cal.Event.summary:

Field **Event.summary**
=======================





Type: CharField

   
.. index::
   single: field;description
   
.. _lino.cal.Event.description:

Field **Event.description**
===========================





Type: RichTextField

   
.. index::
   single: field;access_class
   
.. _lino.cal.Event.access_class:

Field **Event.access_class**
============================





Type: ChoiceListField

   
.. index::
   single: field;sequence
   
.. _lino.cal.Event.sequence:

Field **Event.sequence**
========================





Type: IntegerField

   
.. index::
   single: field;alarm_value
   
.. _lino.cal.Event.alarm_value:

Field **Event.alarm_value**
===========================





Type: IntegerField

   
.. index::
   single: field;alarm_unit
   
.. _lino.cal.Event.alarm_unit:

Field **Event.alarm_unit**
==========================





Type: ChoiceListField

   
.. index::
   single: field;dt_alarm
   
.. _lino.cal.Event.dt_alarm:

Field **Event.dt_alarm**
========================





Type: DateTimeField

   
.. index::
   single: field;end_date
   
.. _lino.cal.Event.end_date:

Field **Event.end_date**
========================





Type: DateField

   
.. index::
   single: field;end_time
   
.. _lino.cal.Event.end_time:

Field **Event.end_time**
========================





Type: TimeField

   
.. index::
   single: field;transparent
   
.. _lino.cal.Event.transparent:

Field **Event.transparent**
===========================





Type: BooleanField

   
.. index::
   single: field;place
   
.. _lino.cal.Event.place:

Field **Event.place**
=====================





Type: ForeignKey

   
.. index::
   single: field;priority
   
.. _lino.cal.Event.priority:

Field **Event.priority**
========================





Type: ChoiceListField

   
.. index::
   single: field;status
   
.. _lino.cal.Event.status:

Field **Event.status**
======================





Type: ChoiceListField

   
.. index::
   single: field;duration_value
   
.. _lino.cal.Event.duration_value:

Field **Event.duration_value**
==============================





Type: IntegerField

   
.. index::
   single: field;duration_unit
   
.. _lino.cal.Event.duration_unit:

Field **Event.duration_unit**
=============================





Type: ChoiceListField

   
.. index::
   single: field;repeat_value
   
.. _lino.cal.Event.repeat_value:

Field **Event.repeat_value**
============================





Type: IntegerField

   
.. index::
   single: field;repeat_unit
   
.. _lino.cal.Event.repeat_unit:

Field **Event.repeat_unit**
===========================





Type: ChoiceListField

   


.. index::
   pair: model; Task

.. _lino.cal.Task:

--------------
Model **Task**
--------------



Task(id, person_id, company_id, componentmixin_ptr_id, user_id, created, modified, owner_type_id, owner_id, start_date, start_time, summary, description, access_class, sequence, alarm_value, alarm_unit, dt_alarm, due_date, due_time, done, percent, status, auto_type)
  
================== ======================== =================================================
name               type                     verbose name                                     
================== ======================== =================================================
id                 AutoField                ID                                               
person             ForeignKey               Person (Personne)                                
company            ForeignKey               Company (Firma,Société)                          
componentmixin_ptr OneToOneField            componentmixin ptr                               
user               ForeignKey               user (Benutzer,utilisateur)                      
created            DateTimeField            created                                          
modified           DateTimeField            modified                                         
owner_type         ForeignKey               Owner type (Besitzertabelle,type de propriétaire)
owner_id           GenericForeignKeyIdField Owner (Besitzer,Propriétaire)                    
start_date         DateField                Start date (Beginnt am)                          
start_time         TimeField                Start time (Beginnt um)                          
summary            CharField                Summary (Kurzbeschreibung)                       
description        RichTextField            Description (Beschreibung)                       
access_class       ChoiceListField          Access Class (Zugriffsklasse)                    
sequence           IntegerField             Revision (Revisionsnummer)                       
alarm_value        IntegerField             Alarm value (Erinnerung (Anzahl))                
alarm_unit         ChoiceListField          Alarm unit (Erinnerung (Einheit))                
dt_alarm           DateTimeField            dt alarm                                         
due_date           DateField                Due date (Fällig am,Terme)                       
due_time           TimeField                Due time (Fällig um)                             
done               BooleanField             Done (Erledigt,Fait)                             
percent            IntegerField             Duration value (Dauer (Anzahl))                  
status             ChoiceListField          Task Status (Aufgabenstatus)                     
auto_type          IntegerField             auto type                                        
================== ======================== =================================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.cal.Task.id:

Field **Task.id**
=================





Type: AutoField

   
.. index::
   single: field;person
   
.. _lino.cal.Task.person:

Field **Task.person**
=====================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _lino.cal.Task.company:

Field **Task.company**
======================





Type: ForeignKey

   
.. index::
   single: field;componentmixin_ptr
   
.. _lino.cal.Task.componentmixin_ptr:

Field **Task.componentmixin_ptr**
=================================





Type: OneToOneField

   
.. index::
   single: field;user
   
.. _lino.cal.Task.user:

Field **Task.user**
===================





Type: ForeignKey

   
.. index::
   single: field;created
   
.. _lino.cal.Task.created:

Field **Task.created**
======================





Type: DateTimeField

   
.. index::
   single: field;modified
   
.. _lino.cal.Task.modified:

Field **Task.modified**
=======================





Type: DateTimeField

   
.. index::
   single: field;owner_type
   
.. _lino.cal.Task.owner_type:

Field **Task.owner_type**
=========================





Type: ForeignKey

   
.. index::
   single: field;owner_id
   
.. _lino.cal.Task.owner_id:

Field **Task.owner_id**
=======================





Type: GenericForeignKeyIdField

   
.. index::
   single: field;start_date
   
.. _lino.cal.Task.start_date:

Field **Task.start_date**
=========================





Type: DateField

   
.. index::
   single: field;start_time
   
.. _lino.cal.Task.start_time:

Field **Task.start_time**
=========================





Type: TimeField

   
.. index::
   single: field;summary
   
.. _lino.cal.Task.summary:

Field **Task.summary**
======================





Type: CharField

   
.. index::
   single: field;description
   
.. _lino.cal.Task.description:

Field **Task.description**
==========================





Type: RichTextField

   
.. index::
   single: field;access_class
   
.. _lino.cal.Task.access_class:

Field **Task.access_class**
===========================





Type: ChoiceListField

   
.. index::
   single: field;sequence
   
.. _lino.cal.Task.sequence:

Field **Task.sequence**
=======================





Type: IntegerField

   
.. index::
   single: field;alarm_value
   
.. _lino.cal.Task.alarm_value:

Field **Task.alarm_value**
==========================





Type: IntegerField

   
.. index::
   single: field;alarm_unit
   
.. _lino.cal.Task.alarm_unit:

Field **Task.alarm_unit**
=========================





Type: ChoiceListField

   
.. index::
   single: field;dt_alarm
   
.. _lino.cal.Task.dt_alarm:

Field **Task.dt_alarm**
=======================





Type: DateTimeField

   
.. index::
   single: field;due_date
   
.. _lino.cal.Task.due_date:

Field **Task.due_date**
=======================





Type: DateField

   
.. index::
   single: field;due_time
   
.. _lino.cal.Task.due_time:

Field **Task.due_time**
=======================





Type: TimeField

   
.. index::
   single: field;done
   
.. _lino.cal.Task.done:

Field **Task.done**
===================





Type: BooleanField

   
.. index::
   single: field;percent
   
.. _lino.cal.Task.percent:

Field **Task.percent**
======================





Type: IntegerField

   
.. index::
   single: field;status
   
.. _lino.cal.Task.status:

Field **Task.status**
=====================





Type: ChoiceListField

   
.. index::
   single: field;auto_type
   
.. _lino.cal.Task.auto_type:

Field **Task.auto_type**
========================





Type: IntegerField

   


