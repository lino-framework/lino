Version 1.2.3 (Coming)
======================

New features
------------

- Wortschatz: statt "Stellenanbieter" heißt es jetzt "Arbeitgeber".

- Neue Tabellen "Sektoren" und "Funktionen" 
  (beide im Menü `Konfigurierung -->Stellen`) 
  sowie "Berufswünsche" (im Reiter "Stellenanfragen" 
  des Details einer Person).

- In "Berufserfahrungen" kann man nun ebenfalls (optional) 
  Sektor und Funktion eingeben.

- Im Hauptbildschirm habt ihr jetzt eine Liste von "Quick Links", 
  dich ich euch leicht wunschgerecht anpassen kann
  (momentan noch nicht benutzerspezifisch).
  
- Der Reiter "Contracts" heißt jetzt "Verträge" und enthält *nur noch* 
  die VSE- und Arbeitsverträge. Stellenanfragen stehen jetzt 
  zusammen mit den Berufswünschen in einem neuen Reiter 
  namens "Stellenanfragen".
  
- Der Reiter "Eigenschaften" wurde umbenannt in  "Kompetenzen".

- Der Reiter "Dokumente" wurde umbenannt in  "Chronik".

- Die Reihenfolge der Reiter ist jetzt wie folgt: 
  Person, Status, 
  Ausbildung, Sprachen, Kompetenzen,
  Stellenanfragen, Verträge, Chronik, 
  Kalender, Korrespondenz, Sonstiges

- Folgende neue Möglichkeiten werdet ihr nicht benutzen 
  (aber ich halte sie nicht für störend):

  - Neue Tabelle :menuselection:`Stellen --> Stellenangebote`
    (wird in Brüssel gebraucht für externe Stellenangebote)
  - Neue Tabelle :menuselection:`Korrespondenz --> Dokumentarten`
    (experimentell, :class:`MailType <lino.modlib.mails.models.MailType>`)

- Ich hielt es für nötig, im Hauptmenü ein paar Änderungen zu machen:

  - "Stellenanbieter" nicht mehr unter "Kontakte", sondern in eigenem 
    Menü "Stellen", zusammen mit dem neuen Befehl "Stellenangebote".
  - "Kursanbieter" nicht mehr unter "Kontakte", sondern im 
    Menü "Kurse". 
  - "Kursinhalte" und "Kursbeendigungen" stehen jetzt 
    *nicht* mehr im Menü "Kurse", sondern im neuen Menü 
    :menuselection:`Konfigurierung --> Kurse`.
    
- Im Listing :class:`Übersicht Verträge 
  <lino.modlib.jobs.models.ContractsSituation>` sind die Stellen jetzt 
  pro Arbeitgeber gruppiert.
  
  
Bugs fixed
----------

- watch_tim : Partner aus TIM werden nach Eingabe MwSt-Nr. 
  keine Organisation (bzw. nach Löschen der MWSt-Nr keine Person). 
  Beispiele: Mosaik, Frauenliga,...
  Siehe :doc:`/blog/2011/0928`.
  
- :menuselection:`Kontakte --> Alle Kontakte`: 
  In dieser Liste konnte man importierte Partner bearbeiten.
  Behoben.
  Siehe :doc:`/blog/2011/0928`.
  
- Wenn man z.B. die Combobox in "Kontaktpersonen"  aufklappte, ohne vorher 
  ein paar Buchstaben des gesuchten Namens eingegeben zu haben, dann konnte 
  das u.U. (in Google Chrome Version 12) zu einer Fehlermeldung "Seiten reagieren nicht" führen. Lag daran, dass choices_view die Parameter `start` und `limit` ignorierte. Siehe :doc:`/blog/2011/0929`.
  
- Filter setzen auf einer Datum-Kolonne funktionierte nicht. 
  Behoben.  
  
- ForeignKey-Kolonnen einer Grid haben unnützerweise eine Lupe. 
  Die sollte nur in ForeignKey-Feldern eines Details da sein.
  
- Beim Speichern eines Vertrags (Bsp. Arbeitsvertrag #140) wurde 
  die Kontaktperson nicht gespeichert.
  
- Die Bezeichnung einer Stelle (in Auswahlliste) enthält jetzt auch den 
  Namen des Arbeitsgebers.
  
- Die Übersicht der Verträge wird jetzt in Landscape ausgedruckt.
  


Administrator
-------------

- Die Tabellen hinter "Form" und "Inhalt" einer Notiz wurden ausgetauscht. 
  Also das Feld "Inhalt" bestimmt jetzt, welche Dokumentvorlage benutzt wird.
  Notizarten werden 
  "Lebenslauf" muss manuell von "Notizarten" nach "Ereignisarten" 
  verschoben werden.
  
- Konfigurierung Stellen : hier muss jetzt der Name des AG aus der 
  Bezeichnung der Stelle rausgenommen werden. 

Upgrade instructions
--------------------

The following are technical instructions related to this 
upgrade, designed to be executed by a Lino expert.
For more general instructions on how to upgrade an existing 
Lino site, see :doc:`/admin/upgrade`.

