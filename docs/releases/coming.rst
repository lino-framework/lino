Version 1.3.8 (Coming)
======================

Sichtbare Änderungen
--------------------

- Vertragsüberschneidungen: ich habe den Test noch strenger gemacht: 
  Verträge müssen 
  jetzt außerdem auch innerhalb der Begleitperiode des Klienten sein. 
  Wobei letztere nach hinten oder vorne hin offen sein kann 
  (eines der Daten darf leer sein).
  Weil beide Tests technisch gesehen "zugleich" stattfinden, 
  müsst ihr auch noch diese Fehlermeldungen ausmerzen, bevor ich den Test 
  obligatorisch machen kann.
  N.B.: wenn dieser Test obligatorisch ist, wird die entsprechende Option 
  aus der Datenkontrollliste verschwinden da unnötig.
  
- Der [pdf]-Button funktioniert jetzt... 

  ... mit zwei offenen Problemen:

  - Wenn zwei Benutzer die gleiche Tabelle gleichzeitig ausdrucken, 
    gibt es Probleme, weil er auf dem Server immer den gleichen Namen nimmt 
    für die temporäre Datei. 
    
  - Tabellen wie `Personen` haben sehr viele Kolonnen, so dass das Resultat 
    lustig aussieht aber nicht sehr nützlich ist.
    Lösungswege: 
    
    - bei solchen Listen insgesamt die Kolonnenzahl reduzieren.
    - Pro Kolonne konfigurieren können, ob sie (1) am Bildschirm, 
      (2) in der .csv-Datei, (3) in der .pdf-Datei erscheinen 
      soll oder nicht.


Upgrade instructions
--------------------

