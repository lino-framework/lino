Version 1.2.2 (Coming)
======================

New features
------------

#.  Es gibt jetzt zwei Arten von Verträgen: VSE-Verträge 
    (:class:`lino.modelib.isip.models.Contract`) 
    und Arbeitsverträge 
    (:class:`lino.modelib.jobs.models.Contract`).
    Dass die bisher in einer einzigen Tabelle waren, war 
    offenbar ein Analysefehler.
    Beide Modelle haben zwar eine Serie von gemeinsamen Feldern 
    (:class:`lino.modelib.isip.models.ContractBase`),
    aber eine gemeinsame Historik ist nicht nötig
    (sondern die Benutzer wollen die beiden lieber klar getrennt 
    haben in zwei Tabellen im Reiter "Verträge" einer Person)

#.  Das Feld "Stelle" eines Arbeitsvertrags ist jetzt nicht mehr 
    obligatorisch. 
    Solche Verträge ohne Stelle erscheinen dann nicht im 
    Listing :mod:`Übersicht Verträge 
    <lino.modlib.jobs.models.ContractsOverview>`.

#.  :class:`lino.fields.FieldSet`.
    Im Detail-Fenster Personen (Reiter 1 unten) sind die Felder zur 
    eID-Karte jetzt optisch zu einer Feldgruppe zusammengefasst.
    Falls ihr noch Ideen habt, wo dieses neue Feature nützlich wäre: 
    melden.
    
#.  New table `Contacts` contains both Persons and Companies.

    Also es gibt jetzt eine Liste, in der Personen, Organisationen 
    und Benutzer zusammengefasst sind:
    :menulabel:`Kontakte --> Alle Kontakte`
    
#.  Calendar module is growing. Attendances by Event. 

#.  New module "Emails". "Create Mail" button. Incoming and outgoing mails.

#.  out-of-the-box doctemplates

Internal optimizations
----------------------

Bugs fixed
----------

Upgrade instructions
--------------------

The following are technical instructions related to this 
upgrade, designed to be executed by a Lino expert.
For more general instructions on how to upgrade an existing 
Lino site, see :doc:`/admin/upgrade`.

#.  Reorganize local :xfile:`doctemplates` directory 
    (see in :doc:`/blog/2011/0809`). Concretely::
    
      mkdir config/jobs
      mkdir config/jobs/Contract
      mv media/webdav/doctemplates/appy/de/contracts/
      mv media/webdav/doctemplates/appy/de/contracts/art60-7.odt  config/jobs/Contract
      mv media/webdav/doctemplates/appy/de/contracts/vse.odt  config/jobs/Contract 
    

#.  Lino/DSBE users must run a database migration because 
    we now also use the :mod:`lino.modlib.mails` module. 

