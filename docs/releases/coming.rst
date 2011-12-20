Version 1.3.1 (Coming)
======================

Sichtbare Änderungen
--------------------

- Bugfix: wenn man z.B. in 
  :menuselection:`Konfigurierung --> Eigenschaften --> Fachkompetenzen`
  das Detail eines Records anfragte, kam sogleich die Meldung
  "Keine weiteren Records, Detail wird geschlossen".
  Das lag daran, dass das Detail-Fenster die Parameter mt und mk nicht 
  richtig anfragte.
  
- Wenn in irgendeiner Tabelle eine Kolonne auf eine Person oder eine Firma 
  verwies, dann war die generell immer zu eng. Jetzt habe ich die 
  Standardbreite von 10 auf 20 Zeichen erweitert.

- Kalender

Administrator
-------------
  


Upgrade instructions
--------------------

The following are technical instructions related to this 
upgrade, designed to be executed by a Lino expert.
For more general instructions on how to upgrade an existing 
Lino site, see :doc:`/admin/upgrade`.

