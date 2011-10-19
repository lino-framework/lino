Version 1.2.4 (Coming)
======================

New features
------------

- In der oberen Toolbar von Detail-Fenstern wurde das Feld für Schnellsuche 
  und den Button zum Export einer csv-Datei rausgeholt, weil das dort 
  nicht sehr sinnnvoll war.  
  Die beiden sind also nur noch in der Listenansicht vorhanden.
  
- In Detail-Fenstern haben wir jetzt eine neue Combobox "Gehe zu Datensatz".

- Lino kann Detail-Fenster jetzt direkt vom Menü aus aufrufen, ohne vorher 
  eine Tabellenansicht zu öffnen. 
  Der Quick Link "Detail Personen" ist ein Beispiel dafür.
  
- Neues Ankreuzfeld "DSBE-Benutzer" in der Benutzertabelle.
  Für Benutzer gibt es jetzt auch eine Detail-Ansicht.

  
Bugs fixed
----------

- Automatische Aufgaben wurden nicht immer korrekt ihrer Person zugewiesen.
- Aufgaben wurden im Rückblick/Ausblick ohne den Namen der Person angezeigt.
- Manuell erstellte aufgaben hatten das Doppelfeld Erinnern (Wert, Einheut) leer.
- AttributeError “Manager isn’t accessible via Third instances” at /api/thirds/ThirdsByOwner (when trying to add a new record in ThirdsByOwner.
- Ausdrucken Personensuche funktionierte nicht.

Administrator
-------------

Upgrade instructions
--------------------

The following are technical instructions related to this 
upgrade, designed to be executed by a Lino expert.
For more general instructions on how to upgrade an existing 
Lino site, see :doc:`/admin/upgrade`.

