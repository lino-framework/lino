Version 1.3.0 (Coming)
======================

Sichtbare Änderungen
--------------------

- Bug-Gefahr, denn es hat einige interne Optimierungen gegeben.
  Bitte gebt mir Feedback, ob Lino schneller/langsamer geworden ist.

- Optimierungen und Bugfixes beim Eingeben von Terminen.

- Passbilder sind jetzt nicht mehr verzerrt

- Da war ein Bug beim Ausfüllen einer Art60-7-Konvention. 
  ("unsupported operand type(s) for -: 'datetime.date' and 'instance'",
  :file:`/var/snapshots/lino/lino/modlib/jobs/models.py` in duration, line 367)
  Kann sein, dass das Speichern von Konventionen insgesamt nicht funktionierte.

- In der oberen rechten Ecke ist jetzt ein Button mit dem Benutzernamen. 
  Wenn man darauf klickt, kann man seine Benutzerdaten ändern.
  

Administrator
-------------
  


Upgrade instructions
--------------------

The following are technical instructions related to this 
upgrade, designed to be executed by a Lino expert.
For more general instructions on how to upgrade an existing 
Lino site, see :doc:`/admin/upgrade`.

