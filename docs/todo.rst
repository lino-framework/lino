To-Do-Liste
===========

Kurzfristig
-----------

- Quickfilter im Detail von Personen geht nicht.

- Man kann noch nicht nach Personen suchen, die ein bestimmtes Studium haben
  
- Datensynchronisierung TIM->Lino weiter beobachten.

- NotesByPerson im Detail-Fenster einer Person sollte nur die wichtigen Ereignisse anzeigen (deren :attr:`notes.NoteType.important` eingeschaltet ist).

- Lokale Dateinamen benutzerfreundlich als Notiz erfassen. Eventuell neues Feld `attached_file` statt `url`? 

- Wenn ich eine NoteType lösche, werden momentan alle Notizen mit dieser Notizart gelöscht. 
  Stattdessen muss das Löschen verweigert werden... 
  Muss on_delete=RESTRICT oder on_delete=SET_NULL sein. 
  Siehe `Django-Ticket 7539 <http://code.djangoproject.com/ticket/7539>`__.

- Sprachabhängige Auswahl der Notizvorlage. Das templates-Verzeichnis muss pro unterstützter Sprache ein entsprechendes Unterverzeichnis (`de`, `fr`, `en`,...) haben. Dieser Teil des Dateinamens wird in :attr:`notes.NoteType.template` nicht gespeichert und erscheint auch nicht in der Auswahlliste. Dort werden immer die Templates der Hauptsprache angezeigt. Wenn Sprache der Notiz nicht die Hauptsprache des Lino-Sites ist, dann wird das Template zunächst in der Notizsprache gesucht. Falls es dort nicht existiert (z.B. weil die Vorlage noch nicht übersetzt wurde oder multilingual ist), nimmt er die Standard-Vorlage aus der Hauptsprache.

- iCal-Dateien generieren. 
  Im :class:`notes.NoteType` wird definiert, ob Lino einen Termin (oder Erinnerung oder Task) 
  per E-Mail an den Benutzer verschicken soll.

- Einfügen :

  - Die Extra-Zeile sollte ganz leer sein (Standardwerte nicht anzeigen).

  - Wenn man z.B. in Companies.insert manuell eine ID eingibt, 
    dann ignoriert der Server die und vergibt trotzdem seine automatische nächste ID.


Kleinkram
---------

- Wie soll ich es machen, dass der Benutzer beim Auswählen der Krankenkasse einer Person nicht alle Firmen, sondern nur die Krankenkassen angezeigt bekommt? Etwa ein eigenes Feld `Company.is_health_insurance`?

- Fenstertitel ändern bzw. anzeigen, welche GC momentan aktiv ist.

- Das Passfoto in dsbe.PersonDetail ist manchmal verzerrt oder noch nicht korrekt ausgeschnitten.

- Die Buttons der tbar sollten mit Icons versehen werden. Für manche Funktionen (Insert,Delete) gibt es vielleicht schon Icons aus der ExtJS.

- Abfragen mit komplexen Bedingungen zur Suche nach Personen

- Die Zeilenhöhe einer Grid muss einen sinnvollen Maximalwert kriegen. In Explorer / Notes hat man momentan den Eindruck, dass es nur eine Zeile gibt; in Wirklichkeit ist der Memo-Text der ersten Zeile so lang, dass die Zeilenhöhe größer als das Fenster ist.

- Hinter das QuickFilter-Feld muss ein Button, um den Filter zu aktivieren. Dass man einfach nur TAB drücken muss ist nicht intuitiv.

- Links ordentlich anzeigen und bequem erfassen können.

- Benutzbarkeit per Tastatur verbessern (issue 11, issue 64) 

- Sehen können, nach welcher Kolonne eine Grid sortiert ist.

- Nach Duplikaten suchen vor Erstellen einer neuen Person (issue 85)

- URLs per drag & drop registrieren können

- `lino.test_apps.journals` funktioniert nicht bzw. wird nicht ausgeführt. Sieht aus als Django-Ticket 11696 doch noch nicht behoben ist. Aber mein Patch 20091107.diff funktioniert nicht mehr und ich bin auch noch nicht sicher. Muss vielleicht mal einen Testcase schreiben, um das Problem zu identifizieren...

- Prüfen, ob die neuen ExtJS-Features `Forms with vbox Layout <http://dev.sencha.com/deploy/dev/examples/form/vbox-form.html>`_ und
  `Composite Form Fields <http://dev.sencha.com/deploy/dev/examples/form/composite-field.html>`_ für Lino interessant sind.

Dokumentation
-------------

- Intersphinx installieren, damit folgende Links funktionieren: 
  :doc:`foo <dsbe:/tim2lino>`
  :doc:`/tim2lino`
  :class:`dsbe.models.Person`


Langfristig
-----------

- Filter auf virtuelle Kolonnen setzen können. Siehe :doc:`/blog/2010/0811`.

- Layout von Detail-Fenstern : in Lino sind die "Zeilen" momentan ja immer im "Blocksatz" (also links- und rechtsbündig). Das ist unkonventionell: alle RIA die ich kenne, machen ihre Formulare nur linksbündig.

- HtmlEditor oder TextArea? Der HtmlEditor verursacht deutliche Performanceeinbußen beim Bildschirmaufbau von Detail-Fenstern. Die Wahl sollte konfigurierbar sein. Markup auch.

- "About"-Fenster mit `thanks_to()` muss irgendwo sichtbar gemacht werden.

- lino.test_apps.properties funktioniert nicht, scheinbar ist `actors.discover()` nicht aufgerufen worden.

- Das Detail-Fenster sollte vielleicht par défaut nicht im Editier-Modus sein, sondern unten ein Button "Edit", und erst wenn man darauf klickt, werden alle Felder editierbar (und der Record in der Datenbank blockiert), und unten stehen dann zwei Buttons "Save" und "Cancel". Wobei darauf zu achten ist was passiert, wenn man während des Bearbeitens in der Grid auf eine andere Zeile klickt. Dann muss er am besten das Detail-Fenster speichern, und falls dort ungültige Daten stehen, in der Grid den Zeilenwechsel verweigern.

- `Report.date_format` muss in der Syntax des UI (d.h. ExtJS) angegeben werden. 

- Prüfen, ob Dokumentvorlagen im `XSL-FO-Format <http://de.wikipedia.org/wiki/XSL-FO>`__ besser wären. `Apache FOP <http://xmlgraphics.apache.org/fop/>`__ als Formatierer. Warum OpenOffice.org nicht schon lange XSL-FO kann, ist mir ein Rätsel. AbiWord dagegen soll es können (laut `1 <http://www.ibm.com/developerworks/xml/library/x-xslfo/>`__ und `2 <http://searjeant.blogspot.com/2008/09/generating-pdf-from-xml-with-xsl-fo.html>`__).

- Inwiefern überschneiden sich :mod:`lino.modlib.system.models.SiteConfig` und :mod:`django.contrib.sites`? 

- Die interne Kolonnenliste eines Reports ist ja konstant. Also sollte ein Record im fmt=json nicht als ``dict`` sondern als ``list`` repräsentiert werden.

- Slave-Grid in eigenem Fenster öffnen

- :term:`disabled fields` sind noch schwer lesbar, wenn es sich um Comboboxen handelt.

- Benutzerverwaltung von der Kommandozeile aus. 
  In Lino-DSBE gibt es :xfile:`make_staff.py`, aber das ist nur ein sehr primitives Skript.
  
- Im Fenster :menuselection:`System --> Site Configuration` müssten Delete und Insert noch weg. 

- Wenn ein Detail-Fenster nur ein Layout hat (nur einen Tab), dann ist der Titel dieses Layouts unnütz.

- http://code.google.com/p/extjs-public/
  und
  http://www.sencha.com/blog/2009/06/10/building-a-rating-widget-with-ext-core-30-final-and-google-cdn/
  lesen.  
  
- Feldgruppen. Z.B. bei den 3 Feldern für Arbeitserlaubnis (:attr:`dsbe.models.Person.work_permit`) in DSBE wäre es interessant, 
  dass das Label "Arbeitserlaubnis" einmal über der Gruppe steht und in den Labels der einzelnen Felder nicht wiederholt wird.

- Comboboxen auf Integerfeldern funktionieren nicht. Zeigen NaN als Text an.

- Strings aus :data:`lino.modlib.fields.KNOWLEDGE_CHOICES` werden von makemessages nicht gefunden, 
  weil sie Teil des "Lino-Kernels" und keine direkte Django application sind.
  Ebenso :mod:`lino.ui.extjs.ext_ui`, :mod:`lino.actions`, :mod:`lino.reports`, ...
  Rausfinden, ob man das nicht doch irgendwie automatisieren kann.
  Der Anfang ist gemacht in :srcref:`/Makefile`.
  Aber Achtung: `make mm` überschreibt jedesmal alle Übersetzungen , siehe auch: 
  :doc:`/blog/2010/1008`, 
  :doc:`/topics/i18n`
  
  
- Der JS-Code, der ein Detail-Fenster definiert, wird für jeden Report zweimal generiert. 
  Ein einziges Mal für alle Reports würde reichen.
  
- Layout-Editor: 

  - Fehlerbehandlung! Momentan knallt es, wenn man einen Tippfehler macht.
  - Schade, dass das Editorfenster das darunterliegende Fenster verdeckt und auch nicht aus dem Browserfenster rausbewegt werden kann. Mögliche Lösung: dass das Editorfenster sich die east region pflanzt. 
  - Button um Feldnamen komfortabel auszuwählen


- Ich würde in der Rückfrage zum Löschen eine oder mehrerer Records ja auch 
  gerne die `__unicode__` der zu löschenden Records anzeigen.
  FormPanel und GridPanel.get_selected() geben deshalb jetzt nicht mehr bloß eine Liste der IDs, sondern eine Liste der Records.
  Aber das nützt (noch) nichts, denn ich weiß nicht, wie ich den Grid-Store überredet bekomme, außer `data` 
  auch eine Eigenschaft `title` aus jedem Record rauszulesen. 
  Auf Serverseite wäre das kein Problem: ich bräuchte einfach nur title in `elem2rec1` statt in `elem2rec_detailed` zu setzen.
  Aber das interessiert den Store der Grid nicht. Kann sein, dass ich ihn konfigurieren kann...
  Oder ich würde es wie mit `disabled_fields` machen. Also ein neues automatisches virtuelles Feld __unicode__.
  
- Insert-Fenster: Für die Situationen, wo man viele neue Records hintereinander erfasst, könnte
    vielleicht ein zusätzlicher Knopf "Save and insert another" (wie im Django-Admin), 
    oder aber das automatische Schließen des Insert-Fensters im Report abschalten können.

