Version 1.2.2 (Coming)
======================

New features
------------

#.  provider und contracttype einer Stelle dürfen jetzt nicht mehr geändert werden, 
    wenn mindestens ein Vertrag mit dieser existiert.     
    Benutzerdoku: Was tun (vor allem jetzt nach der Datenmigration), 
    wenn diese Felder einer Stelle de facto falsch sind und korrigiert 
    werden müssen?
    --> Neue Stelle mit richtigen Daten schaffen, 
    dann in allen Verträgen die neue Stelle zuweisen.
    
#.  In Grids, die ein unformatiertes TextField enthielten, konnte man 
    auch in anderen Zellen weder bearbeiten noch Zeilen einfügen, 
    weil er dann fälschlicherweise versuchte, 
    `Ext.form.TextArea.refresh()` aufzurufen.
    
#.  Die "seltsamen AJAX failure" beim Bearbeiten der Stelle eines Vertrags
    haben eine einfache Erklärung und Lösung. 
    Siehe :doc:`/blog/2011/0727`.
    
#.  Der Menübefehl für die Liste der Stellenanbieter ist jetzt nicht mehr unter 
    :menuselection:`Kurse --> Stellenanbieter`, 
    sondern ebenfalls in :menuselection:`Konfigurierung --> Stellen --> Stellenanbieter`.


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

