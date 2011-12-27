Version 1.3.3 (Coming)
======================

Sichtbare Änderungen
--------------------

- (bugfix) eID-Kartenart (card_type) war bei importierten Partnern 
  nicht schreibgeschützt. Behoben.

- (bugfix) Stundensatz einer Stelle: 
  Hier konnte man keine Nachkommastellen eingeben. Behoben.
  New Lino configuration attribute :attr:`lino.Lino.decimal_separator`.  
  
- Neue Kolonnen "Aktive Akten" und "Komplette Akten" in der 
  Übersicht 
  :func:`Klienten pro Benutzer <lino.apps.dsbe.models.persons_by_user>`.
  Neues Feld `PersonGroup.active`.
  
- Auswertungsstrategien "wöchentlich" oder "zweiwöchentlich" sind nun möglich.
  Neues Feld `isip.ExamPolicy.every_unit`.
  
- Wenn man das Datum eines automatisch generierten Termins verschiebt, dann 
  passt Lino nun alle folgenden Termine automatisch dem neuen Datum an
  (zumindest die, die noch nicht bestätigt oder sonstwie bearbeitet sind).
  
- N.B.: Lino macht momentan immer höchstens 24 automatische Auswertungstermine.
  Das ist ein hardcodierter Grenzwert, den ich auf Wunsch auch (a) ändern oder 
  gar (b) konfigurierbar machen kann.
  


Upgrade instructions
--------------------

Database migration required.
See :func:`lino.apps.dsbe.migrate.migrate_from_1_3_2`.