Version 1.3.4 (Coming)
======================

Sichtbare Änderungen
--------------------


- "in allen Personenlisten, erscheinen die Namen in Kolonne "Name" erst mit
  Vorname, was sehr verwirrend ist. Wir hätten es viel lieber wenn es mit 
  Nachname, alphabetisch anfing."

  Schreibweise des Names von Personen:
  Erstens zeigt er jetzt "NACHNAME Vorname (Nummer)" in allen Personenlisten (d.h. Kolonne `name_column`)
  Zweitens benutzt er diese gleiche Schreibweise für Personen jetzt auch
  in Auswahllisten und an diversen anderen Stellen, wo bisher
  "Vorname NACHNAME (Nummer)" verwendet wurde.
  Ich gebe zu, dass das mehr ist als angefragt war.
  Aber ich hoffe (noch), dass wir eine einheitliche Schreibweise finden. 
  Feedback erwünscht.

- Im Detail einer Art-60/7-Konvention waren die Breiten der Felder 
  der zweiten Zeile ungerecht verteilt. "Arbeitgeber" und "Vertreten durch" 
  waren seit der letzten Version breiter geworden, aber dadurch waren die 
  Felder "Stelle" und "Vertragsart" arg zusammengequetscht. 
  
- Im Detail einer Person, Reiter "Person", standen bisher zwei Felder 
  "Kartenart" mit einer Nummer und "eid-Kartenart" mit dem Text, der 
  diesem Code entspricht. Jetzt ist dort eine Combobox.

Zwei Bugs, die ich in Eupen schon manuell vor dem Release korrigiert hatte:

- Verträge konnten nicht bearbeitet werden
- Feld "Dauer (Arbeitstage)" einer Art-60/7-Konvention 
  (jobs.Contract.duration) konnte nicht ausgewählt werden



Upgrade instructions
--------------------

- Database migration required.
  See :func:`lino.apps.dsbe.migrate.migrate_from_1_3_3`.

- Lokale Datei `contacts/Person/eid-content.odt` löschen.
  