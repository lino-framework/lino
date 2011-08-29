===
cal
===



.. currentmodule:: cal

Defined in :srcref:`/lino/modlib/cal/models.py`


This module defines models :class:`Calendar`, :class:`Task` and :class:`Event`.
And :class:`EventType`, :class:`Place`



.. contents:: Table of Contents



.. index::
   pair: model; Calendar

.. _lino.cal.Calendar:

------------------
Model **Calendar**
------------------




A Calendar is a collection of events and tasks.
There are local calendars and remote calendars.
Remote calendars will be synchronized by
:mod:`lino.modlib.cal.management.commands.watch_calendars`,
and local modifications will be sent back to the remote calendar.

  
============ ============= ===========================
name         type          verbose name               
============ ============= ===========================
id           AutoField     ID                         
user         ForeignKey    User (Benutzer,Utilisateur)
type         CharField     Type                       
name         CharField     Name (Nom)                 
url_template CharField     URL template               
username     CharField     Username                   
password     PasswordField Password                   
readonly     BooleanField  read-only                  
is_default   BooleanField  is default                 
start_date   DateField     Start date (Beginnt am)    
============ ============= ===========================

    
Defined in :srcref:`/lino/modlib/cal/models.py`

Referenced from
`lino.cal.RecurrenceSet.calendar`_, `lino.cal.Event.calendar`_, `lino.cal.Task.calendar`_



.. index::
   single: field;id
   
.. _lino.cal.Calendar.id:

Field **Calendar.id**
=====================





Type: AutoField

   
.. index::
   single: field;user
   
.. _lino.cal.Calendar.user:

Field **Calendar.user**
=======================





Type: ForeignKey

   
.. index::
   single: field;type
   
.. _lino.cal.Calendar.type:

Field **Calendar.type**
=======================





Type: CharField

   
.. index::
   single: field;name
   
.. _lino.cal.Calendar.name:

Field **Calendar.name**
=======================





Type: CharField

   
.. index::
   single: field;url_template
   
.. _lino.cal.Calendar.url_template:

Field **Calendar.url_template**
===============================





Type: CharField

   
.. index::
   single: field;username
   
.. _lino.cal.Calendar.username:

Field **Calendar.username**
===========================





Type: CharField

   
.. index::
   single: field;password
   
.. _lino.cal.Calendar.password:

Field **Calendar.password**
===========================





Type: PasswordField

   
.. index::
   single: field;readonly
   
.. _lino.cal.Calendar.readonly:

Field **Calendar.readonly**
===========================





Type: BooleanField

   
.. index::
   single: field;is_default
   
.. _lino.cal.Calendar.is_default:

Field **Calendar.is_default**
=============================





Type: BooleanField

   
.. index::
   single: field;start_date
   
.. _lino.cal.Calendar.start_date:

Field **Calendar.start_date**
=============================





Type: DateField

   


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



Deserves more documentation.
  
============ ============== ===========================================================
name         type           verbose name                                               
============ ============== ===========================================================
id           AutoField      ID                                                         
name         BabelCharField Designation (Beschreibung,Désignation)                     
build_method CharField      Build method (Konstruktionsmethode,Méthode de construction)
template     CharField      Template (Vorlage,Modèle)                                  
name_fr      CharField      Designation (fr)                                           
name_nl      CharField      Designation (nl)                                           
name_en      CharField      Designation (en)                                           
============ ============== ===========================================================

    
Defined in :srcref:`/lino/modlib/cal/models.py`

Referenced from
`lino.cal.Event.type`_



.. index::
   single: field;id
   
.. _lino.cal.EventType.id:

Field **EventType.id**
======================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.cal.EventType.name:

Field **EventType.name**
========================





Type: BabelCharField

   
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
   pair: model; RecurrenceSet

.. _lino.cal.RecurrenceSet:

-----------------------
Model **RecurrenceSet**
-----------------------




Groups together all instances of a set of recurring calendar components.

Thanks to http://www.kanzaki.com/docs/ical/rdate.html


  
=========== ============= ==========================
name        type          verbose name              
=========== ============= ==========================
id          AutoField     ID                        
calendar    ForeignKey    Calendar (Kalender)       
uid         CharField     UID                       
start_date  DateField     Start date (Beginnt am)   
start_time  TimeField     Start time (Beginnt um)   
summary     CharField     Summary (Kurzbeschreibung)
description RichTextField Description (Beschreibung)
rdates      TextField     Recurrence dates          
exdates     TextField     Excluded dates            
rrules      TextField     Recurrence Rules          
exrules     TextField     Exclusion Rules           
=========== ============= ==========================

    
Defined in :srcref:`/lino/modlib/cal/models.py`

Referenced from
`lino.cal.Event.rset`_, `lino.cal.Task.rset`_



.. index::
   single: field;id
   
.. _lino.cal.RecurrenceSet.id:

Field **RecurrenceSet.id**
==========================





Type: AutoField

   
.. index::
   single: field;calendar
   
.. _lino.cal.RecurrenceSet.calendar:

Field **RecurrenceSet.calendar**
================================





Type: ForeignKey

   
.. index::
   single: field;uid
   
.. _lino.cal.RecurrenceSet.uid:

Field **RecurrenceSet.uid**
===========================





Type: CharField

   
.. index::
   single: field;start_date
   
.. _lino.cal.RecurrenceSet.start_date:

Field **RecurrenceSet.start_date**
==================================





Type: DateField

   
.. index::
   single: field;start_time
   
.. _lino.cal.RecurrenceSet.start_time:

Field **RecurrenceSet.start_time**
==================================





Type: TimeField

   
.. index::
   single: field;summary
   
.. _lino.cal.RecurrenceSet.summary:

Field **RecurrenceSet.summary**
===============================





Type: CharField

   
.. index::
   single: field;description
   
.. _lino.cal.RecurrenceSet.description:

Field **RecurrenceSet.description**
===================================





Type: RichTextField

   
.. index::
   single: field;rdates
   
.. _lino.cal.RecurrenceSet.rdates:

Field **RecurrenceSet.rdates**
==============================





Type: TextField

   
.. index::
   single: field;exdates
   
.. _lino.cal.RecurrenceSet.exdates:

Field **RecurrenceSet.exdates**
===============================





Type: TextField

   
.. index::
   single: field;rrules
   
.. _lino.cal.RecurrenceSet.rrules:

Field **RecurrenceSet.rrules**
==============================





Type: TextField

   
.. index::
   single: field;exrules
   
.. _lino.cal.RecurrenceSet.exrules:

Field **RecurrenceSet.exrules**
===============================





Type: TextField

   


.. index::
   pair: model; GuestRole

.. _lino.cal.GuestRole:

-------------------
Model **GuestRole**
-------------------




A possible value for the `role` field of an :class:`Guest`.


  
======= ============== ======================================
name    type           verbose name                          
======= ============== ======================================
id      AutoField      ID                                    
name    BabelCharField Designation (Beschreibung,Désignation)
name_fr CharField      Designation (fr)                      
name_nl CharField      Designation (nl)                      
name_en CharField      Designation (en)                      
======= ============== ======================================

    
Defined in :srcref:`/lino/modlib/cal/models.py`

Referenced from
`lino.cal.Guest.role`_



.. index::
   single: field;id
   
.. _lino.cal.GuestRole.id:

Field **GuestRole.id**
======================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.cal.GuestRole.name:

Field **GuestRole.name**
========================





Type: BabelCharField

   
.. index::
   single: field;name_fr
   
.. _lino.cal.GuestRole.name_fr:

Field **GuestRole.name_fr**
===========================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _lino.cal.GuestRole.name_nl:

Field **GuestRole.name_nl**
===========================





Type: CharField

   
.. index::
   single: field;name_en
   
.. _lino.cal.GuestRole.name_en:

Field **GuestRole.name_en**
===========================





Type: CharField

   


.. index::
   pair: model; Guest

.. _lino.cal.Guest:

---------------
Model **Guest**
---------------




A Guest is a Contact who is invited to an :class:`Event`.

  
========== =============== ======================================================
name       type            verbose name                                          
========== =============== ======================================================
id         AutoField       ID                                                    
must_build BooleanField    must build (muss generiert werden,doit être construit)
contact    ForeignKey      Contact (Kontakt)                                     
language   LanguageField   Language (Sprache,Langue)                             
event      ForeignKey      Event (Termin)                                        
role       ForeignKey      Guest Role                                            
status     ChoiceListField Guest Status                                          
remark     CharField       Remark (Bemerkung,Remarque)                           
========== =============== ======================================================

    
Defined in :srcref:`/lino/modlib/cal/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.cal.Guest.id:

Field **Guest.id**
==================





Type: AutoField

   
.. index::
   single: field;must_build
   
.. _lino.cal.Guest.must_build:

Field **Guest.must_build**
==========================





Type: BooleanField

   
.. index::
   single: field;contact
   
.. _lino.cal.Guest.contact:

Field **Guest.contact**
=======================





Type: ForeignKey

   
.. index::
   single: field;language
   
.. _lino.cal.Guest.language:

Field **Guest.language**
========================





Type: LanguageField

   
.. index::
   single: field;event
   
.. _lino.cal.Guest.event:

Field **Guest.event**
=====================





Type: ForeignKey

   
.. index::
   single: field;role
   
.. _lino.cal.Guest.role:

Field **Guest.role**
====================





Type: ForeignKey

   
.. index::
   single: field;status
   
.. _lino.cal.Guest.status:

Field **Guest.status**
======================





Type: ChoiceListField

   
.. index::
   single: field;remark
   
.. _lino.cal.Guest.remark:

Field **Guest.remark**
======================





Type: CharField

   


.. index::
   pair: model; Event

.. _lino.cal.Event:

---------------
Model **Event**
---------------



Event(id, user_id, created, modified, project_id, must_build, calendar_id, uid, start_date, start_time, summary, description, access_class, sequence, alarm_value, alarm_unit, dt_alarm, user_modified, rset_id, end_date, end_time, transparent, type_id, place_id, priority, status, duration_value, duration_unit)
  
============== =============== ======================================================
name           type            verbose name                                          
============== =============== ======================================================
id             AutoField       ID                                                    
user           ForeignKey      User (Benutzer,Utilisateur)                           
created        DateTimeField   created                                               
modified       DateTimeField   modified                                              
project        ForeignKey      Person (Personne)                                     
must_build     BooleanField    must build (muss generiert werden,doit être construit)
calendar       ForeignKey      Calendar (Kalender)                                   
uid            CharField       UID                                                   
start_date     DateField       Start date (Beginnt am)                               
start_time     TimeField       Start time (Beginnt um)                               
summary        CharField       Summary (Kurzbeschreibung)                            
description    RichTextField   Description (Beschreibung)                            
access_class   ChoiceListField Access Class (Zugriffsklasse)                         
sequence       IntegerField    Revision (Revisionsnummer)                            
alarm_value    IntegerField    Value (Wert,Valeur)                                   
alarm_unit     ChoiceListField Unit                                                  
dt_alarm       DateTimeField   Alarm time                                            
user_modified  BooleanField    modified by user                                      
rset           ForeignKey      Recurrence Set                                        
end_date       DateField       End date (Endet am)                                   
end_time       TimeField       End time (Endet um)                                   
transparent    BooleanField    Transparent (nicht blockierend)                       
type           ForeignKey      Event Type (Ereignisart,Type d'événement)             
place          ForeignKey      Place (Ort)                                           
priority       ChoiceListField Priority (Priorität)                                  
status         ChoiceListField Status (Statut)                                       
duration_value IntegerField    Value (Wert,Valeur)                                   
duration_unit  ChoiceListField Unit                                                  
============== =============== ======================================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from
`lino.cal.Guest.event`_



.. index::
   single: field;id
   
.. _lino.cal.Event.id:

Field **Event.id**
==================





Type: AutoField

   
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
   single: field;project
   
.. _lino.cal.Event.project:

Field **Event.project**
=======================





Type: ForeignKey

   
.. index::
   single: field;must_build
   
.. _lino.cal.Event.must_build:

Field **Event.must_build**
==========================





Type: BooleanField

   
.. index::
   single: field;calendar
   
.. _lino.cal.Event.calendar:

Field **Event.calendar**
========================





Type: ForeignKey

   
.. index::
   single: field;uid
   
.. _lino.cal.Event.uid:

Field **Event.uid**
===================





Type: CharField

   
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
   single: field;user_modified
   
.. _lino.cal.Event.user_modified:

Field **Event.user_modified**
=============================





Type: BooleanField

   
.. index::
   single: field;rset
   
.. _lino.cal.Event.rset:

Field **Event.rset**
====================





Type: ForeignKey

   
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
   single: field;type
   
.. _lino.cal.Event.type:

Field **Event.type**
====================





Type: ForeignKey

   
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
   pair: model; Task

.. _lino.cal.Task:

--------------
Model **Task**
--------------



Task(id, user_id, created, modified, owner_type_id, owner_id, project_id, calendar_id, uid, start_date, start_time, summary, description, access_class, sequence, alarm_value, alarm_unit, dt_alarm, user_modified, rset_id, due_date, due_time, done, percent, status, auto_type)
  
============= ======================== =================================================
name          type                     verbose name                                     
============= ======================== =================================================
id            AutoField                ID                                               
user          ForeignKey               User (Benutzer,Utilisateur)                      
created       DateTimeField            created                                          
modified      DateTimeField            modified                                         
owner_type    ForeignKey               Owner type (Besitzertabelle,type de propriétaire)
owner_id      GenericForeignKeyIdField Owner (Besitzer,Propriétaire)                    
project       ForeignKey               Person (Personne)                                
calendar      ForeignKey               Calendar (Kalender)                              
uid           CharField                UID                                              
start_date    DateField                Start date (Beginnt am)                          
start_time    TimeField                Start time (Beginnt um)                          
summary       CharField                Summary (Kurzbeschreibung)                       
description   RichTextField            Description (Beschreibung)                       
access_class  ChoiceListField          Access Class (Zugriffsklasse)                    
sequence      IntegerField             Revision (Revisionsnummer)                       
alarm_value   IntegerField             Value (Wert,Valeur)                              
alarm_unit    ChoiceListField          Unit                                             
dt_alarm      DateTimeField            Alarm time                                       
user_modified BooleanField             modified by user                                 
rset          ForeignKey               Recurrence Set                                   
due_date      DateField                Due date (Fällig am,Terme)                       
due_time      TimeField                Due time (Fällig um)                             
done          BooleanField             Done (Erledigt,Fait)                             
percent       IntegerField             Duration value (Dauer (Anzahl))                  
status        ChoiceListField          Task Status (Aufgabenstatus)                     
auto_type     IntegerField             auto type                                        
============= ======================== =================================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.cal.Task.id:

Field **Task.id**
=================





Type: AutoField

   
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
   single: field;project
   
.. _lino.cal.Task.project:

Field **Task.project**
======================





Type: ForeignKey

   
.. index::
   single: field;calendar
   
.. _lino.cal.Task.calendar:

Field **Task.calendar**
=======================





Type: ForeignKey

   
.. index::
   single: field;uid
   
.. _lino.cal.Task.uid:

Field **Task.uid**
==================





Type: CharField

   
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
   single: field;user_modified
   
.. _lino.cal.Task.user_modified:

Field **Task.user_modified**
============================





Type: BooleanField

   
.. index::
   single: field;rset
   
.. _lino.cal.Task.rset:

Field **Task.rset**
===================





Type: ForeignKey

   
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

   


