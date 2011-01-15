Einführung
==========

Das folgende Dokument ist als Wegweiser für die 
Benutzer während der ersten Woche mit Lino gedacht.

Personen
--------

- :menuselection:`Kontakte --> Personen` zeigt alle Personen
- :menuselection:`Notizen --> Von mir begleitete Personen` 
  zeigt nur die Personen, bei denen ich im Reiter "Person 2" 
  als Begleiter 1 oder 2 eingetragen bin.


Die begleiteten Personen werden in einer Datenbank erfasst, 
die automatisch aus TIM importiert wird. 
Die importierten Angaben können in Lino nicht bearbeitet werden 
(werden am Bildschirm blau dargestellt).

Zusätzlich zu den aus TIM importierten Angaben über eine Person 
werden weitere Angaben erfasst:

   - Sprachkenntnisse
   - Erfahrungen (Beruf, Schule, Ausbildung, Sonstige)
   - Hindernisse bei Arbeitssuche
   
**Übung** Jemand hat die falsche Telefonnummer oder Adresse.
Partner in TIM bearbeiten. 
In Lino auf "Refresh" klicken.
Angaben in Lino werden automatisch synchronisiert.

Das bisherige "Individuelle Auskunftsblatt" 
braucht nicht mehr manuell ausgefüllt zu werden.
Einfacher ist es, die Angaben gleich am Bildschirm einzugeben.
Anschließend kann man jederzeit von Lino ein 
Auskunftsblatt ausdrucken lassen.

- **Auskunftsblatt ausdrucken**: 
  Dazu muss man im Reiter Notizen eine neue Notiz einfügen.
  Die Notiz an sich ist leer, du wählst lediglich als Notizart "Auskunftsblatt" aus. Dann :guilabel:`Speichern` und :guilabel:`Drucken`.
  
Die Tatsache, dass du etwas über die Person ausdruckst, 
ist eine "Notiz" und wird als solche in der Datenbank gespeichert.
Wenn du nach dem Ausdruck eine Angabe änderst, 
bleibt die Notiz mit dem generierten Dokument erhalten.

Wir haben auch erwägt, ob wir statt "Notiz" nicht lieber "Ereignis" nehmen sollten. 

**Übung** Nimm dir eine von dir begleiteten Personen vor und "bring deren Dossier in Ordnung", so dass am Ende ein korrektes Auskunftsblatt ausgedruckt wird.

Firmen
------

Eigentlich müsste dieser Menüpunkt "Organisationen" heißen, 
denn hier sind nicht nur Firmen, sondern auch Vereine, Betriebe, Stadtverwaltungen, Ministerien, Dienste, ...
Wir haben "Firmen" gewählt weil uns das "praktischer" erschien.

Firmen sind ebenfalls aus TIM importiert und können dann in Lino nicht bearbeitet werden.

Es gibt noch einige Fälle von Firmen, die in Lino als Person stehen und umgekehrt. Das kommt daher, dass TIM diese beiden etwas zu sehr in den gleichen Topf wirft.


Kontaktpersonen
---------------

Man kann in Lino Personen erstellen. 
Z.B. den Direktor einer Firma, 
der auf einem Vertrag erscheinen muss 
und ansonsten voraussichtlich 
nie etwas mit dem ÖSHZ zu tun haben wird.

**Übung**: Nennt ein paar Beispiele von Leuten, 
die ihr anrufen müsst. 
Wo sind sie gespeichert? 
Wie findet ihr deren Telefonnumer?
Nach welchen Regeln sollen wir ggf. entscheiden, 
ob eine Person in TIM oder nur in Lino erfasst werden soll?


Meine Leute finden
------------------

- :menuselection:`Mein Menü --> von mir begleitete Personen`

Damit eine Person in dieser Liste erscheint, muss

(1) ich als (mindestens) einer der beiden Begleiter angegeben sein
(2) das heutige Tagesdatum in den Begleitungszeitraum fallen

Der Begleitungszeitraum definiert sich wie folgt ausgehend von 
den Feldern "Begleitet seit" und "Begleitet bis":

- beide Felder leer : wird nicht begleitet
- "seit" leer und "bis" ausgefüllt : wird/wurde begleitet bis zum
  angegebenen Datum (Anfangsdatum unbekannt)
- "seit" ausgefüllt und "bis" leer : wird seit dem angegebenen 
  Datum ad eternum begleitet.
- beide Felder ausgefüllt : wir begleitet mit voraussichtlichem 
  Enddatum.

Verträge
--------

Verträge können wie folgt eingesehen / gesucht / erfasst werden:

- Im Reiter "Notizen" einer Person stehen alle Verträge, 
  die für diese Person erfasst wurden.
- Im Reiter "Notizen" einer Firma stehen alle Verträge, 
  die mit dieser Firma erfasst wurden.
- In :menuselection:`Mein Menü --> Meine Verträge` stehen alle Verträge, 
  deren Autor ich bin (d.h. deren Feld "Benutzer (DSBE)" mich enthält).
  
  

Erinnerungen
------------

Im Hauptmenü zeigt Lino automatisch "Erinnerungen" an.

Das geplante Feature, dass man Erinnerungen per Mausklick
als "gelesen" markieren kann, ist momentan noch nicht gemacht.
Kann sein, dass die Präsentierung demnächst viel luxuriöser in 
Form eines Kalenders kommt. 

Uploads, Links, Notizen und Verträge haben ein Feld "Fällig am".
Wenn dieses Feld ausgefüllt ist, wird aus diesem Upload (Link, Notiz oder 
Vertrag) eine Erinnerung.

Optional kann man zusätzlich das Datum der Erinnerung nach vorne 
verschieben.
Um z.B. 2 Monate vor dem Fälligkeitsdatum erinnert zu werden, trägt 
man in "Frist (Wert)" 2 ein und setzt "Frist (Art)" auf "Monat".

Bei Uploads (eingescannten Dokumenten), die nur bis zu einem 
bestimmten Datum gültig sind, trägt man in "Fällig am" das 
tatsächliche datum "Gültig-bis" des Originaldokuments ein und 
benutzt die Frist, um die Erinnerung zeitig genug erscheinen zu 
lassen. 


Folgende Datumsfelder in den direkten Personenstammdaten führen 
(wenn sie ausgefüllt sind) zu automatischen Erinnerungen:

===================== ========= ====================================
Datumsfeld            Frist     Erinnerungstext
===================== ========= ====================================
Nicht verfügbar bis   30 Tage   Person wieder verfügbar ab x
Wartezeit bis         30 Tage   Wartezeit Arbeitssuche endet am x
Begleitet bis         30 Tage   Begleitung endet am x
ID-Karte gültig bis   30 Tage   ID-Karte gültig bis x
===================== ========= ====================================





Kandidatensuche
---------------

**Übung**: 
Mitarbeiter sieht Stellenangebot und fragt Lino, 
welche potentiellen Kandidaten in der Datenbank sind.



