To-Do-Liste
===========

Kurzfristig
-----------

TODO:

- Sprachkenntnisse eingeben funktioniert noch nicht.
- Auch alle Daten aus PXS, die für DSBE nicht wichtig sind (z.B. Krankenkasse)

- Neue Tabelle "Arbeitslosengeld-Sperren"

  von | bis | Grund | Bemerkung

- Neue Tabelle AG-Sperrgründe:

  - Termin nicht eingehalten
  - ONEM-Auflagen nicht erfüllt


- Datensynchronisierung TIM->Lino

- NotesByPerson im Detail-Fenster einer Person sollte nur die wichtigen Ereignisse anzeigen (deren :attr:`notes.NoteType.important` eingeschaltet ist).

- Bei Insert in :class:`notes.NotesByPerson` wird Note.person (der fk zum Master) nicht eingetragen. Ein GET `/api/notes/NotesByPerson?fmt=insert` findet ja nie statt, weil NotesByPerson ein Slave-Report ist, der kein eigenes Fenster hat. Deshalb wird ein solcher Permalink nie generiert. Also :js:func:`Lino.notes.NotesByPerson.insert` darf sich darauf verlassen, einen caller zu haben, der dann seine get_master_params gefragt wird.

- Lokale Dateinamen benutzerfreundlich als Notiz erfassen. Eventuell neues Feld `attached_file` statt `url`? 

- Wenn ich eine NoteType lösche, werden momentan alle Notizen mit dieser Notizart gelöscht. Stattdessen muss das Löschen verweigert werden... Muss on_delete=RESTRICT oder on_delete=SET_NULL sein. Siehe `Django-Ticket 7539 <http://code.djangoproject.com/ticket/7539>`__.

- Noch testen (z.B. werden Filter gespeichert?)

- Insert in notes.Note : Datum sollte par défaut auf heute stehen, Sprache auf Deutsch.

- Release im :term:`DSBE` (:term:`Tups` kann momentan warten).

- Sprachabhängige Auswahl der Notizvorlage. Auf mehrsprachigen Sites hat das templates-Verzeichnis pro unterstützter Sprache ein entsprechendes Unterverzeichnis (`de`, `fr`, `en`,...), was aber in NoteType.template nicht gespeichert wird (und in der Auswahlliste nicht erscheint). Dort werden immer die Templates der Hauptsprache angezeigt. Wenn Sprache der Notiz nicht die Hauptsprache des Lino-Sites ist, dann wird das Template zunächst in der Notizsprache gesucht. Falls es dort nicht existiert (z.B. weil die Vorlage noch nicht übersetzt wurde oder multilingual ist), nimmt er die Standard-Vorlage aus der Hauptsprache.

- iCal-Dateien generieren. 
  Im :class:`notes.NoteType` wird definiert, ob Lino einen Termin (oder Erinnerung oder Task) 
  per E-Mail an den Benutzer verschicken soll.

- Quickfilter im Detail von Personen geht nicht. 

Kleinkram
---------

- Fenstertitel ändern bzw. anzeigen, welche GC momentan aktiv ist.

- Das Passfoto in dsbe.PersonDetail ist manchmal verzerrt oder noch nicht korrekt ausgeschnitten.

- Die Buttons der tbar sollten mit Icons versehen werden. Für manche Funktionen (Insert,Delete) gibt es vielleicht schon Icons aus der ExtJS.

- Abfragen mit komplexen Bedingungen zur Suche nach Personen

- Die Zeilenhöhe einer Grid muss einen sinnvollen Maximalwert kriegen. In Explorer / Notes hat man momentan den Eindruck, dass es nur eine Zeile gibt; in Wirklichkeit ist der Memo-Text der ersten Zeile so lang, dass die Zeilenhöhe größer als das Fenster ist.

- Hinter das QuickFilter-Feld muss ein Button, um den Filter zu aktivieren. Dass man einfach nur ENTER drücken muss ist nicht intuitiv.

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

- Anwendung lino.demo, die zum Generieren der Sphinx-Dokumentation bentuzt wird.
- Intersphinx nutzen und Lino von Lino-DSBE trennen
- dsbe.saffre-rumma.ee und igen.saffre-rumma.ee sollten nicht die Demo, sondern die Projekt-Doku zeigen. Für Demos wäre es ja elegant, einen Site demos.s-r.ee zu haben. Aber einfacher ist wahrscheinlich dsbe-demo.s-r-ee

Langfristig
-----------

- Filter auf virtuelle Kolonnen setzen können. Siehe :doc:`/blog/2010/0811`.

- Layout von Detail-Fenstern : in Lino sind die "Zeilen" momentan ja immer im "Blocksatz" (also links- und rechtsbündig). Das ist unkonventionell: alle RIA die ich kenne, machen ihre Formulare nur linksbündig.

- HtmlEditor oder TextArea? Der HtmlEditor verursacht deutliche Performanceeinbußen beim Bildschirmaufbau von Detail-Fenstern. Die Wahl sollte konfigurierbar sein. Markup auch.

- "About"-Fenster mit `thanks_to()` muss irgendwo sichtbar gemacht werden.

- lino.test_apps.properties funktioniert nicht, scheinbar ist `actors.discover()` nicht aufgerufen worden.

- Das Detail-Fenster sollte vielleicht par défaut nicht im Editier-Modus sein, sondern unten ein Button "Edit", und erst wenn man darauf klickt, werden alle Felder editierbar (und der Record in der Datenbank blockiert), und unten stehen dann zwei Buttons "Save" und "Cancel". Wobei darauf zu achten ist was passiert, wenn man während des Bearbeitens in der Grid auf eine andere Zeile klickt. Dann muss er am besten das Detail-Fenster speichern, und falls dort ungültige Daten stehen, in der Grid den Zeilenwechsel verweigern.

- `Report.date_format` muss in der Syntax des UI (d.h. ExtJS) angegeben werden. 

- Scripts wie :xfile:`fill.py`, :xfile:`load_tim.py`, :xfile:`send_invoices.py` usw. sollten durch `django-admin commands <http://docs.djangoproject.com/en/dev/howto/custom-management-commands/#howto-custom-management-commands>`_ ersetzt werden. Dazu brauche ich wahrscheinlich ein `Signal <http://docs.djangoproject.com/en/dev/topics/signals/>`_, das bei jedem Start eines Management Tools nach dem Laden der Modelle gefeuert wird. Vor load_data. Dort würde ich dann mein LinoSite.setup() aufrufen. Sieht aus wie `Django-Ticket 13024 <http://code.djangoproject.com/ticket/13024>`_.

- Prüfen, ob Dokumentvorlagen im `XSL-FO-Format <http://de.wikipedia.org/wiki/XSL-FO>`__ besser wären. `Apache FOP <http://xmlgraphics.apache.org/fop/>`__ als Formatierer. Warum OpenOffice.org nicht schon lange XSL-FO kann, ist mir ein Rätsel. AbiWord dagegen soll es können (laut `1 <http://www.ibm.com/developerworks/xml/library/x-xslfo/>`__ und `2 <http://searjeant.blogspot.com/2008/09/generating-pdf-from-xml-with-xsl-fo.html>`__).

- Inwiefern überschneiden sich :mod:`lino.modlib.system.models.SiteConfig` und :mod:`django.contrib.sites`? 

- Die interne Kolonnenliste eines Reports ist ja konstant. Also sollte ein Record im fmt=json nicht als ``dict`` sondern als ``list`` repräsentiert werden.

- Slave-Grid in eigenem Fenster öffnen

- :term:`disabled fields` sind noch schwer lesbar, wenn es sich um Comboboxen handelt.

- Benutzerverwaltung von der Kommandozeile aus. 
  In Lino-DSBE gibt es :xfile:`make_staff.py`, aber das ist nur ein sehr primitives Skript.