Coming
======

#.  Änderungen im Hauptmenü:

    - Das (Konfigurierung) ist jetzt strukturiert, 
      weil es unübersichtlich wurde. 
      Ich habe mal einen schnellen Vorschlag gemacht. Feedback willkommen.
    
    - Ich habe es jetzt (zum Probieren) mal so gemacht, dass das Hauptmenü 
      über Permalinks funktioniert. Das hat vor allem zur Folge, dass alle 
      offenen Fenster geschlossen werden, wenn man aus dem Hauptmenü einen 
      Befehl wählt. 
    
    - Außerdem gibt es jetzt einen Button "Anfang", mit dem man in den 
        Anfangsbildschirm (mit den Erinnerungen) zurückgelangt.

New features
------------


Bugs fixed
----------


Upgrade instructions
--------------------

- Go to your local directory::

    cd /usr/local/django/myproject
    
- Stop application services::

    ./stop
    
- Update the source code::

    ./pull
    
- When a data migration is necessary, see :doc:`/admin/datamig`

