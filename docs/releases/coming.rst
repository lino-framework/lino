Coming
======


:checkin:`086ae8661d28`

Bugfixes:

- Im Grid-Fenster Personen. Schnellsuche "Muster", dann Doppelklick auf Max Mustermann, 
  dann im GeheZu nach 'jupa' suchen: Klienten mit "jupa" werden zwar im 
  Dropdown angezeigt, aber Lino springt nach Auswahl nicht darauf.
  Im Detail-Fenster blieb (zumindest für manche Operationen) 
  der quick-search-text aus der grid aktiv.
  Siehe auch :doc:`/blog/2012/0725`.
  
- __repr__ of a choicelist Choice failed under Python 2.6.6, 
  saying "Error in formatting: encode() takes no keyword arguments".
  Der Fehler schlug zu in watch_tim, wenn in TIM ein ChoiceListField 
  geändert worden war (z.B,. Geschlecht, Id-Karten-Art,...) und der neue 
  oder alte Wert in Lino einen Umlaut enthielt.
  (:doc:`/blog/2012/0725`)
  
  
- Traceback when trying to print a calendar 
  event whose Calendar.build_method is empty.
  (:doc:`/blog/2012/0725`)

- Tracebacks
  "Cannot re-execute Tx25-Anfrage #9 with non-empty ticket"
  and
  "Forced update did not affect any rows".

- :mod:`lino.utils.html2xhtml` produzierte ungültigen XHTML, 
  wenn im HTML Attribute mit Gänsefüßen waren. 
  Dadurch wurden manchmal Textfragmente (z.B. Aufgabenbereich eines Art607) 
  nicht ausgedruckt (und in der generierten `.odt` stand als 
  Fehlermeldung "not well-formed (invalid token)")
