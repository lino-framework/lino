Manueller Testlauf DSBE
=======================

Um die system.log anzuzeigen, ein ssh-terminal auf lino öffnen und::

  tail -f /var/log/lino/system.log

- Detail einer *aus TIM importierten* Person aufrufen. 

  Ohne vorher was zu ändern den Speichern-Button der Person klicken.
  Dadurch sollte sich nichts verändern und es dürfte *keine Änderung* in der system.log erscheinen.
  :doc:`/blog/2011/0406`   
  
  Checkbox "circa" vom Geburtsdatum ankreuzen, Speichern. Bleibt sie angeschaltet?
  Wieder ausschalten und wieder speichern. Bleibt sie ausgeschaltet?

  Im Reiter "Sprachen" eine neue Sprache in "Sprachkenntnisse" eingeben.
  Die Änderung wird gleich nach Verlassen der Zelle in der system.log erscheinen.
  Dann den Speichern-Button der Person klicken.
  Dabei sollte nichts passieren und es dürfte *keine Änderung* in der system.log erscheinen.
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


