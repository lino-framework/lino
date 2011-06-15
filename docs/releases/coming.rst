Coming
======

New features
------------

- "Integrationsphasen" haben ein neues Feld "Seq.Nr" und werden entsprechend 
  dessen Wert sortiert. N.B. damit sich das Menü verändert, muss momentan 
  der Server neugestartet werden.
  
- Lebenslauf ist jetzt eine Notizart. Also um einen Lebenslauf zu drucken: 
  Notiz erstellen, Notizart  "Lebenlauf" wählen und die Notiz drucken.

Bugs fixed
----------



Upgrade instructions
--------------------

The following are technical instructions related to this 
upgrade, designed to be executed by a Lino expert.
For more general instructions on how to upgrade an existing 
Lino site, see :doc:`/admin/upgrade`.


- "Curiculum vitae" is no longer a :class:`lino.utils.printable.DirectPrintAction`.
  Move template `cv.odt` from `persons/cv.odt` to `notes/cv.odt` and create a 
  :class:`lino.apps.dsbe.models.NoteType` using that template.
  
  


- Database migration: 

  - Field `native_language` has been removed from :class:`lino.apps.dsbe.models.Person`.
  - New field `duties_person` in :class:`lino.apps.dsbe.models.Contract`.