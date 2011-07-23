Manueller Testlauf DSBE
=======================

- Um die system.log anzuzeigen, ein ssh-terminal auf lino öffnen und::

    tail -f /var/log/lino/system.log

Speichern
---------

- Detail einer *aus TIM importierten* Person aufrufen. 

  Ohne vorher was zu ändern den Speichern-Button der Person klicken.
  Dadurch sollte sich nichts verändern und es dürfte *keine Änderung* in der system.log erscheinen.
  :doc:`/blog/2011/0406`   
  
  Checkbox "circa" vom Geburtsdatum ankreuzen, Speichern. Bleibt sie angeschaltet?
  Wieder ausschalten und wieder speichern. Bleibt sie ausgeschaltet?

  Im Reiter "Sprachen" eine neue Sprache in "Sprachkenntnisse" eingeben.
  Die Änderung wird gleich nach Verlassen der Zelle in der :xfile:`system.log` 
  erscheinen.
  Dann den Speichern-Button der Person klicken.
  Dabei sollte nichts passieren und es dürfte *keine Änderung* 
  in der :xfile:`system.log` erscheinen.
  :doc:`/blog/2011/0406`

- Detail einer Firma aufrufen, die *kein Kursanbieter* ist.

  Ohne vorher was zu ändern den Speichern-Button klicken.
  Dabei sollte nichts passieren und es dürfte *keine Änderung* in der system.log erscheinen.
  :doc:`/blog/2011/0406`

  Checkbox "Kursanbieter" einschalten und speichern.
  Die Checkbox sollte angeschaltet bleiben.
  
  In einem zweiten Browserfenster :menuselection:`Kurse-->Kursanbieter` aufrufen: 
  die Firma sollte dort nun sichtbar sein.
  
  Checkbox "Kursanbieter" wieder ausschalten und speichern.
  Die Checkbox sollte ausgeschaltet bleiben.
  
  Im zweiten Browserfenster auf "Refresh" klicken : 
  Firma sollte aus der Liste verschwunden sein.
  
  :doc:`/blog/2011/0406`

Einfügetexte
------------

- Notiz erstellen. Im Inhalt ein bisschen eintippen, 
  einige Einfügetexte einfügen, speichern, drucken.
  Nach den Drucken sind die meisten Felder schreibgeschützt (blau).
  Auf :guilabel:`Cache löschen` klicken (Felder werden wieder bearbeitbar).
  Eine kleine Änderung im Inhalt machen, speichern, drucken. 
  Prüfen, ob Änderung auch im Ausdruck sichtbar ist.

- Eine weitere Notiz erstellen. 
  Folgenden Textabschnitt (Quelle: Wikipedia) kopieren und einfügen:

    **Interpunktionsregeln bei Aufzählungen**

    Grundsätzlich werden aus Sicht der Interpunktionsregeln Aufzählungszeichen so behandelt, als seien sie nicht vorhanden. Das heißt, dass Interpunktion so gesetzt werden muss, als gäbe es keine typografische Gliederung.

    Beispiel:

      Der Mann erblickte ein gelbes Auto, einen schwarzen Hund, eine grüne Handtasche und ein braunes Pferd in seiner Küche.
      
    Dieser Satz wird zu folgendem:

      Der Mann erblickte

      - ein gelbes Auto,
      - einen schwarzen Hund,
      - eine grüne Handtasche
      - und ein braunes Pferd
      
      in seiner Küche.
  
  Speichern & drucken.  
