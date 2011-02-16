Coming
======

#.  Der "Änderungen-Speichern ?"-Bug ist behoben.
#.  Die beiden Felder 
    :attr:`noble_condition <lino.modlib.dsbe.models.Person.noble_condition>` 
    und     
    :attr:`card_issuer <lino.modlib.dsbe.models.Person.card_issuer>` 
    sind jetzt readonly (bei importierten Personen).


Upgrade instructions
--------------------

- Go to your local directory::

    cd /usr/local/django/myproject
    
- Stop application services::

    ./stop
    
- Update the source code::

    ./pull
    
- When a data migration is necessary, see :doc:`/admin/datamig`

