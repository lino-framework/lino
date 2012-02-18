Version 1.4.0 (Coming)
======================

Ich habe die neue Version 1.4 genannt, weil sie wieder einige schöne 
aber heftige interne Änderungen mitbringt. 
Diskussion der internen Änderungen siehe :doc:`/blog/2012/0217`.
Diesmal sind es immerhin 
"nur" Änderungen im Python-Code, weniger im Javascript-Code. 
Also leichter testbar. Trotzdem gibt es ein gewisses Bug-Risiko.

Sichtbare Änderungen
--------------------

- Man kann in Detail-Ansichten jetzt "Feldgruppen" definieren, und 
  an einigen Stellen habe ich damit begonnen. 
  Ich erwarte dazu aber auch euer Feedback. Z.B. ghört "Zivilstand" 
  eigentlich nicht in die Gruppe "Geburtsangaben"...
  
- Insgesamt lässt Lino jetzt mehr Freiraum zwischen den Feldern, 
  so dass das Gesamtbild auch für Designer etwas ansprechender wirkt.

Behobene Bugs
-------------

- Lino zeigte an gewissen Stellen immer nur maximal 5 Zeilen einer Tabelle an, 
  auch wenn es deren mehr gab.

- Wenn man z.B. eine neue Personensuche erstellte, dann sprang er nach dem Speichern 
  auf die Listenansicht zurück statt die neu erstellte Suche im Vollbild anzuzeigen.
  
- Wenn auf Seite 2 einer Liste stand und dann im Schnellsuch-Feld einen Filtertext eingab, 
  der die Liste auf weniger als eine Seite reduzierte, dann blieb er auf "Seite 2 von 1" 
  stehen und war scheinbar leer.
  Jetzt springt er nach Eingabe im Schnellsuch-Feld immer auf die erste Seite.
  
- Das Detail einer Notiz hat jetzt auch endlich blaue Hintergrundfarbe und sieht 
  jetzt aus wie es soll.

- Benutzer gerd und lsaffre erschienen fälschlicherweise bei normalen Benutzern 
  manchmal noch in der Übersichtsliste "Benutzer und ihre Klienten".
  
- Wenn man z.B. in den Fachkompetenzen oder Kursanfragen einer Person etwas 
  eingab, konnte es vorkommen, dass Lino mit "Bitte warten" steckenblieb 
  (weil er auf den AJAX-call mit "Exception Unknown action response 'errors'" 
  antwortete).
  
- Man konnte den Kursanbieter eines Kursangebotes nicht eingeben; 
  die Auswahlliste blieb leer
  (weil der Server dann ein "AttributeError 'TableRequest' object has no 
  attribute 'queryset'" machte).



Nach dem Upgrade
----------------

- Felder mit Hilfetexten haben momentan zwar ihr Label gepunktet unterstrichen, 
  aber wenn man mit der Maus drüberfährt, erscheint dennoch nicht der Hilfetext.
  Siehe :doc:`/blog/2012/0214`.

