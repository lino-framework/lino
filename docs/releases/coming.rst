Coming
======

#.  Die provisorische Lösung aus :doc:`20110216` 
    (`knowledge_text(row.spoken)` in einer Dokumentvorlage 
    für :class:`lino.utils.printable.AppyBuildMethod`)
    ist jetzt wieder raus, denn Werte eines 
    :class:`lino.fields.KnowledgeField`
    werden nun automatisch als Text gedruckt, der 
    außerdem in der Sprache des Partners ist.
    
#.  Ich habe jetzt erstmals ein (theoretisch) vollständiges System 
    um die Bezeichnungen der Tabs eines Detailfensters zu übersetzen.


Upgrade instructions
--------------------

- Go to your local directory::

    cd /usr/local/django/myproject
    
- Stop application services::

    ./stop
    
- Update the source code::

    ./pull
    
- When a data migration is necessary, see :doc:`/admin/datamig`

