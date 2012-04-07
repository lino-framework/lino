Coming
======


- Neue Tabelle 
  :class:`Offene Kursanfragen 
  <lino.apps.pcsw.courses.models.PendingCourseRequests>`.


Bugfixes
--------

- Felder eID-Karte gültig von und gültig bis waren zu klein.

- Wenn man z.B. in der Liste der Stellen 
  auf einen Stellenanbieter klickte um dessen Detail zu sehen, 
  kam stattdessen ein Traceback auf dem Server.
  (:doc:`/blog/2012/0305`)
  
- Die "(zeigen)"-Links im Detail Organisation und Person 
  funktionierten nicht. 
  (:doc:`/blog/2012/0305`)
  
- "Remote fields" funktionierte noch nicht. 
  Kamen allerdings bisher erst in 
  :menuselection:`Stellen --> Suche Art-60-7-Konventionen` vor (Kolonnen Stadt, NR-Nummer und Geschlecht)

- Clicking the :guilabel:`[html]` button on that table causes a server traceback.
  

Internal changes
----------------

Administrators need to ``aptitude install python-lxml`` before upgrading.
:mod:`lino.utils.xmlgen` turned out to be a reinvention of the wheel 
and has been replaced by `lxml <http://www.lxml.de>`_.

